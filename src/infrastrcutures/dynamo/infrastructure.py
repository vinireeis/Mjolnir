# Third party
from aioboto3 import Session
from contextlib import asynccontextmanager
from decouple import config
from loguru import logger


class DynamodbInfrastructure:

    session = None

    @classmethod
    async def get_session(cls):
        if cls.session is None:
            try:
                cls.session = Session(
                    aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
                    aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
                    region_name=config("AWS_REGION_NAME")
                )
            except Exception as ex:
                logger.error(ex=ex, __message="Error trying to get session on aws")
                raise ex
        return cls.session

    @classmethod
    @asynccontextmanager
    async def get_dynamodb_resource(cls):
        try:
            session = await cls.get_session()
            async with session.resource('dynamodb') as dynamodb_resource:
                yield dynamodb_resource
        except Exception as ex:
            logger.error(ex=ex, __message="Error trying to get dynamodb resource")
            raise ex
