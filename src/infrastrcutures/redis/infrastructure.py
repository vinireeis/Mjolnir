# Third party
from decouple import config
from loguru import logger
import aioredis


class RedisInfrastructure:
    redis = None

    @classmethod
    async def get_client(cls):
        if cls.redis is None:
            try:
                url = config("REDIS_HOST")
                cls.redis = await aioredis.from_url(url, max_connections=10)
            except Exception as ex:
                logger.error(
                    ex=ex,
                    __message=f"RedisInfrastructure::get_client::Error connecting the client for the given url",
                )
                raise ex
        return cls.redis
