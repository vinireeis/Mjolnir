# Mjolnir
from src.domain.validator import ArtistBaseModel

# Standards
from http import HTTPStatus

# Third party
from flask import Flask, request, Response

app = Flask("Mjolnir")


@app.route('/')
async def hello_world() -> Response:
    response = "Mjolnir API is now working!"
    return Response(response, HTTPStatus.OK)


@app.route('/top-musics/<string:artist_name>')
async def get_top_ten_musics(artist_id: int) -> Response:
    cache = request.args.get("cache", True)
    try:
        artist_validated = await ArtistBaseModel.unpack_raw_params(cache=cache, artist_id=artist_id)
        return Response("ok", HTTPStatus.OK)
    except ValueError as ex:
        return Response("Invalid params", HTTPStatus.BAD_REQUEST)
    except Exception as ex:
        return Response("An unexpected error has occurred", 500)


app.run(debug=True)
