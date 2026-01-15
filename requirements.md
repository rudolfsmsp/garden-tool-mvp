# Zaļais Pirksts – MVP prasības

## Mērķis un lietotāji

Zaļais Pirksts ir digitāls dārzkopības plānotājs hobija dārzkopjiem, ar īpašu uzsvaru uz senioriem un mazāk tehniskiem lietotājiem. Lietotne paredzēta latviešu valodā runājošiem lietotājiem un nedrīkst paļauties uz angļu valodas zināšanām. Dizainam jābūt vienkāršam, skaidram un paredzamam, ar zemu kognitīvo slodzi.

Lietotnes galvenais mērķis ir palīdzēt saprast, kas ir iestādīts katrā dobē, kas vēl jādara un kas jau ir paveikts, neizmantojot sarežģītas sistēmas.

## Funkcionālās prasības

### FR-01 Dārza struktūra pa dobēm

**Lietotāja stāsts:**  
Kā hobija dārzkopis es vēlos veidot un pārvaldīt dārzu pa dobēm, lai vienmēr zinātu, kas ir iestādīts un ieplānots katrā vietā.

**Prasības:**
- Sistēmai jāļauj veidot, skatīt, rediģēt un dzēst dobes.
- Katrai dobē jābūt nosaukumam.
- Dobes apraksts un foto ir neobligāti.
- Dobes dzēšanai vienmēr jāprasa apstiprinājums.

**Scenāriji:**
- Ja lietotājs ir “Mans dārzs” ekrānā un pievieno dobi ar nosaukumu “Tomāti”, dobe tiek saglabāta un parādās sarakstā.
- Ja lietotājam ir dobe “Tomāti” un viņš to atver, tiek parādīta dobēs detaļu informācija.
- Ja lietotājs mēģina dzēst dobi, sistēma prasa apstiprinājumu un dzēš tikai pēc apstiprinājuma.

### FR-02 Dobes atrašanas atbalsts

**Lietotāja stāsts:**  
Kā hobija dārzkopis es vēlos atpazīt dobes vizuāli ar foto un vienkāršām norādēm, lai ātri atrastu īsto dobi bez kartēm vai koordinātēm.

**Prasības:**
- Jāatbalsta dobes vizuāla identificēšana.
- Dobei var pievienot foto no reālās vietas.
- Dobei var pievienot īsu atrašanās norādi, piemēram, “pie žoga” vai “blakus siltumnīcai”.
- Nedrīkst prasīt GPS, koordinātas vai kartes piespraudes.

**Scenāriji:**
- Ja lietotājs pievieno dobei foto un norādi “pie siltumnīcas”, tie tiek saglabāti un parādīti.
- Ja ir vairākas dobes ar foto, atverot dobju atlasītāju, lietotājs var vizuāli izvēlēties pareizo dobi.

### FR-03 Augu uzskaite dobēs

**Lietotāja stāsts:**  
Kā hobija dārzkopis es vēlos pievienot augus katrai dobei, lai zinātu, kas kur ir iestādīts.

**Prasības:**
- Jāļauj pievienot augus dobei.
- Augus var izvēlēties no vienkārša iepriekšdefinēta saraksta.
- Lietotājs var pievienot arī pielāgotu auga nosaukumu.
- Visi dobei pievienotie augi jāparāda dobju skatā.

**Scenāriji:**
- Ja lietotājs dobē “Tomāti” pievieno augu “Tomāts”, tas parādās dobju skatā.
- Ja lietotājs ievada “Melnā tomātu šķirne”, augs tiek saglabāts un parādīts dobē.

### FR-04 Darbu plānošana

**Lietotāja stāsts:**  
Kā hobija dārzkopis es vēlos plānot vienkāršus darbus katrai dobei, lai atcerētos, kas un kad jādara.

**Prasības:**
- Darbi jāsaista ar vienu konkrētu dobi.
- Darbiem jābūt vienkāršam tipam, piemēram, “laistīt”, “mēslot”, “ravēt”.
- Darbiem var būt neobligāts datums.
- Darbi ir rediģējami un dzēšami ar apstiprinājumu.
- Darbus var atzīmēt kā izpildītus.

**Scenāriji:**
- Ja lietotājs dobē “Tomāti” izveido darbu “laistīt” ar datumu, tas tiek saglabāts un parādīts.
- Ja lietotājs atzīmē darbu kā izpildītu, tas tiek atzīmēts kā paveikts.

### FR-05 Darbu atgādinājumi

