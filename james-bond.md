# Knowledge Engineering & Extraction – James Bond Universe

**Thema:** Semantische Modellierung und Wissensextraktion im James-Bond-Universum

--- 

## Forschungsfrage

Wie sind Charaktere (zb. Bösewichte, Liebhaberinnen), Orte, Fahrzeuge und musikalische Elemente im James-Bond-Universum miteinander verknüpft, und wie haben sich diese über die Zeit entwickelt?

## Datengrundlage
**Strukturierte Quellen**
* CSV mit allen James-Bond-Filmen laden oder direkt aus Wikidata etc.
* Wikidata, DBpedia, IMDb, TMDb, MusicBrainz

**Unstrukturierte Quelle**
* Fandom Wiki, Rotten Tomatoes etc (zb. Trivia)
* Extraktion mittels NLP (Named Entity Recognition + Regex) von:
  * Orten (zB. „London“, „Fort Knox“)
  * Antagonisten (zB. „Goldfinger“)
  * Liebhaberinnen
  * Fahrzeugen / Gadgets

## Ontologie

Eigene Ontologie `fi:` (Film Ontology) mit bestehenden Vokabularen:

| Namespace | 	Beschreibung                                        |
|-----------|------------------------------------------------------|
| `fi:`     | 	Eigene Film Ontology (Film-spezifische Beziehungen) |
| `foaf:`   | 	Personen & Organisationen (Darsteller, Bands)       |
| `mo:`     | 	Music Ontology (Titelsongs, Musiker)                |

**Beispiel-Relationen**

```
:Goldfinger a                   fi:Film ;
            fi:releaseYear      "1964" ;
            fi:hasActor         :SeanConnery ;
            fi:hasAntagonist    :AuricGoldfinger ;
            fi:hasLoveInterest  :PussyGalore ;
            fi:hasLocation      :FortKnox ;
            fi:hasCar           :AstonMartinDB5 ;
            fi:hasSong          :GoldfingerTheme .
```

## Knowledge Extraction Workflow

1. Filmliste erstellen: CSV mit Titel, Jahr, Bond-Darsteller etc.
2. Externe strukturierte Daten abrufen
3. Unstrukturierte Texte extrahieren
4. NLP-Analyse:
   * Named Entity Recognition (z. B. mit spaCy)
   * Erkennung und Klassifikation von Entitäten (Ort, Person, Objekt)
5. RDF-Generierung: neue Triples (z. B. „hat Ort“, „hat Auto“, „hat Antagonisten“)
6. Integration in Triple Store: Zusammenführung aller Daten zu einem semantischen Wissensgraphen

## Visualisierung (Streamlit)

**Interaktive Karte:**
* Drehorte weltweit
* Filter nach Bond-Darsteller, Jahrzehnt oder Film

**Netzwerkgraph:**
* Beziehungen zwischen Bond, Antagonisten, Liebhaberinnen, Fahrzeugen und Songs


**Zeitstrahl:**

* Chronologische Darstellung aller Filme
* Anzeige von Bond-Darsteller, Hauptgegner, Song und Fahrzeug

## Beispielhafte Reasoning-Regeln

* Wenn ein Ort in mehreren Filmen vorkommt → inferiere `fi:recurringLocation`.
* Wenn ein Auto mehrfach genutzt wird → inferiere `fi:iconicVehicle`.
* Wenn ein Musiker mehr als einen Song beigesteuert hat → inferiere `fi:bondComposer`.
