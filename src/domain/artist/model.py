from uuid import uuid4
from loguru import logger


class ArtistModel:

    def __init__(self, songs_result_from_genius: dict, artist_id: int):
        self.artist_id = artist_id
        self.songs = songs_result_from_genius.get("response", {}).get("songs", [])
        self.transaction_id = str(uuid4())

    async def _get_artist_name(self, song) -> str:
        artist_name = await self._get_artist_name_from_feature_artist(song=song)
        if not artist_name:
            artist_name = song.get("primary_artist").get("name")
        return artist_name

    async def _get_artist_name_from_feature_artist(self, song):
        featured_artists = song.get("featured_artists", [])
        if featured_artists:
            name = [
                artist.get("name")
                for artist in featured_artists
                if artist.get("id") == self.artist_id
            ]
            name = name[0] if name else []
            return name
        return []

    async def _get_first_artist_name(self):
        song = self.songs[0]
        artist_name = await self._get_artist_name(song=song)
        return artist_name

    async def get_songs_result_template(self) -> dict:
        songs_treated_template = {"top_ten_songs": []}
        try:
            for song in self.songs:
                song_treated = dict()
                song_treated.update(artist_name=await self._get_artist_name(song=song))
                song_treated.update(title=song.get("title"))
                song_treated.update(full_title=str(song.get("full_title").replace("\xa0", " ")))
                song_treated.update(url_song=song.get("url"))
                song_treated.update(release_date=song.get("release_date_for_display"))
                song_treated.update(song_art_image_url=song.get("song_art_image_url"))

                songs_treated_template.get("top_ten_songs").append(song_treated)

            return songs_treated_template

        except Exception as ex:
            logger.error(
                ex=ex,
                __message="ArtistModel::get_songs_result_template::Error on create result"
                " songs template",
            )
            raise ex

    async def get_dynamo_template(self) -> dict:
        songs_template_to_save_in_dynamo = {
            "transaction_id": self.transaction_id,
            "artist_name": await self._get_first_artist_name(),
            "artist_id": self.artist_id,
        }
        return songs_template_to_save_in_dynamo
