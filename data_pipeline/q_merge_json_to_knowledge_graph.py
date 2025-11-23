# q_merge_json_to_knowledge_graph.py

import json
import os
import re
from pathlib import Path
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS, XSD, OWL

"""
This script converts JSON data into a knowledge graph in TTL-format.

It defines:
- OWL classes for the ontology (Movie, Actor, Character, BondGirl, Villain, Vehicle, Location, Song)
- Object Properties (relationships between entities)
- Data Properties (attributes with literal values)
- Individuals and their relationships

Characters appearing in less than 2 films are filtered out.
"""

def sanitize_uri_part(text):
    """
    Sanitize text to create valid URI parts
    Removes or replaces characters that are problematic in URIs
    """
    # Remove quotes and other problematic characters
    text = text.replace('"', '')
    text = text.replace("'", '')
    text = text.replace("|", '_')
    text = text.replace("/", '_')
    text = text.replace("\\", '_')
    text = text.replace(":", '_')
    text = text.replace("?", '')
    text = text.replace("#", '')
    text = text.replace("[", '')
    text = text.replace("]", '')
    text = text.replace("(", '')
    text = text.replace(")", '')
    text = text.replace("{", '')
    text = text.replace("}", '')
    text = text.replace("<", '')
    text = text.replace(">", '')
    text = text.replace(",", '_')
    # Replace spaces with underscores
    text = text.replace(" ", "_")
    # Remove multiple consecutive underscores
    text = re.sub(r'_+', '_', text)
    # Remove leading/trailing underscores
    text = text.strip('_')
    return text


