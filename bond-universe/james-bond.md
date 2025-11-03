# Knowledge Engineering & Extraction – James Bond Universe

**Thema:** Semantische Modellierung und Wissensextraktion im James-Bond-Universum

--- 

## Forschungsfrage

Wie sind Charaktere (zb. Bösewichte, Liebhaberinnen), Orte, Fahrzeuge und musikalische Elemente im James-Bond-Universum miteinander verknüpft, und wie haben sich diese über die Zeit entwickelt?

## Datengrundlage
**Strukturierte Quellen**
* [James Bond Movie Dataset](https://www.kaggle.com/datasets/dreb87/jamesbond?resource=download): CSV mit allen James-Bond-Filmen (ohne James Bond 007: No Time to Die)
* Wikidata, DBpedia, IMDb, TMDb, MusicBrainz

**Unstrukturierte Quelle**
* Fandom Wiki, Rotten Tomatoes etc. (zb. Trivia)
* Extraktion mittels NLP (Named Entity Recognition + Regex) von: Orten, Antagonisten, Liebhaberinnen, Fahrzeugen / Gadgets

## Ontologie

Eigene Ontologie `fi:` (Film Ontology) mit bestehenden Vokabularen:

| Namespace | 	Beschreibung                                        |
|-----------|------------------------------------------------------|
| `fi:`     | 	eigene Film Ontology (Film-spezifische Beziehungen) |
| `foaf:`   | 	Personen & Organisationen (Darsteller, Bands)       |
| `mo:`     | 	Music Ontology (Titelsongs, Musiker)                |

**Beispiel-Relationen**

```
:CasinoRoyale a                 fi:Film ;
            fi:releaseYear      "2006" ;
            fi:hasActor         :DanielCraig ;
            fi:hasAntagonist    :LeChiffre ;
            fi:hasLoveInterest  :VesperLynd ;
            fi:hasLocation      :Venice ;
            fi:hasCar           :AstonMartinDBS ;
            fi:hasSong          :YouKnowMyName .
```

## Knowledge Extraction Workflow

1. Filmliste erstellen: CSV mit Titel, Jahr, Bond-Darsteller, Wikidata-ID etc.
2. James Bond 007: No Time to Die im CSV hinzufügen
3. Externe strukturierte Daten abrufen
4. Unstrukturierte Texte extrahieren
5. NLP-Analyse:
   * Named Entity Recognition (zb. mit spaCy)
   * Erkennung und Klassifikation von Entitäten (Ort, Person, Objekt)
6. RDF-Generierung: neue Triples (zb. „hat Ort“, „hat Auto“, „hat Antagonisten“)
7. Integration in Triple Store: Zusammenführung aller Daten zu einem semantischen Wissensgraphen

## Visualisierung (Streamlit)

* **Interaktive Karte:** Drehorte weltweit, Filter (Bond-Darsteller, Jahrzehnt, Film)
* **Netzwerkgraph:** Beziehungen zwischen Bond, Antagonisten, Liebhaberinnen, Fahrzeugen und Songs
* **Zeitstrahl:** Ratings

## Beispielhafte Reasoning-Regeln

* Wenn ein Ort in mehreren Filmen vorkommt → inferiere `fi:recurringLocation`.
* Wenn ein Auto mehrfach genutzt wird → inferiere `fi:iconicVehicle`.
* Wenn ein Musiker mehr als einen Song beigesteuert hat → inferiere `fi:bondComposer`.
