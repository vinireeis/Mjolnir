# Mjolnir
# from ..domain.exceptions import NotFoundArtistId
from src.domain.exceptions import NotFoundArtistId

# Standards
from http import HTTPStatus

# Third party
from decouple import config
from loguru import logger
import httpx


class MusicApi:

    @staticmethod
    async def get_ten_most_popular_musics_on_genius(artist_id: int) -> dict:
        async with httpx.AsyncClient() as client:
            request_response = await client.get(
                f"https://{config('GENIUS_API_BASE_URL')}/artists/{artist_id}/songs",
                headers={
                    "Accept": "application/json",
                    "Host": config('GENIUS_API_BASE_URL'),
                    "Authorization": f"Bearer {config('GENIUS_CLIENT_ACCESS_TOKEN')}"
                },
                params={
                    "sort": "popularity",
                    "per_page": config("MUSICS_PER_PAGE")
                }
            )
        await MusicApi.__result_map_from_request_response(request_response=request_response)
        ten_most_popular_musics = request_response.json()
        return ten_most_popular_musics

    @staticmethod
    async def __result_map_from_request_response(request_response: httpx.Response):
        response_map = {
            HTTPStatus.INTERNAL_SERVER_ERROR: MusicApi.__raise_internal_server_error,
            HTTPStatus.BAD_REQUEST: MusicApi.__raise_bad_request,
            HTTPStatus.NOT_FOUND: MusicApi.__raise_not_found,
            HTTPStatus.OK: lambda: True,
        }
        status_code = request_response.status_code
        result = response_map.get(status_code, MusicApi.__raise_internal_server_error)
        return result()

    @staticmethod
    def __raise_internal_server_error():
        logger.error("Error on api partners")
        raise Exception

    @staticmethod
    def __raise_bad_request():
        logger.info("Error on get songs, invalid params")
        raise ValueError

    @staticmethod
    def __raise_not_found():
        logger.info("No found any artist with this ID")
        raise NotFoundArtistId

# import asyncio
# from pprint import pprint
# pprint(asyncio.run(MusicApi.get_ten_most_popular_musics_on_genius(357)))
