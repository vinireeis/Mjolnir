from ..domain.artist.model import ArtistModel
from ..transports.genius import MusicApi

class ArtistService:
    def __init__(self, artist_validated):
        self.artist_id = artist_validated.get("artist_id")
        self.cache = artist_validated.get("cache")

    async def get_ten_most_popular_songs(self):
        songs_result = await MusicApi.get_ten_most_popular_musics_on_genius(artist_id=self.artist_id)
        songs_result_treated = ArtistModel(songs_result=songs_result).get_songs_template()


        pass
