# Mjolnir
from src.services.artist import ArtistService
from .stubs import stub_artist_validated

# Third party
from pytest import fixture


@fixture(scope='function')
def setup_artist_service():
    artist_service = ArtistService(artist_validated=stub_artist_validated)
    return artist_service
