# page_config.py
from pages.intro_page import show_intro_page
from pages.movie_page import show_movie_page
from pages.rdf_page import show_rdf_page
from pages.characters_page import show_characters_page
from pages.image_gallery_page import show_image_gallery_page
from pages.map_page import show_map_page

PAGE_CONFIG = {
    "▶️ Introduction": show_intro_page,
    "🎬 Movie Collection": show_movie_page,
    "🔗 RDF-Graph": show_rdf_page,
    "👥 Recurring Characters": show_characters_page,
    "📷 Image Collection": show_image_gallery_page,
    "🌍 Film Locations": show_map_page
}