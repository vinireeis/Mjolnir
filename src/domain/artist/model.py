from uuid import uuid4
from loguru import logger


class ArtistModel:
    def __init__(self, songs_result_from_genius: dict, artist_id: int):
        self.artist_id = artist_id
        self.songs = songs_result_from_genius.get("response", {}).get("songs", [])
        self.artist_name = self._get_artist_name()
        self.transaction_id = uuid4()

    def _get_artist_name(self) -> str:
        try:
            song = self.songs[0]
            the_same_artist = song.get("primary_artist", {}).get("id", False) == self.artist_id
            if the_same_artist:
                artist_name = song.get("primary_artist").get("name")
                return artist_name
            featured_artists = song.get("featured_artists", {})
            name = [artist.get("name") for artist in featured_artists if artist.get("id") == self.artist_id]
            return name[0]
        except Exception as ex:
            logger.error(ex=ex, __message="ArtistModel::_get_artist_name::Error when trying to get artist name")
            raise ex

    async def get_songs_result_template(self) -> dict:
        songs_treated_template = {
            "artist_name": self.artist_name,
            "top_ten_songs": [
            ]
        }
        try:
            for song in self.songs:
                song_treated = dict()
                song_treated.update(title=song.get("title"))
                song_treated.update(full_title=str(song.get("full_title").replace("\xa0", " ")))
                song_treated.update(url_song=song.get("url"))
                song_treated.update(release_date=song.get("release_date_for_display"))
                song_treated.update(song_art_image_url=song.get("song_art_image_url"))

                songs_treated_template.get("top_ten_songs").append(song_treated)

            return songs_treated_template
        except Exception as ex:
            logger.error(ex=ex, __message="ArtistModel::get_songs_result_template::Error on create result"
                                          " songs template")
            raise ex

    async def get_dynamo_template(self) -> dict:
        songs_template_to_save_in_dynamo = {
            "id_transaction": self.transaction_id,
            "artist_name": self.artist_name,
            "artist_id": self.artist_id,
        }
        return songs_template_to_save_in_dynamo

# from src.domain.artist.example import songs_result2, example2
# import asyncio
# from pprint import pprint
# model = asyncio.run(ArtistModel(songs_result=example2, artist_id=357).get_songs_result_template())
# pprint(model)
