from ..domain.artist.model import ArtistModel
from ..repositories.redis.repository import RedisRepository
from ..transports.genius import MusicApi


class ArtistService:
    def __init__(self, artist_validated):
        self.artist_id = artist_validated.get("artist_id")
        self.artist_id_to_string = str(artist_validated.get("artist_id"))
        self.cache = artist_validated.get("cache")

    async def get_ten_most_popular_songs(self):
        if self.cache:
            songs_treated_template = await self._get_or_set_artist_songs_on_redis()
            return songs_treated_template
        songs_treated_template = await self._clean_up_redis_and_save_on_dynamo()
        return songs_treated_template

    async def _get_or_set_artist_songs_on_redis(self):
        result = await RedisRepository.get(key=self.artist_id_to_string)
        if result:
            result = eval(result.decode())
            return result
        songs_result_from_genius = await MusicApi.get_ten_most_popular_musics_on_genius(artist_id=self.artist_id)
        artist_model = ArtistModel(songs_result_from_genius=songs_result_from_genius, artist_id=self.artist_id)
        # TODO: salvar no dynamoDB
        songs_treated_template = await artist_model.get_songs_result_template()
        await RedisRepository.set(key=self.artist_id_to_string, value=str(songs_treated_template))
        return songs_treated_template

    async def _clean_up_redis_and_save_on_dynamo(self):
        await RedisRepository.delete(key=self.artist_id_to_string)
        songs_result_from_genius = await MusicApi.get_ten_most_popular_musics_on_genius(artist_id=self.artist_id)
        artist_model = ArtistModel(songs_result_from_genius=songs_result_from_genius, artist_id=self.artist_id)
        # TODO: update dynamo with new result
        songs_treated_template = await artist_model.get_songs_result_template()
        return songs_treated_template
