import datetime as dt
import os
from typing import Optional

import streamlit as st

from garden import constants, db
from garden.storage import ensure_uploads, save_streamlit_upload

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT_DIR, "garden.db")
UPLOADS_DIR = os.path.join(ROOT_DIR, "uploads")
LOGO_PATH = os.path.join(ROOT_DIR, "static", "logo.svg")
HERO_PATH = os.path.join(ROOT_DIR, "static", "hero.svg")
PLACEHOLDER_PATH = os.path.join(ROOT_DIR, "static", "placeholder.svg")


def init_app():
    ensure_uploads(UPLOADS_DIR)
    db.ensure_schema(DB_PATH)


def get_setting(key: str) -> str:
    row = db.fetch_one(DB_PATH, "SELECT value FROM settings WHERE key = ?", (key,))
    return row["value"] if row else ""


def set_setting(key: str, value: str) -> None:
    db.execute(
        DB_PATH,
        "INSERT INTO settings (key, value) VALUES (?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
        (key, value),
    )


def today_iso() -> str:
    return dt.date.today().isoformat()


def format_date(value: Optional[str]) -> str:
    if not value:
        return ""
    try:
        return dt.date.fromisoformat(value).strftime("%d.%m.%Y")
    except ValueError:
        return value


def load_svg(path: str) -> str:
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def read_image(path: str) -> bytes:
    with open(path, "rb") as handle:
        return handle.read()


def is_svg(path: str) -> bool:
    if path.lower().endswith(".svg"):
        return True
    try:
        with open(path, "rb") as handle:
            sample = handle.read(200)
        return b"<svg" in sample.lower()
    except OSError:
        return False


def render_svg(path: str, max_width: int = 220) -> None:
    svg = load_svg(path)
    st.markdown(
        f"<div class='svg-image' style='max-width:{max_width}px'>{svg}</div>",
        unsafe_allow_html=True,
    )


def render_image(path: str, max_width: int = 240) -> None:
    if is_svg(path):
        render_svg(path, max_width=max_width)
        return
    try:
        st.image(read_image(path), use_container_width=True)
    except Exception:
        st.markdown("<div class='image-fallback'>Attēlu nevarēja ielādēt.</div>", unsafe_allow_html=True)


def get_photo_path(filename: Optional[str]) -> str:
    if not filename:
        return PLACEHOLDER_PATH
    return os.path.join(UPLOADS_DIR, filename)


def page_header(title: str, subtitle: str) -> None:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"## {title}")
        st.caption(subtitle)
    with col2:
        render_image(HERO_PATH, max_width=220)
        st.image(read_image(HERO_PATH), use_container_width=True)


def render_sidebar() -> str:
    st.sidebar.markdown(load_svg(LOGO_PATH), unsafe_allow_html=True)
    st.sidebar.markdown("### Zaļais Pirksts")
    return st.sidebar.radio(
        "Galvenās sadaļas",
        ["Mans dārzs", "Dobes atrast", "Vēsture"],
    )


def render_bed_form() -> None:
    st.markdown("### Jauna dobe")
    with st.form("create_bed"):
        name = st.text_input("Dobes nosaukums", placeholder="Piemēram, Tomāti")
        description = st.text_area("Apraksts (neobligāts)")
        location_hint = st.text_input("Atrašanās norāde (neobligāta)")
        photo = st.file_uploader("Dobes foto (neobligāts)", type=["png", "jpg", "jpeg"])
        submitted = st.form_submit_button("Saglabāt dobi")
    if submitted and name.strip():
        photo_path = save_streamlit_upload(UPLOADS_DIR, photo)
        db.execute(
            DB_PATH,
            "INSERT INTO beds (name, description, location_hint, photo_path) VALUES (?, ?, ?, ?)",
            (name.strip(), description.strip(), location_hint.strip(), photo_path),
        )
        st.success("Dobe ir saglabāta.")
        st.rerun()


