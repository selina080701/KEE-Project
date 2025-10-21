# KEE-Project
Knowledge Engineering and Extraction | MSc-DV | HS25 

GruppenmitgliederInnen:
* Selina Steiner
* Tamara Nyffeler

## Ausgangslage und Aufgabenstellung
Informationen zu Filmen, Schauspielern, Regisseuren und Filmmusik sind im Internet über zahlreiche Plattformen und Formate verstreut. Dies erschwert die strukturierte Analyse komplexer Zusammenhänge zwischen diesen Entitäten. Dieses Projekt zielt darauf ab, eine Ontologie zu entwickeln, die Filme und deren Mitwirkende sowie musikalische Elemente systematisch modelliert.

## Kerndatensatz (Was wird modelliert)
Der Kerndatensatz (CSV) besteht aus einer Liste von rund 600 auswählbarer Filmtitel aus den Jahren 1927-2010. Für jeden Film werden folgende Entitäten und Beziehungen modelliert:

* **Film:** Titel, Erscheinungsjahr, Genre
* **Schauspieler:** Beteiligung am Film, vollständige Filmographie, biografische Daten
* **Regisseur:** Regie beim Film, weitere Regiearbeiten
* **Musik/Band:** Soundtrack-Zuordnung, Bandinformationen, Alben, Titel, Genre, Mitglieder

Diese Entitäten werden durch semantische Beziehungen miteinander verknüpft (z.B. „hat Schauspieler“, „wurde inszeniert von“, „enthält Soundtrack von“, etc.).

## Datenquellen
Zur Befüllung und Validierung des Kerndatensatzes werden folgende Datenquellen verwendet:
* **Wikidata:** Triple Store für ergänzende Metadaten und biografische Informationen (https://query.wikidata.org/)
* **DBpedia:** Alternative Triple Store für ergänzende Metadaten und biografische Informationen (https://dbpedia.org/sparql/)
* **IMDb (Internet Movie Database):** Informationen zu Filmen, Schauspielern, Regisseuren und Soundtracks (https://www.imdb.com/interfaces/)
* **TMDb (The Movie Database):** Alternative Quelle für Film- und Personendaten (https://developer.themoviedb.org/docs/getting-started)
* **MusicBrainz:** REST-API für Musikmetadaten (https://musicbrainz.org/doc/MusicBrainz_API)

## Ontologie
* Verwendung der bestehenden Music Ontology `mo` (http://purl.org/ontology/mo/)
* Nutzung von `foaf` (http://xmlns.com/foaf/spec/) für Personen und Bands
* Erweiterung um eigene `fi` (Film Ontology) für film-spezifische Konzepte und Beziehungen

## Mehrwert
Einige mögliche Fragestellungen, welche durch das Projekt beantwortet werden können:

**Film:**
* Welche Schauspieler (Actor) haben im Film mitgespielt?
* Welche Filmographie hat jeder dieser Schauspieler?
* Metainformationen zum Film (Erscheinungsjahr, etc.)?
* Wer war der Regisseur des Films?
* Bei welchen anderen Filmen war dieser Regisseur im Einsatz (in dieser Rolle)? 

**Schauspieler:**
* Welche Filmographie hat jeder der im gewählten Film aktiven Schauspieler?
* Metainformationen zum Schauspieler (dob, dod, Nationalität etc.)?

**Musik / Band:**
* Welche Musik / Soundtracks gehören zum Film?
* Von welchen Bands stammen diese Soundtracks?
* Welche Alben haben diese Bands wann veröffentlicht?
* Welche Titel sind auf den einzelnen Alben?
* Welchem Genre wird die Band zugeordnet?
* Aus welchen Mitgliedern setzt sich die Band zusammen?
* Metadaten zur Band (Gründungsjahr, Herkunft etc.)?