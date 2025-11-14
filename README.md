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
* **Regisseur:** Regie beim Film, weitere Werke
* **Musik/Band:** Soundtrack, Bandinformationen, Alben, Titel, Genre, Mitglieder

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
* Fandom Wiki, Rotten Tomatoes etc. (zb. Trivia)
* Extraktion mittels NLP (Named Entity Recognition + Regex) von: Orten, Antagonisten, Liebhaberinnen, Fahrzeugen / Gadgets

## Ontologie
Eigene Ontologie `fi:` (Film Ontology) mit bestehenden Vokabularen:

| Namespace    | 	Beschreibung                                        |
|--------------|------------------------------------------------------|
| `fi:`        | 	eigene Film Ontology (Film-spezifische Beziehungen) |
| `foaf:`      | 	Personen & Organisationen (Darsteller, Bands)       |
| `mo:`        | 	Music Ontology (Titelsongs, Musiker)                |
| `linkedMDB:` | Linked Internet Movie Database                       |

Das `LinkedMDB` Vokabular (Schema, Tripels etc.) ist in der [TriblyDB](https://triplydb.com/AradhyaTripathi/linkedmdb) dokumentiert.

## Beispielhafte Reasoning-Regeln

* Wenn ein Ort in mehreren Filmen vorkommt → inferiere `fi:recurringLocation`.
* Wenn ein Auto mehrfach genutzt wird → inferiere `fi:iconicVehicle`.
* Wenn ein Musiker mehr als einen Song beigesteuert hat → inferiere `fi:bondComposer`.

## Mehrwert
Eine übersichtliche Visualisierung mit Streamlit schaffen.
* **Interaktive Karte:** Drehorte weltweit, Filter (Bond-Darsteller, Jahrzehnt, Film)
* **Netzwerkgraph:** Beziehungen zwischen Bond, Antagonisten, Liebhaberinnen, Fahrzeugen und Songs
* **Zeitstrahl:** Ratings