# James Bond Universe
Knowledge Engineering and Extraction | MSc-DV | HS25 

**Teilnehmer:** Selina Steiner, Tamara Nyffeler

---

## Ausgangslage und Aufgabenstellung
Semantische Modellierung und Wissensextraktion im James Bond Universum.
Wie sind Charakter (zb. Bösewichte, Liebhaberinnen), Orte, Fahrzeuge und musikalische Elemente im James-Bond-Universum miteinander verknüpft und wie haben sich diese über die Zeit entwickelt?

## Kerndatensatz
[James Bond Movie Dataset](https://www.kaggle.com/datasets/dreb87/jamesbond?resource=download): CSV mit allen James-Bond-Filmen (ohne James Bond 007: No Time to Die)

## Knowledge Extraction
Auf Basis des Kerndatensatzes werden weitere Daten aus externen APIs und Triple Stores extrahiert und anschliessend folgende Entitäten modelliert:

* **Film:** Titel, Erscheinungsjahr, Genre
* **Schauspieler:** Beteiligung am Film, Filmographie, biografische Daten
* **Regisseur und Producer:** Regie beim Film
* **Musik/Band:** Soundtrack, Titel, Performer, Videosequenzen
* **Locations und Vehicles:** Filmschauplätze, Fahrzeuge

Diese Entitäten werden durch semantische Beziehungen miteinander verknüpft (z.B. „hat Schauspieler“, „wurde inszeniert von“, „enthält Soundtrack von“).

**Beispiel-Relationen**

```
:CasinoRoyale a                 fi:JamesBondMovie ;
            fi:hasID            :Q151904 ;
            fi:releaseYear      "2006" ;
            fi:hasBudget        "117465" ;
            fi:hasIMDBRating    "7.9" ;
            fi:hasRtnTomRating  "7.8" ;
            fi:hasActor         :DanielCraig ;
            fi:hasAntagonist    :LeChiffre ;
            fi:hasLoveInterest  :VesperLynd ;
            fi:hasLocation      :Venice, :London, :Miami ;
            fi:hasCar           :AstonMartinDBS ;
            fi:hasTitleSong     :YouKnowMyName .
```

## Datenquellen
**Strukturierte Quellen**
* **Wikidata**: Triple Store für Metadaten und biografische Informationen

**Unstrukturierte Quelle**
* Fandom Wiki, Wikipedia, LLM mittels Groq-Client
* Extraktion mittels NLP (Named Entity Recognition + Regex) von: Orten, Antagonisten, Liebhaberinnen, Fahrzeugen, Soundtracks

## Ontologie
Eigene Ontologie `fi:` (Film Ontology) mit bestehenden Vokabularen:

| Namespace    | 	Beschreibung                                        |
|--------------|------------------------------------------------------|
| `fi:`        | 	eigene Film Ontology (Film-spezifische Beziehungen) |
| `foaf:`      | 	Personen & Organisationen (Darsteller, Bands)       |
| `mo:`        | 	Music Ontology (Titelsongs, Musiker)                |
| `linkedMDB:` | Linked Internet Movie Database                       |

Das `LinkedMDB` Vokabular (Schema, Tripels etc.) ist in der [TriblyDB](https://triplydb.com/AradhyaTripathi/linkedmdb) dokumentiert.

## Mehrwert
Eine übersichtliche Visualisierung mit Streamlit schaffen.
* **Interaktive Karte:** Drehorte weltweit, Filter (Bond-Darsteller, Jahrzehnt, Film)
* **Netzwerkgraph:** Beziehungen zwischen Bond, Antagonisten, Liebhaberinnen, Fahrzeugen und Songs
* **Zeitstrahl:** Ratings

---

## Installationsanleitung

Dieser Abschnitt beschreibt, wie das Projekt lokal eingerichtet und ausgeführt werden kann.

### Voraussetzungen

- **Python 3.11 oder höher** muss auf Ihrem System installiert sein
- **Git** (optional, zum Klonen des Repositories)
- Eine aktive Internetverbindung für die Installation der Abhängigkeiten

### 1) Projekt herunterladen

Das Projekt ist auf GitHub als privates Repository verfügbar. Klonen Sie das Repository oder laden Sie es als ZIP-Datei herunter:

```bash
git clone https://github.com/selina080701/KEE-Project.git
cd KEE-Project
```

### 2) Virtuelle Umgebung erstellen

Erstellen Sie eine virtuelle Umgebung und aktivieren Sie diese:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3) Abhängigkeiten installieren

Die benötigten Bibliotheken sind im `requirements.txt`-File aufgelistet. Installieren Sie alle benötigten Python-Pakete mit pip:

```bash
pip install -r requirements.txt
```

### 4) Streamlit-Anwendung starten

Starten Sie die Webanwendung mit folgendem Befehl:

```bash
streamlit run app.py
```

Die Anwendung öffnet sich automatisch im Browser unter `http://localhost:8501`.

---

## Projektstruktur

```
James_Bond_Universe/
├── app.py                      # Haupt-Streamlit-Anwendung
├── README.md                   # Installationsanleitung
├── requirements.txt            # Python-Abhängigkeiten
├── report/                     # Projektbericht
├── pages/                      # Streamlit-Seiten
│   ├── intro_page.py
│   ├── movie_page.py
│   ├── map_page.py
│   ├── characters_page.py
│   ├── rdf_page.py
│   └── image_gallery_page.py
├── utils/                      # Hilfsfunktionen und Konfiguration
├── data/ 
    ├── jamesbond_raw.csv       # Kerndatensatz von Kaggle
    ├── triple_store/           # Kompletter Knowledge-Datensatz, serialisiert in JSON/OWL/TTL
├── data_pipeline/              # Datenextraktions-Skripte
├── extract_knowledge/          # extrahierte Knowledge-Files 
├── ontologies/                 # Skizzen zur RDF/OWL-Ontologie
└── archive/                    # Archivierte Skripte (nicht mehr relevant)
```