**Lietotāja stāsts:**  
Kā hobija dārzkopis es vēlos saņemt mierīgus atgādinājumus par darbiem, lai tos neaizmirstu, un iespēju atgādinājumus izslēgt.

**Prasības:**
- Atgādinājumi ir neobligāti.
- Valodai jābūt mierīgai un vienkāršai.
- Atgādinājumi nedrīkst bloķēt lietotni.
- Lietotājam jāspēj atgādinājumus izslēgt.

**Scenāriji:**
- Ja atgādinājumi ir ieslēgti un darbs ir jāizpilda, lietotājs saņem ziņu “Šodien jāpalaista Tomāti”.
- Ja lietotājs atslēdz atgādinājumus, tie vairs netiek rādīti.

### FR-06 Darbu vēsture

**Lietotāja stāsts:**  
Kā hobija dārzkopis es vēlos automātisku paveikto darbu vēsturi, lai redzētu, ko jau esmu izdarījis.

**Prasības:**
- Pabeigtie darbi jāglabā vēsturē automātiski.
- Vēsturē jāparāda darba nosaukums, datums un saistītā dobe.
- Lietotājam nav manuāli jāpārvalda vēsture.

**Scenāriji:**
- Ja lietotājs pabeidz darbu “laistīt”, tas parādās darbu vēsturē.

### FR-07 Foto dokumentēšana

**Lietotāja stāsts:**  
Kā hobija dārzkopis es vēlos pievienot foto dobēm un paveiktiem darbiem, lai sekotu progresam un atcerētos, ko darīju.

**Prasības:**
- Jāļauj pievienot foto dobēm.
- Jāļauj pievienot foto paveiktiem darbiem.
- Foto nav jārediģē vai jāmarķē.

**Scenāriji:**
- Ja lietotājs pēc darba pievieno foto, tas tiek saglabāts un redzams vēsturē.

### FR-08 Vienkārša navigācija

**Lietotāja stāsts:**  
Kā hobija dārzkopis es vēlos vienkāršu un paredzamu navigāciju, lai nekad nepazustu lietotnē.

**Prasības:**
- Lietotnē jābūt ne vairāk kā trim galvenajām sadaļām.
- Navigācijai jābūt konsekventai visos ekrānos.
- Lietotājam vienmēr jāzina, kur viņš atrodas.

**Scenārijs:**
- Ja lietotājs pārvietojas starp ekrāniem, navigācijas izvietojums paliek nemainīgs.

### FR-09 Kļūdu tolerance un drošība

**Lietotāja stāsts:**  
Kā hobija dārzkopis es vēlos, lai lietotne nepieļauj nejaušas kļūdas, lai nebaidītos to izmantot.

**Prasības:**
- Visi destruktīvie soļi jāapstiprina.
- Kļūdu ziņojumiem jābūt vienkāršā latviešu valodā.
- Jāatļauj darbību atcelšana.

**Scenārijs:**
- Ja lietotājs mēģina dzēst dobi, sistēma prasa apstiprinājumu un dzēš tikai pēc apstiprinājuma.

## Nefunkcionālās prasības

### Pieejamība
- Jāatbilst WCAG 2.1 AA līmenim.
- Tekstam jābūt ar pietiekamu kontrastu.
- Jāatbalsta teksta palielināšana līdz 200 procentiem.
- Visām darbībām jābūt iespējām ar tastatūru vai palīgtehnoloģijām.
- Interaktīvajiem elementiem jābūt skaidram fokusam.
- Skārienmērķiem jābūt pietiekami lieliem.
- Informāciju nedrīkst nodot tikai ar krāsu.

### Valoda
- Visa lietotne ir latviešu valodā.
- Lietotāja saskarnē nedrīkst parādīties angļu vārdi.
- Valodai jābūt vienkāršai un netehniskai.

### Lietojamība
- Sākumlapa un darbplūsma ir mierīga un paredzama.
- Nav agresīvu paziņojumu vai mirgojošu elementu.
- Nav sarežģītu žestu vai slēptu darbību.

### Veiktspēja un stabilitāte
- Lietotnei jāielādējas ātri.
- Pamata skatījumiem jāstrādā uzticami arī ar ierobežotu savienojumu.
- Kļūdas jāapstrādā saprotami un mierīgi.

## Lokālās darbības prasība

Lietotnei jāspēj darboties lokāli uz lietotāja ierīces. Attīstības režīmā visām pamatfunkcijām jāstrādā uz localhost bez ārējiem servisiem vai mākoņa atkarībām.
