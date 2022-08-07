# Mjolnir
from ...infrastrcutures.dynamo.infrastructure import DynamodbInfrastructure

# Third party
from boto3.dynamodb.conditions import Key
from decouple import config


class DynamodbRepository:

    infra = DynamodbInfrastructure

    @classmethod
    async def get_items(cls, key: str, value: str) -> list:
        async with cls.infra.get_dynamodb_resource() as dynamodb_resource:

            table = await dynamodb_resource.Table(config('AWS_TABLE_NAME'))
            result = await table.query(
                KeyConditionExpression=Key(key).eq(value)
            )

        return result['Items']

    @classmethod
    async def put_items(cls, item: dict):
        async with cls.infra.get_dynamodb_resource() as dynamodb_resource:

            table = await dynamodb_resource.Table(config('AWS_TABLE_NAME'))
            await table.put_item(
                Item=item
            )
