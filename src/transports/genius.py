# Standards
from http import HTTPStatus

# Third party
from decouple import config
import httpx


class MusicApi:

    @staticmethod
    async def get_ten_most_popular_musics(artist_id: int) -> dict:
        async with httpx.AsyncClient() as client:
            request_response = await client.get(
                f"https://api.genius.com/artists/{artist_id}/songs",
                headers={
                    "Accept": "application/json",
                    "Host": "api.genius.com",
                    "Authorization": f"Bearer {config('GENIUS_CLIENT_ACCESS_TOKEN')}"
                },
                params={
                    "sort": "popularity",
                    "per_page": 10
                }
            )

        print(type(request_response))
        await MusicApi.__result_map_from_request_response(request_response=request_response)
        ten_most_popular_musics = request_response.json()
        return ten_most_popular_musics

    @staticmethod
    async def __result_map_from_request_response(request_response: httpx.Response):
        response_map = {
            HTTPStatus.INTERNAL_SERVER_ERROR: "await MusicApi.__raise(Exception)",
            HTTPStatus.BAD_REQUEST: "await MusicApi.__raise(Exception)",
            HTTPStatus.OK: True,
        }
        status_code = request_response.status_code
        result = response_map.get(status_code, 500)
        return result

    @staticmethod
    async def __raise(exception) -> Exception:
        raise exception


import asyncio
from pprint import pprint
pprint(asyncio.run(MusicApi.get_ten_most_popular_musics(1325)))