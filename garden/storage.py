import os
import uuid


def ensure_uploads(path):
    os.makedirs(path, exist_ok=True)


def save_upload(upload_dir, field_storage):
    if not field_storage or not getattr(field_storage, "filename", None):
        return ""
    filename = os.path.basename(field_storage.filename)
    ext = os.path.splitext(filename)[1].lower()
    safe_name = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(upload_dir, safe_name)
    with open(path, "wb") as handle:
        handle.write(field_storage.file.read())
    return safe_name


def save_streamlit_upload(upload_dir, uploaded_file):
    if uploaded_file is None:
        return ""
    filename = os.path.basename(uploaded_file.name)
    ext = os.path.splitext(filename)[1].lower()
    safe_name = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(upload_dir, safe_name)
    with open(path, "wb") as handle:
        handle.write(uploaded_file.getvalue())
    return safe_name
