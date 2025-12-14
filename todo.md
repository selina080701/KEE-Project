# Knowledge Engineering Workflow
1. [x] Hintergrundwissen formalisieren, das für die Wissensgewinnung verwendet wird:
   - [x] Kerndatensatz als Ausgangslage: Raw-Datensatz auf relevante Eigenschaften reduzieren.

2. [x] James Bond 007: No Time to Die im Kerndatensatz hinzufügen (händisch).

3. [x] RDF-Domänenmodell bereitstellen:
   - [x] RDF-Graph Skizze in Excalidraw (Beispiel Casino Royale)
   - [x] RDF-Graph serialisieren (ttl-Format)
   - [x] RDF-Graph visualisieren (streamlit)
   - [x] RDF-Graph neu generieren: Wenn neue Triples vorhanden sind (zb. „hat Ort“, „hat Auto“, „hat Antagonisten“)
4. [x] Hinzufügen einer Ontologie, um das Modell zu beschreiben und Schlussfolgerungen zu ermöglichen:
   - [x] Ontologie in Protegé & Python (owlready2) testen

----

# Knowledge Extraction Workflow
1. [x] Filmliste erstellen: Kerndatensatz mit Wikidata-ID erweitern.

2. [x] Externe strukturierte Daten abrufen (Wikidata SPARQL)
   - [x] Deutsche Film-Titel hinzufügen
   - [x] Schauspieler Info: dob, dod, country origin, etc.

3. [x] Unstrukturierte Texte extrahieren (Fandom):
   - [x] Filmseiten auf Fandom über `wikitextparser` parsen und als JSON speichern
   - [x] Benötigte Elemente aus dem Text extrahieren
   - [x] NLP-Analyse:
     - Named Entity Recognition (zb. mit spaCy)
     - Erkennung und Klassifikation von Entitäten (Ort, Person, Objekt)

----

# Visualization
1. [x] Framework der Streamlit-App erstellen

2. [x] Titelpage:
   - [x] Übersicht / Intro gestalten
   - [x] Kerndatensatz-Tabelle einfügen
   - [x] deutsche Titel ergänzen
   - [x] Suchfunktion für Filme     
   - [x] Filmposter einfügen

3. [x] RDF-Graph
   - [x] RDF-Graph visualisieren (streamlit)
   - [x] RDF-Graph mit neuen Triples aktualisieren

4. [x] Recurring Characters Page

5. [x] Image Galleries:
   - [x] Autos Übersichtseite
   - [x] Bond Girls Übersichtseite
   - [x] Villains Übersichtseite

5. [x] Interactive Map 