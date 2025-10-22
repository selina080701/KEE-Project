# Filmdatenbank
Knowledge Engineering and Extraction | MSc-DV | HS25 

**Teilnehmer:** Selina Steiner, Tamara Nyffeler

---

## Ausgangslage und Aufgabenstellung
Informationen zu Filmen, Schauspielern, Regisseuren und Filmmusik sind über zahlreiche Plattformen verstreut, was die strukturierte Analyse komplexer Zusammenhänge erschwert. Das Projekt zielt darauf ab, eine Ontologie zu entwickeln, die Filme, Mitwirkende und musikalische Elemente systematisch modelliert.

## Kerndatensatz
Der Kerndatensatz (CSV) umfasst rund 600 Filmtitel, extrahiert aus dem [cornell_movie_dialog](https://huggingface.co/datasets/cornell-movie-dialog/cornell_movie_dialog)-Datensatz. Enthalten sind die Attribute ID, Titel, Jahr, Rating, Votes und Genre.

## Knowledge Extraction
Auf Basis des Kerndatensatzes werden weitere Daten aus externen APIs und Triple Stores extrahiert und anschliessend folgende Entitäten modelliert:

* **Film:** Titel, Erscheinungsjahr, Genre 
* **Schauspieler:** Beteiligung am Film, Filmographie, biografische Daten
* **Regisseur:** Regie beim Film, weitere Werke
* **Musik/Band:** Soundtrack, Bandinformationen, Alben, Titel, Genre, Mitglieder

Diese Entitäten werden durch semantische Beziehungen miteinander verknüpft (z.B. „hat Schauspieler“, „wurde inszeniert von“, „enthält Soundtrack von“).

## Datenquellen
* **Wikidata** und **DBpedia**: Triple Store für Metadaten und biografische Informationen 
* **IMDb**: API zu Filmen, Schauspielern, Regisseuren, Soundtracks (https://www.imdb.com/interfaces/)
* **TMDb**: API für Film- und Personendaten (https://developer.themoviedb.org/docs/getting-started)
* **MusicBrainz:** API für Musikmetadaten (https://musicbrainz.org/doc/MusicBrainz_API)

## Ontologie
* Music Ontology: `mo` (http://purl.org/ontology/mo/)
* Personen und Bands: `foaf` (http://xmlns.com/foaf/spec/)
* eigene Ontolgoy: `fi` (Film Ontology) für film-spezifische Beziehungen

## Mehrwert
Mögliche Fragestellungen sind im Dokument `fragestellungen.md` aufgeführt.