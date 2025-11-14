# 3. Statusupdate - Fr, 21.11.2025
**Done**:

**Obstacles**:


**Whats Next**:

----

# 2. Statusupdate - Fr, 14.11.2025
**Done**:
- Code-Struktur für Streamlit-App aufgebaut
- Titelseite mit Kerndatensatz und Suchfunktion erstellt
- Movie-Pages von Fandom geparst und als JSON gespeichert
- Poster URLs extrahiert und in Übersichtstabelle eingebettet (Thumbnail-View oder Poster-Ansicht umschaltbar)
- Erster Versuch mit NER auf Fandom-Texten gestartet (spaCy) -> Locations extrahiert und in Map visualisiert

**Obstacles**:
- [fixed] Problem beim Einbetten der Poster-URL. URL funktioniert aber Bild-Thumbnail wurde nicht angezeigt.
   - Lösung: '/revision/latest' aus der URL entfernt.
- [Frage] Abschlussbericht in Overleaf - gibt es eine Vorlage?

**Whats Next**:
- Wikidata-Triples extrahieren -> deutsche Filmtitel, Schauspieler Metadaten
- NLP-Analyse der Fandom-Seiten durchführen -> Autos, Antagonisten, Bondgirls extrahieren
- Ontologie und Reasoning mit Restrictions

----


# 1. Statusupdate - Fr, 07.11.2025
**Done**:
- Kerndatensatz mit Wikidata-IDs erweitert (über Sparql)
- RDF-Beispiel für Casino Royale erstellt
- Ontologie-Design erstellt (Excalidraw)
- RDF-Triples für alle Filme generiert (ohne No Time to Die)
- RDF-Graph mit Streamlit visualisiert
- Template Streamlit-App erstellt

**Whats Next**:
- Wikidata-Triples extrahieren
- Unstrukturierte Daten extrahieren (Fandom)
- Ontologie und Reasoning mit Restrictions

**Tips & Inputs**:
- Bei der Ontologie wo möglich das Vokabular von `LinkedMDb` verwenden (Endppoint zwar nicht mehr online, aber Vokabular müsste noch dokumentiert sein).
- Trailer einbetten oder z.B. auch Filmposter als Bild einfügen.
- Neuster Bond-Film "No Time to Die" kann manuell hinzugefügt werden (braucht keinen overkill).

----

# Knowledge Engineering Workflow
1. [x] Hintergrundwissen formalisieren, das für die Wissensgewinnung verwendet wird:
   - [x] Kerndatensatz als Ausgangslage: Raw-Datensatz auf relevante Eigenschaften reduzieren.

2. [x] James Bond 007: No Time to Die im Kerndatensatz hinzufügen (händisch).

3. [] RDF-Domänenmodell bereitstellen:
   - [x] RDF-Graph Skizze in Excalidraw (Beispiel Casino Royale)
   - [x] RDF-Graph serialisieren (ttl-Format)
   - [x] RDF-Graph visualisieren (streamlit)
   - [] RDF-Graph neu generieren: Wenn neue Triples vorhanden sind (zb. „hat Ort“, „hat Auto“, „hat Antagonisten“)
4. [] Hinzufügen einer Ontologie, um das Modell zu beschreiben und Schlussfolgerungen zu ermöglichen:
   - [] Ontologie in Protegé erstellen
   - [] Reasoning-Regeln für wiederkehrende Locations, Charaktere, Autos, etc. 

----

# Knowledge Extraction Workflow
1. [x] Filmliste erstellen: Kerndatensatz mit Wikidata-ID erweitern.

2. [] Externe strukturierte Daten abrufen (Wikidata SPARQL)

3. [] Unstrukturierte Texte extrahieren (Fandom):
   - [x] Filmseiten auf Fandom über `wikitextparser` parsen und als JSON speichern
   - [] Benötigte Elemente aus dem Text extrahieren
   - [] NLP-Analyse:
     - Named Entity Recognition (zb. mit spaCy)
     - Erkennung und Klassifikation von Entitäten (Ort, Person, Objekt)

----

# Visualization
1. [x]Framework der Streamlit-App erstellen

2. [] Titelpage:
   - [x] Übersicht / Intro gestalten
   - [x] Kerndatensatz-Tabelle einfügen
   - [x] Suchfunktion für Filme     
   - [x] Filmposter einfügen

3. [] RDF-Graph

4. [] Timeline

5. [] Interactive Map 

6. [] Trailer einbetten

