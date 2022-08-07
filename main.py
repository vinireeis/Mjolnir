# Mjolnir
from src.domain.exceptions import NotFoundArtistId
from src.domain.validator import ArtistBaseModel
from src.domain.response.model import ResponseModel
from src.domain.enums.response_internal_code import InternalCode
from src.services.artist import ArtistService

# Standards
from http import HTTPStatus

# Third party
from asgiref.wsgi import WsgiToAsgi
from flask import Flask, request, Response
from loguru import logger

app = Flask("Mjolnir")
asgi_app = WsgiToAsgi(app)


@app.route('/')
async def hello_world() -> Response:
    response = ResponseModel(
        success=True,
        message= "Mjolnir API is now working!",
        code=InternalCode.SUCCESS
    ).build_http_response(status=HTTPStatus.OK)
    return response


@app.route('/top-songs/<int:artist_id>')
async def get_artist_songs(artist_id: int) -> Response:
    cache = request.args.get("cache", True)
    try:
        artist_validated = await ArtistBaseModel.unpack_raw_params(cache=cache, artist_id=artist_id)
        result = await ArtistService(artist_validated=artist_validated).get_ten_most_popular_songs()
        response = ResponseModel(
            success=True,
            result=result,
            code=InternalCode.SUCCESS
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except NotFoundArtistId as ex:
        logger.error(ex)
        response = ResponseModel(
            success=True,
            message="No artist was found with this id",
            result={},
            code=InternalCode.INVALID_PARAMS
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except ValueError as ex:
        logger.error(ex)
        response = ResponseModel(
            success=False,
            message="Invalid params",
            result={},
            code=InternalCode.INVALID_PARAMS
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except Exception as ex:
        logger.error(ex)
        response = ResponseModel(
            success=False,
            message="An unexpected error has occurred",
            code=InternalCode.INTERNAL_SERVER_ERROR
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

