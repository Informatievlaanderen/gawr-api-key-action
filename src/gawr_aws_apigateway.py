from gawr_aws_dynamodb import DynamoDB
from gawr_types import ApiKey, CreateApiKeyRequest, Environment
from gawr_util import kebab_case


class ApiGateWay:
    def __init__(self, client, env: str, apply: bool):
        self.__client = client
        self.__env = env
        self.__apply = apply

    def __create_usage_plan_key(self, apikey_id: str, plan_id: str):
        self.__client.create_usage_plan_key(
            usagePlanId=plan_id,
            keyId=apikey_id,
            keyType='API_KEY'
        )

    def __delete_usage_plan_key(self, apikey_id: str, plan_id: str):
        self.__client.delete_usage_plan_key(
            usagePlanId=plan_id,
            keyId=apikey_id
        )

    def update_usage_plan_key(self, apikey_id: str, old_plan_id: str, new_plan_id):
        if (not self.__apply):
            return None
        
        self.__delete_usage_plan_key(apikey_id, old_plan_id)
        self.__create_usage_plan_key(apikey_id, new_plan_id)

    def create_apigateway_apikey(self, apikey: ApiKey):
        if (not self.__apply):
            return None

        request = CreateApiKeyRequest(apikey)
        response = self.__client.create_api_key(
            name=request.name,
            description=request.description,
            enabled=request.enabled,
            value=request.value,
            stageKeys=request.stageKeys,
            tags=request.tags
        )
        apikey_id = response.get("id")
        self.__create_usage_plan_key(apikey_id, apikey.UsagePlanID)

        return response

    def delete_apigateway_apikey(self, api_key_id: str):
        if (not self.__apply):
            return None
        self.__client.delete_api_key(apiKey= api_key_id)

    def update_apigateway_apikey(self, apikey: ApiKey, dynamoClient: DynamoDB):
        if (not self.__apply):
            return None
            
        self.delete_apigateway_apikey(apikey.ApiKeyId)
        response = self.create_apigateway_apikey(apikey)
        apikey.ApiKeyId = response.get("id")
        delattr(apikey, "StageName")
        delattr(apikey, "ApiId")
        dynamoClient.update_api_key(api_key = apikey);
        return apikey
