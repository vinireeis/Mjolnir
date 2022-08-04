# Standards
from typing import Dict
from uuid import uuid4

# Third party
from pydantic import BaseModel


class ArtistBaseModel(BaseModel):
    artist_name: str
    cache: bool

    @classmethod
    async def unpack_raw_params(cls, cache, artist_name) -> Dict:
        params = {
            "artist_name": artist_name,
            "cache": cache,
            "id_transaction": uuid4(),
        }
        artist_validated = ArtistBaseModel(**params).dict()
        return artist_validated
