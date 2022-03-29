from gawr_types import Environment
from gawr_aws_dynamodb import DynamoDB
from gawr_aws_apigateway import ApiGateWay
from boto3.session import Session


class AwsClient:
    def __init__(self, env: Environment):
        self.__env = env

        self.__session = Session(
            aws_access_key_id=env.aws_access_key_id,
            aws_secret_access_key=env.aws_secret_access_key,
            region_name=env.region)

        self.dynamodb = DynamoDB(
            table=self.__session.resource('dynamodb').Table(
                'basisregisters-api-gate-keys'),
            apply=self.__env.apply,
            env=self.__env.name)

        self.api_gateway = ApiGateWay(
            client=self.__session.client('apigateway'),
            apply=self.__env.apply,
            env=self.__env.name)