def render_bed_card(bed) -> None:
    photo_path = get_photo_path(bed["photo_path"])
    with st.container(border=True):
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"#### {bed['name']}")
            if bed["description"]:
                st.write(bed["description"])
            if bed["location_hint"]:
                st.caption(f"Atrašanās vieta: {bed['location_hint']}")
        with col2:
            render_image(photo_path, max_width=240)
            st.image(read_image(photo_path), use_container_width=True)

        plants = db.fetch_all(DB_PATH, "SELECT * FROM plants WHERE bed_id = ? ORDER BY id DESC", (bed["id"],))
        tasks = db.fetch_all(
            DB_PATH,
            "SELECT * FROM tasks WHERE bed_id = ? AND completed_at IS NULL ORDER BY task_date IS NULL, task_date",
            (bed["id"],),
        )

        tabs = st.tabs(["Augi", "Darbi", "Rediģēt", "Dzēst"])
        with tabs[0]:
            if plants:
                st.write(", ".join(p["name"] for p in plants))
            else:
                st.caption("Nav pievienotu augu.")
            with st.form(f"add_plant_{bed['id']}"):
                plant_choice = st.selectbox(
                    "Auga nosaukums",
                    constants.PLANT_OPTIONS + ["Cits nosaukums"],
                    key=f"plant_choice_{bed['id']}",
                )
                custom_name = ""
                if plant_choice == "Cits nosaukums":
                    custom_name = st.text_input("Pielāgots nosaukums", key=f"custom_plant_{bed['id']}")
                submitted = st.form_submit_button("Pievienot augu")
            if submitted:
                name = custom_name.strip() if plant_choice == "Cits nosaukums" else plant_choice
                if name:
                    db.execute(
                        DB_PATH,
                        "INSERT INTO plants (bed_id, name) VALUES (?, ?)",
                        (bed["id"], name),
                    )
                    st.success("Augs pievienots.")
                    st.rerun()
        with tabs[1]:
            if tasks:
                for task in tasks:
                    cols = st.columns([2, 2, 1, 1, 1])
                    cols[0].markdown(f"**{task['task_type']}**")
                    cols[1].write(format_date(task["task_date"]) or "Bez datuma")
                    if cols[2].button("Paveikts", key=f"done_{task['id']}"):
                        db.execute(
                            DB_PATH,
                            "UPDATE tasks SET completed_at = ? WHERE id = ?",
                            (today_iso(), task["id"]),
                        )
                        st.rerun()
                    if cols[3].button("Rediģēt", key=f"edit_{task['id']}"):
                        st.session_state[f"edit_task_{task['id']}"] = True
                    if cols[4].button("Dzēst", key=f"delete_{task['id']}"):
                        db.execute(DB_PATH, "DELETE FROM tasks WHERE id = ?", (task["id"],))
                        st.rerun()
                    if st.session_state.get(f"edit_task_{task['id']}"):
                        with st.form(f"edit_task_form_{task['id']}"):
                            task_type = st.selectbox(
                                "Darba veids",
                                constants.TASK_TYPES,
                                index=constants.TASK_TYPES.index(task["task_type"])
                                if task["task_type"] in constants.TASK_TYPES
                                else 0,
                                key=f"task_type_{task['id']}",
                            )
                            task_date = st.date_input(
                                "Datums",
                                value=dt.date.fromisoformat(task["task_date"]) if task["task_date"] else None,
                                key=f"task_date_{task['id']}",
                            )
                            updated = st.form_submit_button("Saglabāt")
                        if updated:
                            db.execute(
                                DB_PATH,
                                "UPDATE tasks SET task_type = ?, task_date = ? WHERE id = ?",
                                (task_type, task_date.isoformat() if task_date else None, task["id"]),
                            )
                            st.session_state.pop(f"edit_task_{task['id']}", None)
                            st.rerun()
            else:
                st.caption("Nav ieplānotu darbu.")

            with st.form(f"add_task_{bed['id']}"):
                task_type = st.selectbox("Darba veids", constants.TASK_TYPES, key=f"task_type_new_{bed['id']}")
                task_date = st.date_input("Datums (neobligāts)", value=None, key=f"task_date_new_{bed['id']}")
                task_photo = st.file_uploader(
                    "Darba foto (neobligāts)", type=["png", "jpg", "jpeg"], key=f"task_photo_{bed['id']}"
                )
                submitted = st.form_submit_button("Pievienot darbu")
            if submitted:
                photo_path = save_streamlit_upload(UPLOADS_DIR, task_photo)
                db.execute(
                    DB_PATH,
                    "INSERT INTO tasks (bed_id, task_type, task_date, photo_path) VALUES (?, ?, ?, ?)",
                    (bed["id"], task_type, task_date.isoformat() if task_date else None, photo_path),
                )
                st.success("Darbs pievienots.")
                st.rerun()
        with tabs[2]:
            with st.form(f"edit_bed_{bed['id']}"):
                name = st.text_input("Dobes nosaukums", value=bed["name"])
                description = st.text_area("Apraksts", value=bed["description"] or "")
                location_hint = st.text_input("Atrašanās norāde", value=bed["location_hint"] or "")
                photo = st.file_uploader(
                    "Jauns dobes foto (neobligāts)", type=["png", "jpg", "jpeg"], key=f"photo_{bed['id']}"
                )
                submitted = st.form_submit_button("Saglabāt izmaiņas")
            if submitted and name.strip():
                photo_path = save_streamlit_upload(UPLOADS_DIR, photo)
                if photo_path:
                    db.execute(
                        DB_PATH,
                        "UPDATE beds SET name = ?, description = ?, location_hint = ?, photo_path = ? WHERE id = ?",
                        (name.strip(), description.strip(), location_hint.strip(), photo_path, bed["id"]),
                    )
                else:
                    db.execute(
                        DB_PATH,
                        "UPDATE beds SET name = ?, description = ?, location_hint = ? WHERE id = ?",
                        (name.strip(), description.strip(), location_hint.strip(), bed["id"]),
                    )
                st.success("Dobe atjaunināta.")
                st.rerun()
        with tabs[3]:
            st.warning("Dzēšana ir neatgriezeniska.")
            confirm = st.checkbox("Apstiprinu, ka vēlos dzēst šo dobi.", key=f"confirm_{bed['id']}")
            if st.button("Dzēst dobi", disabled=not confirm, key=f"delete_bed_{bed['id']}"):
                db.execute(DB_PATH, "DELETE FROM beds WHERE id = ?", (bed["id"],))
                st.success("Dobe dzēsta.")
                st.rerun()


