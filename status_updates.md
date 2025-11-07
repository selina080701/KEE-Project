# 1. Statusupdate - Fr, 07.11.2025
**Done**:
- Kerndatensatz mit Wikidata-IDs erweitert (über Sparql)
- RDF-Beispiel für Casino Royale erstellt
- Ontologie-Design erstellt
- RDF-Triples für alle Filme generiert (ohne No Time to Die)
- RDF-Graph mit Streamlit visualisiert
- Template Streamlit-App erstellt

**Whats Next**:
- Wikidata-Triples extrahieren
- Unstrukturierte Daten extrahieren (Fandom)

**Varia**:
- Bei der Ontologie wo möglich das Vokabular von `LinkedMDb` verwenden (Endppoint zwar nicht mehr online, aber Vokabular müsste noch dokumentiert sein)

----

# Knowledge Extraction Workflow
[x] 1. Filmliste erstellen: CSV mit Titel, Jahr, Bond-Darsteller, Wikidata-ID etc.

[] 2. James Bond 007: No Time to Die im CSV hinzufügen

[] 3. Externe strukturierte Daten abrufen (Wikidata SPARQL)

[] 4. Unstrukturierte Texte extrahieren (Fandom)

[] 5. NLP-Analyse:
   - Named Entity Recognition (zb. mit spaCy)
   - Erkennung und Klassifikation von Entitäten (Ort, Person, Objekt)

[] 6. RDF-Generierung: neue Triples (zb. „hat Ort“, „hat Auto“, „hat Antagonisten“)

[] 7. Integration in Triple Store: Zusammenführung aller Daten zu einem semantischen Wissensgraphen

