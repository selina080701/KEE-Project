# KEE-Project: Filmnetzwerk-Analyse
Knowledge Engineering and Extraction | MSc-DV | HS25 

GruppenmitgliederInnen:
* Selina Steiner
* Tamara Nyffeler

## Ausgangslage und Aufgabenstellung
Informationen zu Filmen, Schauspielern und Regisseuren sind im Internet auf zahlreiche Plattformen zu finden. Dieses Projekt untersucht die erfolgreichsten Filme der `IMDb Top 250`-Liste und analysiert die Netzwerkstrukturen zwischen Regisseuren und Schauspielern. Durch die Integration von strukturierten Daten (IMDb-Ratings, Wikidata) und unstrukturierten Textquellen (Filmkritiken) wird ein Knowledge Graph erstellt. Dieser ermöglicht es, Muster erfolgreicher Zusammenarbeiten zu identifizieren. 

## Kerndatensatz (Was wird modelliert)
Als Ausgangslage dient ein Kerndatensatz (CSV), der die [250 bestbewerteten Filmtitel von IMDb](https://www.kaggle.com/datasets/rajugc/imdb-top-250-movies-dataset) beinhaltet. Für jeden Film sind folgende Attribute vorhanden:

* **rank:** Rang des Films in der Top 250 Liste
* **name:** Titel des Films
* **year:** Erscheinungsjahr
* **genre:** Klassifizierte Genre
* **directors:** Regisseure
* **budget:** Budget des Films
* **rating:** IMDb-Bewertung

Diese Entitäten werden durch semantische Beziehungen miteinander verknüpft (z.B. „hat Schauspieler“, „hatBewertung“, „hatRegisseur“).

## Datenquellen
* **Wikidata**: Triple Store für Ergänzungen zu Schauspielern
* **Filmkritiken**: Unstrukturierte Textdaten von Plattformen wie `Rotten Tomatoes` oder `IMDb` zur qualitativen Analyse

## Ontologie
* Verwendung von `schema.org` (https://schema.org/Movie) als Basis-Ontologie für Filme, Personen und Bewertungen
* Erweiterung um eigene Ontologie bei Bedarf

## Mehrwert
Die Beantwortung der Fragestellung: Gibt es wiederkehrende Kollaborationen zwischen Regisseuren und Schauspielern in hochbewerteten Filmen, und wie werden diese Partnerschaften in Filmkritiken qualitativ bewertet ("Erfolgsrezepte")?