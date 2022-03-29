from gawr_types import ApiKey
from gawr_util import generate_guid


class DynamoDB:
    def __init__(self, table, env: str, apply: bool):
        self.__table = table
        self.__env = env
        self.__apply = apply

    def __generate_update_apikey_request__(self, client_name: str, description: str, sync_access: bool, wr_access: bool, revoked: bool, plan: str, plan_id: str, api_key_id: str):
        return {
            "SyncAccess": {
                "Action": "PUT",
                "Value": sync_access
            },
            "UsagePlanID": {
                "Action": "PUT",
                "Value":  plan_id
            },
            "Description": {
                "Action": "PUT",
                "Value": description
            },
            "WrAccess": {
                "Action": "PUT",
                "Value": wr_access
            },
            "Revoked": {
                "Action": "PUT",
                "Value": revoked
            },
            "ClientName": {
                "Action": "PUT",
                "Value": client_name
            },
            "Plan": {
                "Action": "PUT",
                "Value": plan
            },
            "ApiKeyId": {
                "Action": "PUT",
                "Value": api_key_id
            }
        }

    def create_new_apikey(self, apikey: ApiKey):
        if (not self.__apply):
            return None
        self.__table.put_item(Item=apikey.__dict__)

    def get_api_key(self, api_key: str):
        if (not self.__apply):
            return None
        item=self.__table.get_item(Key={'ApiKey': api_key})
        return ApiKey.ParseDynamoDbResult(item)

    def delete_api_key(self, api_key: str):
        if (not self.__apply):
            return None

        self.__table.delete_item(Key={"ApiKey": api_key})

    def update_api_key(self, api_key: ApiKey):
        if (not self.__apply):
            return None

        return self.__table.update_item(
            Key={"ApiKey": api_key.ApiKey},
            AttributeUpdates=self.__generate_update_apikey_request__(
                api_key.ClientName,
                api_key.Description,
                api_key.SyncAccess,
                api_key.WrAccess,
                api_key.Revoked,
                api_key.Plan,
                api_key.UsagePlanID,
                api_key.ApiKeyId
            ),
            ReturnValues="ALL_NEW"
        )