def render_garden_page():
    page_header("Mans dārzs", "Pārskatiet dobes, augus un darbus vienuviet.")
    render_bed_form()

    st.markdown("### Dobes")
    search = st.text_input("Meklēt dobi", placeholder="Ievadiet nosaukumu")
    beds = db.fetch_all(DB_PATH, "SELECT * FROM beds ORDER BY id DESC")
    if search.strip():
        beds = [bed for bed in beds if search.lower() in bed["name"].lower()]
    if not beds:
        st.info("Nav izveidotu dobju. Pievienojiet pirmo dobi.")
        return
    for bed in beds:
        render_bed_card(bed)


def render_locator_page():
    page_header("Dobes atrast", "Atrodiet dobes pēc foto un norādēm.")
    beds = db.fetch_all(DB_PATH, "SELECT * FROM beds ORDER BY id DESC")
    if not beds:
        st.info("Nav dobju, ko parādīt.")
        return
    cols = st.columns(2)
    for idx, bed in enumerate(beds):
        with cols[idx % 2]:
            photo_path = get_photo_path(bed["photo_path"])
            with st.container(border=True):
                render_image(photo_path, max_width=260)
                st.image(read_image(photo_path), use_container_width=True)
                st.markdown(f"**{bed['name']}**")
                if bed["location_hint"]:
                    st.caption(bed["location_hint"])


