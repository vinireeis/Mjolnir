# Jormungandr
# from ...infrastrcutures.redis.infrastructure import RedisInfrastructure
from src.infrastrcutures.redis.infrastructure import RedisInfrastructure

# Third party
from decouple import config
from loguru import logger


class RedisRepository:

    @staticmethod
    async def get(key: str) -> bytes:
        redis = await RedisInfrastructure.get_client()
        songs_most_popular = await redis.get(key)
        return songs_most_popular

    @staticmethod
    async def set(key: str, value: str):
        redis = await RedisInfrastructure.get_client()
        try:

            result = await redis.set(
                key,
                value,
                ex=int(config("REDIS_DATA_EXPIRATION_IN_SECONDS")),
            )
            return result

        except Exception as ex:
            logger.error(ex=ex, __message=f"RedisRepository::set::error on trying to set data")
            raise ex

    @staticmethod
    async def delete(key: str):
        redis = await RedisInfrastructure.get_client()
        try:
            await redis.delete(key)
        except Exception as ex:
            logger.error(ex=ex, __message=f"RedisRepository::delete::error on trying to delete key")
            raise ex