def create_ttl_knowledge_graph(json_file, output_file):
    """
    Create a knowledge graph in TTL (Turtle) format from JSON data
    """

    # Define namespaces
    MOVIE = Namespace("https://triplydb.com/Triply/linkedmdb/vocab/")
    FOAF = Namespace("http://xmlns.com/foaf/0.1/")
    DBO = Namespace("http://dbpedia.org/ontology/")
    TIME = Namespace("http://www.w3.org/2006/time#")
    SCHEMA = Namespace("http://schema.org/")
    BOND = Namespace("http://example.org/bond/")
    GEO = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")

    # Initialize graph
    g = Graph()
    g.bind("movie", MOVIE)
    g.bind("foaf", FOAF)
    g.bind("dbo", DBO)
    g.bind("time", TIME)
    g.bind("schema", SCHEMA)
    g.bind("bond", BOND)
    g.bind("geo", GEO)
    g.bind("rdfs", RDFS)
    g.bind("xsd", XSD)
    g.bind("owl", OWL)

    # Load JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Count character appearances across all movies
    character_appearances = {}
    for movie_data in data['movies']:
        for character in movie_data.get('characters', []):
            char_name = character['name']
            if char_name not in character_appearances:
                character_appearances[char_name] = 0
            character_appearances[char_name] += 1

    # Filter characters with at least 2 appearances
    frequent_characters = {name for name, count in character_appearances.items() if count >= 2}
    total_chars = len(character_appearances)
    filtered_chars = len(frequent_characters)
    print(f"Character filtering: {filtered_chars} out of {total_chars} characters appear in 2+ films")


    #######################################################
    # ----- Definition of Ontology -----
    ########################################################

    # ----- 1. Define Classes -----
    g.add((MOVIE.Film, RDF.type, OWL.Class))
    g.add((MOVIE.Actor, RDF.type, OWL.Class))
    g.add((MOVIE.FilmCharacter, RDF.type, OWL.Class))
    g.add((MOVIE.FilmLocation, RDF.type, OWL.Class))
    g.add((MOVIE.MusicContributor, RDF.type, OWL.Class))
    g.add((MOVIE.Producer, RDF.type, OWL.Class))
    g.add((MOVIE.Director, RDF.type, OWL.Class))

    g.add((MOVIE.Person, RDF.type, OWL.Class))

    g.add((DBO.Song, RDF.type, OWL.Class))

    g.add((BOND.BondGirl, RDF.type, OWL.Class))
    g.add((BOND.Villain, RDF.type, OWL.Class))
    g.add((BOND.Vehicle, RDF.type, OWL.Class))

    # ----- 2. Define SubClasses -----
    # SubClasses of Person
    g.add((BOND.BondGirl, RDFS.subClassOf, MOVIE.Person))
    g.add((BOND.Villain, RDFS.subClassOf, MOVIE.Person))
    g.add((MOVIE.Actor, RDFS.subClassOf, MOVIE.Person))
    g.add((MOVIE.Producer, RDFS.subClassOf, MOVIE.Person))
    g.add((MOVIE.Director, RDFS.subClassOf, MOVIE.Person))
    g.add((MOVIE.MusicContributor, RDFS.subClassOf, MOVIE.Person))

    # SubClasses of FilmCharacter
    g.add((BOND.BondGirl, RDFS.subClassOf, MOVIE.FilmCharacter))
    g.add((BOND.Villain, RDFS.subClassOf, MOVIE.FilmCharacter))

    # ----- 3: Define Object Properties (relationships between individuals)
    
    # Film -> Actor: hasActor | Person -> Film: appearsIn (transitive)
    g.add((BOND.hasActor, RDF.type, OWL.ObjectProperty))
    g.add((BOND.hasActor, RDFS.domain, MOVIE.Film))
    g.add((BOND.hasActor, RDFS.range, MOVIE.Actor))
    g.add((BOND.hasActor, OWL.inverseOf, BOND.appearsIn))
    g.add((BOND.appearsIn, RDF.type, OWL.ObjectProperty))
    g.add((BOND.appearsIn, RDF.type, OWL.TransitiveProperty))  # must be transitive to BondGirl, Villain, Actor, Director, etc.
    g.add((BOND.appearsIn, RDFS.domain, MOVIE.Person))
    g.add((BOND.appearsIn, RDFS.range, MOVIE.Film))

    # Actor -> Character: portrayedBy | Character -> Actor: portrayedByInverse
    g.add((BOND.portrayedBy, RDF.type, OWL.ObjectProperty))
    g.add((BOND.portrayedBy, RDFS.domain, MOVIE.FilmCharacter))
    g.add((BOND.portrayedBy, RDFS.range, MOVIE.Actor))
    g.add((BOND.portrayedBy, OWL.inverseOf, BOND.portrayedByInverse))
    g.add((BOND.portrayedByInverse, RDF.type, OWL.ObjectProperty))
    g.add((BOND.portrayedByInverse, RDFS.domain, MOVIE.Actor))
    g.add((BOND.portrayedByInverse, RDFS.range, MOVIE.FilmCharacter))

    # Film -> Villain: hasAntagonist
    g.add((BOND.hasAntagonist, RDF.type, OWL.ObjectProperty))
    g.add((BOND.hasAntagonist, RDFS.domain, MOVIE.Film))
    g.add((BOND.hasAntagonist, RDFS.range, BOND.Villain))
    g.add((BOND.hasAntagonist, OWL.inverseOf, BOND.appearsIn))

    # Film -> BondGirl: hasBondGirl
    g.add((BOND.hasBondGirl, RDF.type, OWL.ObjectProperty))
    g.add((BOND.hasBondGirl, RDFS.domain, MOVIE.Film))
    g.add((BOND.hasBondGirl, RDFS.range, BOND.BondGirl))
    g.add((BOND.hasBondGirl, OWL.inverseOf, BOND.appearsIn))

    # Film -> Director: hasDirector
    g.add((BOND.hasDirector, RDF.type, OWL.ObjectProperty))
    g.add((BOND.hasDirector, RDFS.domain, MOVIE.Film))
    g.add((BOND.hasDirector, RDFS.range, MOVIE.Director))
    g.add((BOND.hasDirector, OWL.inverseOf, BOND.appearsIn))

    # Film -> Producer: hasProducer
    g.add((BOND.hasProducer, RDF.type, OWL.ObjectProperty))
    g.add((BOND.hasProducer, RDFS.domain, MOVIE.Film))
    g.add((BOND.hasProducer, RDFS.range, MOVIE.Producer))
    g.add((BOND.hasProducer, OWL.inverseOf, BOND.appearsIn))

    # Film -> Location: hasLocation | Location -> Film: filmedIn
    g.add((BOND.hasLocation, RDF.type, OWL.ObjectProperty))
    g.add((BOND.hasLocation, RDFS.domain, MOVIE.Film))
    g.add((BOND.hasLocation, RDFS.range, MOVIE.FilmLocation))
    g.add((BOND.hasLocation, OWL.inverseOf, BOND.filmedIn))
    g.add((BOND.filmedIn, RDF.type, OWL.ObjectProperty))
    g.add((BOND.filmedIn, RDFS.domain, MOVIE.FilmLocation))
    g.add((BOND.filmedIn, RDFS.range, MOVIE.Film))

    # Film -> Song: hasThemeSong | Song -> Film: isThemeSongOf
    g.add((BOND.hasThemeSong, RDF.type, OWL.ObjectProperty))
    g.add((BOND.hasThemeSong, RDFS.domain, MOVIE.Film))
    g.add((BOND.hasThemeSong, RDFS.range, DBO.Song))
    g.add((BOND.hasThemeSong, OWL.inverseOf, BOND.isThemeSongOf))
    g.add((BOND.isThemeSongOf, RDF.type, OWL.ObjectProperty))
    g.add((BOND.isThemeSongOf, RDFS.domain, DBO.Song))
    g.add((BOND.isThemeSongOf, RDFS.range, MOVIE.Film))

    # Film -> MusicContributor: hasMusicContributor | MusicContributor -> Film: contributedTo
    g.add((BOND.hasMusicContributor, RDF.type, OWL.ObjectProperty))
    g.add((BOND.hasMusicContributor, RDFS.domain, MOVIE.Film))
    g.add((BOND.hasMusicContributor, RDFS.range, MOVIE.MusicContributor))
    g.add((BOND.hasMusicContributor, OWL.inverseOf, BOND.contributedTo))
    g.add((BOND.contributedTo, RDF.type, OWL.ObjectProperty))
    g.add((BOND.contributedTo, RDFS.domain, MOVIE.MusicContributor))
    g.add((BOND.contributedTo, RDFS.range, MOVIE.Film))

    # ThemeSong -> MusicContributor: isPerformedBy | MusicContributor -> ThemeSong: performedThemeSong
    g.add((BOND.isPerformedBy, RDF.type, OWL.ObjectProperty))
    g.add((BOND.isPerformedBy, RDFS.domain, DBO.Song))
    g.add((BOND.isPerformedBy, RDFS.range, MOVIE.MusicContributor))
    g.add((BOND.isPerformedBy, OWL.inverseOf, BOND.performedThemeSong))
    g.add((BOND.performedThemeSong, RDF.type, OWL.ObjectProperty))
    g.add((BOND.performedThemeSong, RDFS.domain, MOVIE.MusicContributor))
    g.add((BOND.performedThemeSong, RDFS.range, DBO.Song))

    # Film -> Vehicle: hasVehicle | Vehicle -> Film: featuredIn
    g.add((BOND.hasVehicle, RDF.type, OWL.ObjectProperty))
    g.add((BOND.hasVehicle, RDFS.domain, MOVIE.Film))
    g.add((BOND.hasVehicle, RDFS.range, BOND.Vehicle))
    g.add((BOND.hasVehicle, OWL.inverseOf, BOND.featuredIn))
    g.add((BOND.featuredIn, RDF.type, OWL.ObjectProperty))
    g.add((BOND.featuredIn, RDFS.domain, BOND.Vehicle))
    g.add((BOND.featuredIn, RDFS.range, MOVIE.Film))

    # ----- 4: Define Data Properties (attributes with literal values) -----

    g.add((RDFS.label, RDF.type, OWL.DatatypeProperty))
    g.add((RDFS.label, RDFS.range, XSD.string))

    g.add((SCHEMA.name, RDF.type, OWL.DatatypeProperty))
    g.add((SCHEMA.name, RDFS.domain, MOVIE.Film))
    g.add((SCHEMA.name, RDFS.range, XSD.string))

    g.add((FOAF.name, RDF.type, OWL.DatatypeProperty))
    g.add((FOAF.name, RDFS.domain, MOVIE.Person))
    g.add((FOAF.name, RDFS.range, XSD.string))

    g.add((FOAF.gender, RDF.type, OWL.DatatypeProperty))
    g.add((FOAF.gender, RDFS.domain, MOVIE.Person))
    g.add((FOAF.gender, RDFS.range, XSD.string))

    g.add((SCHEMA.image, RDF.type, OWL.DatatypeProperty))
    g.add((SCHEMA.image, RDFS.range, XSD.anyURI))

    g.add((SCHEMA.url, RDF.type, OWL.DatatypeProperty))
    g.add((SCHEMA.url, RDFS.domain, DBO.Song))
    g.add((SCHEMA.url, RDFS.range, XSD.anyURI))

    g.add((GEO.lat, RDF.type, OWL.DatatypeProperty))
    g.add((GEO.lat, RDFS.domain, MOVIE.FilmLocation))
    g.add((GEO.lat, RDFS.range, XSD.decimal))

    g.add((GEO.long, RDF.type, OWL.DatatypeProperty))
    g.add((GEO.long, RDFS.domain, MOVIE.FilmLocation))
    g.add((GEO.long, RDFS.range, XSD.decimal))

    g.add((TIME.year, RDF.type, OWL.DatatypeProperty))
    g.add((TIME.year, RDFS.domain, MOVIE.Film))
    g.add((TIME.year, RDFS.range, XSD.gYear))

    g.add((BOND.imdbRating, RDF.type, OWL.DatatypeProperty))
    g.add((BOND.imdbRating, RDFS.domain, MOVIE.Film))
    g.add((BOND.imdbRating, RDFS.range, XSD.decimal))

    g.add((BOND.rtmRating, RDF.type, OWL.DatatypeProperty))
    g.add((BOND.rtmRating, RDFS.domain, MOVIE.Film))
    g.add((BOND.rtmRating, RDFS.range, XSD.decimal))

    #######################################################
    # Create Triples for each Movie and its Entities
    ########################################################

    for movie_data in data['movies']:
        movie_title = movie_data['title_en']
        movie_uri_safe = sanitize_uri_part(movie_title)
        movie_uri = BOND[movie_uri_safe]

        # Create movie node
        g.add((movie_uri, RDF.type, MOVIE.Film))
        g.add((movie_uri, RDFS.label, Literal(movie_title, lang='en')))
        g.add((movie_uri, SCHEMA.name, Literal(movie_title)))

        # Add German title if available
        if 'title_de' in movie_data and movie_data['title_de']:
            g.add((movie_uri, RDFS.label, Literal(movie_data['title_de'], lang='de')))

        # Add Release Year
        if 'year' in movie_data and movie_data['year']:
            g.add((movie_uri, TIME.year, Literal(movie_data['year'], datatype=XSD.gYear)))

        # Add Ratings
        if 'imdb_rating' in movie_data and movie_data['imdb_rating']:
            try:
                rating = float(movie_data['imdb_rating'])
                g.add((movie_uri, BOND.imdbRating, Literal(rating, datatype=XSD.decimal)))
            except (ValueError, TypeError):
                pass

        if 'rotten_tomatoes_rating' in movie_data and movie_data['rotten_tomatoes_rating']:
            try:
                rating = float(movie_data['rotten_tomatoes_rating'])
                g.add((movie_uri, BOND.rtmRating, Literal(rating, datatype=XSD.decimal)))
            except (ValueError, TypeError):
                pass

        # Add Director
        if 'director' in movie_data and movie_data['director']:
            director_name = movie_data['director']
            director_uri_safe = sanitize_uri_part(director_name)
            director_uri = BOND[director_uri_safe]
            
            g.add((director_uri, RDF.type, MOVIE.Director))
            g.add((director_uri, FOAF.name, Literal(director_name)))
            g.add((movie_uri, BOND.hasDirector, director_uri))
            g.add((director_uri, BOND.appearsIn, movie_uri))

        # Add Producer
        if 'producer' in movie_data and movie_data['producer']:
            producer_name = movie_data['producer']
            producer_uri_safe = sanitize_uri_part(producer_name)
            producer_uri = BOND[producer_uri_safe]
            
            g.add((producer_uri, RDF.type, MOVIE.Producer))
            g.add((producer_uri, FOAF.name, Literal(producer_name)))
            g.add((movie_uri, BOND.hasProducer, producer_uri))
            g.add((producer_uri, BOND.appearsIn, movie_uri))

        # Process Bond Girls
        for bond_girl in movie_data.get('bond_girls', []):
            girl_name = bond_girl['name']
            actress_name = bond_girl['actress']

            # Create bond girl character URI
            girl_uri_safe = sanitize_uri_part(girl_name)
            girl_uri = BOND[girl_uri_safe]

            # Create actress URI
            actress_uri_safe = sanitize_uri_part(actress_name)
            actress_uri = BOND[actress_uri_safe]

            # Add triples
            g.add((girl_uri, RDF.type, BOND.BondGirl))
            g.add((girl_uri, FOAF.name, Literal(girl_name)))
            g.add((girl_uri, BOND.appearsIn, movie_uri))
            g.add((girl_uri, BOND.portrayedBy, actress_uri))
            g.add((actress_uri, RDF.type, MOVIE.Actor))
            g.add((actress_uri, FOAF.name, Literal(actress_name)))

            if bond_girl.get('image_url'):
                g.add((girl_uri, SCHEMA.image, Literal(bond_girl['image_url'])))

        # Process Villains
        for villain in movie_data.get('villains', []):
            villain_name = villain['name']
            actor_name = villain['actor']

            # Create villain character URI
            villain_uri_safe = sanitize_uri_part(villain_name)
            villain_uri = BOND[villain_uri_safe]

            # Create actor URI
            actor_uri_safe = sanitize_uri_part(actor_name)
            actor_uri = BOND[actor_uri_safe]

            # Add triples
            g.add((villain_uri, RDF.type, BOND.Villain))
            g.add((villain_uri, FOAF.name, Literal(villain_name)))
            g.add((villain_uri, BOND.appearsIn, movie_uri))
            g.add((villain_uri, BOND.portrayedBy, actor_uri))
            g.add((actor_uri, RDF.type, MOVIE.Actor))
            g.add((actor_uri, FOAF.name, Literal(actor_name)))

            if villain.get('image_url'):
                g.add((villain_uri, SCHEMA.image, Literal(villain['image_url'])))

        # Process Characters (other than bond girls and villains)
        # Only include characters that appear in at least 2 films
        for character in movie_data.get('characters', []):
            char_name = character['name']

            # Skip characters that appear in less than 2 films
            if char_name not in frequent_characters:
                continue

            actor_name = character['actor']

            # Create character URI
            char_uri_safe = sanitize_uri_part(char_name)
            char_uri = BOND[char_uri_safe]

            # Create actor URI
            actor_uri_safe = sanitize_uri_part(actor_name)
            actor_uri = BOND[actor_uri_safe]

            # Add triples
            g.add((char_uri, RDF.type, MOVIE.Person))
            g.add((char_uri, FOAF.name, Literal(char_name)))
            g.add((char_uri, BOND.appearsIn, movie_uri))
            g.add((char_uri, BOND.portrayedBy, actor_uri))
            g.add((actor_uri, RDF.type, MOVIE.Actor))
            g.add((actor_uri, FOAF.name, Literal(actor_name)))

            if character.get('image_url'):
                g.add((char_uri, SCHEMA.image, Literal(character['image_url'])))

        # Process Locations
        for location in movie_data.get('locations', []):
            loc_name = location['name']
            loc_uri_safe = sanitize_uri_part(loc_name)
            loc_uri = BOND[loc_uri_safe]

            g.add((loc_uri, RDF.type, MOVIE.FilmLocation))
            g.add((loc_uri, RDFS.label, Literal(loc_name)))
            g.add((movie_uri, BOND.hasLocation, loc_uri))
            g.add((loc_uri, BOND.filmedIn, movie_uri))

            if location.get('latitude'):
                g.add((loc_uri, GEO.lat, Literal(float(location['latitude']), datatype=XSD.decimal)))
            if location.get('longitude'):
                g.add((loc_uri, GEO.long, Literal(float(location['longitude']), datatype=XSD.decimal)))

        # Process ThemeSongs
        for song in movie_data.get('songs', []):
            song_title = song['title']
            song_uri_safe = sanitize_uri_part(song_title)
            song_uri = BOND[song_uri_safe]

            g.add((song_uri, RDF.type, DBO.Song))
            g.add((song_uri, RDFS.label, Literal(song_title)))
            g.add((movie_uri, BOND.hasThemeSong, song_uri))
            g.add((song_uri, BOND.isThemeSongOf, movie_uri))

            # Create MusicContributor entity if performer exists
            if song.get('performer'):
                performer_name = song['performer']
                performer_uri_safe = sanitize_uri_part(performer_name)
                performer_uri = BOND[performer_uri_safe]
                
                g.add((performer_uri, RDF.type, MOVIE.MusicContributor))
                g.add((performer_uri, FOAF.name, Literal(performer_name)))
                g.add((song_uri, BOND.isPerformedBy, performer_uri))
                g.add((movie_uri, BOND.hasMusicContributor, performer_uri))

            if song.get('youtube_link'):
                g.add((song_uri, SCHEMA.url, Literal(song['youtube_link'])))

        # Process Vehicles
        for vehicle in movie_data.get('vehicles', []):
            vehicle_name = vehicle['name']
            vehicle_uri_safe = sanitize_uri_part(vehicle_name)
            vehicle_uri = BOND[vehicle_uri_safe]

            g.add((vehicle_uri, RDF.type, BOND.Vehicle))
            g.add((vehicle_uri, RDFS.label, Literal(vehicle_name)))
            g.add((movie_uri, BOND.hasVehicle, vehicle_uri))
            g.add((vehicle_uri, BOND.featuredIn, movie_uri))

            if vehicle.get('image_url'):
                g.add((vehicle_uri, SCHEMA.image, Literal(vehicle['image_url'])))

    # Serialize to TTL
    print(f"Serializing {len(g)} triples to Turtle format...")
    turtle_output = g.serialize(format="turtle")

    # Write to file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(turtle_output)

    print(f"TTL file created: {output_file}")
    print(f"Total triples: {len(g)}")

    return g


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent

    json_input = base_dir / "data/triple_store/james_bond_knowledge.json"
    ttl_output = base_dir / "data/triple_store/james_bond_knowledge.ttl"

    graph = create_ttl_knowledge_graph(json_input, ttl_output)

    print(f"JSON input: {json_input}")
    print(f"TTL output: {ttl_output}")
    print(f"Total triples: {len(graph)}")