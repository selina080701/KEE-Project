# KEE-Project
Knowledge Engineering and Extraction | MSc-DV | HS25 

GruppenmitgliederInnen:
* Selina Steiner
* Tamara Nyffeler

## Ausgangslage und Aufgabenstellung
Informationen zu Filmen, Schauspielern, Regisseuren und Filmmusik sind im Internet über zahlreiche Plattformen und Formate verstreut. Dies erschwert die strukturierte Analyse komplexer Zusammenhänge zwischen diesen Entitäten. Dieses Projekt zielt darauf ab, eine Ontologie zu entwickeln, die Filme und deren Mitwirkende sowie musikalische Elemente systematisch modelliert.

## Kerndatensatz (Was wird modelliert)
Der Kerndatensatz (CSV) besteht aus einer Liste von rund 600 auswählbarer Filmtitel. Für jeden Film werden folgende Entitäten und Beziehungen modelliert:

* **Film:** Titel, Erscheinungsjahr, Genre
* **Schauspieler:** Beteiligung am Film, vollständige Filmographie, biografische Daten
* **Regisseur:** Regie beim Film, weitere Regiearbeiten
* **Musik/Band:** Soundtrack-Zuordnung, Bandinformationen, Alben, Titel, Genre, Mitglieder

Diese Entitäten werden durch semantische Beziehungen miteinander verknüpft (z.B. „hat Schauspieler“, „wurde inszeniert von“, „enthält Soundtrack von“).

## Datenquellen
* **Wikidata** und **DBpedia**: Triple Store für ergänzende Metadaten und biografische Informationen 
* **IMDb**: API zu Filmen, Schauspielern, Regisseuren, Soundtracks (https://www.imdb.com/interfaces/)
* **TMDb**: API für Film- und Personendaten (https://developer.themoviedb.org/docs/getting-started)
* **MusicBrainz:** API für Musikmetadaten (https://musicbrainz.org/doc/MusicBrainz_API)

## Ontologie
* Verwendung der Music Ontology `mo` (http://purl.org/ontology/mo/)
* Nutzung von `foaf` (http://xmlns.com/foaf/spec/) für Personen und Bands
* Erweiterung um eigene `fi` (Film Ontology) für film-spezifische Beziehungen

## Mehrwert
Mögliche Fragestellungen sind im Dokument `fragestellungen.md` aufgeführt.