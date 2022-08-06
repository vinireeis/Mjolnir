# Standards
from typing import Dict
from uuid import uuid4

# Third party
from pydantic import BaseModel, Extra


class ArtistBaseModel(BaseModel, extra=Extra.forbid):
    artist_id: str
    cache: bool = True

    @classmethod
    async def unpack_raw_params(cls, cache, artist_id) -> Dict:
        params = {
            "artist_id": artist_id,
            "cache": cache,
            "id_transaction": uuid4(),
        }
        artist_validated = ArtistBaseModel(**params).dict()
        return artist_validated