def render_history_page():
    page_header("Vēsture", "Pārskatiet paveiktos darbus un atgādinājumus.")

    reminders_enabled = get_setting("reminders_enabled") == "1"
    reminders = db.fetch_all(
        DB_PATH,
        """
        SELECT tasks.*, beds.name AS bed_name
        FROM tasks
        JOIN beds ON beds.id = tasks.bed_id
        WHERE tasks.completed_at IS NULL
          AND tasks.task_date IS NOT NULL
          AND tasks.task_date <= ?
        ORDER BY tasks.task_date
        """,
        (today_iso(),),
    )

    st.markdown("### Atgādinājumi")
    if reminders_enabled:
        if reminders:
            for task in reminders:
                st.info(f"Šodien jāpaveic {task['task_type']} dobē {task['bed_name']}.")
        else:
            st.caption("Šodien nav ieplānotu darbu.")
    else:
        st.caption("Atgādinājumi ir izslēgti.")

    if st.toggle("Atgādinājumi ieslēgti", value=reminders_enabled):
        set_setting("reminders_enabled", "1")
    else:
        set_setting("reminders_enabled", "0")

    st.divider()
    st.markdown("### Paveikto darbu vēsture")
    tasks = db.fetch_all(
        DB_PATH,
        """
        SELECT tasks.*, beds.name AS bed_name
        FROM tasks
        JOIN beds ON beds.id = tasks.bed_id
        WHERE tasks.completed_at IS NOT NULL
        ORDER BY tasks.completed_at DESC
        """,
    )
    if not tasks:
        st.caption("Vēsturē pagaidām nav darbu.")
        return
    for task in tasks:
        with st.container(border=True):
            st.markdown(f"**{task['task_type']}**")
            st.caption(f"{task['bed_name']} · {format_date(task['completed_at'])}")
            photo_path = get_photo_path(task["photo_path"])
            render_image(photo_path, max_width=320)
            st.image(read_image(photo_path), use_container_width=True)
            if not task["photo_path"]:
                upload = st.file_uploader(
                    "Pievienot foto", type=["png", "jpg", "jpeg"], key=f"history_photo_{task['id']}"
                )
                if upload:
                    photo_name = save_streamlit_upload(UPLOADS_DIR, upload)
                    db.execute(
                        DB_PATH,
                        "UPDATE tasks SET photo_path = ? WHERE id = ?",
                        (photo_name, task["id"]),
                    )
                    st.success("Foto pievienots.")
                    st.rerun()


def inject_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background: #edf3ef;
            color: #1f2b24;
            font-size: 18px;
        }
        section[data-testid="stSidebar"] {
            background: #f8fbf9;
            background: #f4f8f6;
        }
        section[data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid #d5e2db;
        }
        .block-container {
            padding-top: 2rem;
        }
        .svg-image svg {
            width: 100%;
            height: auto;
        }
        .stApp [data-testid="stContainer"] {
            background: #ffffff;
            border-radius: 16px;
            padding: 1rem;
            border: 1px solid #d5e2db;
        }
        .image-fallback {
            background: #f1f5f2;
            border-radius: 12px;
            padding: 16px;
            color: #526158;
            text-align: center;
        }
        .stButton button,
        .stTextInput input,
        .stTextArea textarea,
        .stSelectbox select,
        .stDateInput input {
            font-size: 17px;
        }
        [data-testid="stMarkdownContainer"] h2 {
            font-size: 1.6rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main():
    st.set_page_config(page_title="Zaļais Pirksts", page_icon="🌿", layout="wide")
    init_app()
    inject_styles()

    page = render_sidebar()
    if page == "Mans dārzs":
        render_garden_page()
    elif page == "Dobes atrast":
        render_locator_page()
    else:
        render_history_page()


if __name__ == "__main__":
    main()
