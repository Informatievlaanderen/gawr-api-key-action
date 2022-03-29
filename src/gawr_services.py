#!/usr/bin/python3

from logging import exception
from typing import Dict
from gawr_types import ActionArgs, AddActionArgs, RemoveActionArgs, UpdateActionArgs, ApiKey
from gawr_aws_client import AwsClient
from gawr_util import generate_guid


class GawrService:
    __usage_plan_ids = {
        "anon": {
            "tst": "l80flj",
            "stg": "dyzrte",
            "prd": "2wb5cd",
        },
        "abuse": {
            "tst": "jgivsn",
            "stg": "ccfy0v",
            "prd": "9nrj1z",
        },
        "standard": {
            "tst": "yhlc48",
            "stg": "oh8xgc",
            "prd": "m8vqe3",
        },
        "unlimited": {
            "tst": "6rhww4",
            "stg": "5fbb32",
            "prd": "r5patr",
        }
    }

    def __init__(self, args: ActionArgs):
        self.__args = args
        self.__aws: Dict[str, AwsClient] = {}
        for env_name, env in args.environments.items():
            self.__aws[env_name] = AwsClient(env)

    def __get_usage_plan_id__(self, plan: str, env_name: str):
        return self.__usage_plan_ids[plan][env_name]

    def create_new_api_key(self):
        if not isinstance(self.__args, AddActionArgs):
            exception("argument exception")

        for env_name, client in self.__aws.items():
            if not self.__args.environments[env_name].apply:
                continue
            
            apikey = ApiKey(
                generate_guid(),
                self.__args.client_name,
                self.__args.description,
                self.__args.sync_access,
                self.__args.road_access,
                self.__args.revoked,
                self.__args.plan,
                self.__get_usage_plan_id__(self.__args.plan, env_name),
                self.__args.environments[env_name].api_id,
                self.__args.environments[env_name].stage_name,
                None
            )

            # API Gateway
            response = client.api_gateway.create_apigateway_apikey(apikey)
            print(
                f"API key {apikey.ApiKey} has been created in aws API Gateway")

            apikey.ApiKeyId = response.get("id")
            delattr(apikey, "StageName")
            delattr(apikey, "ApiId")

            # DynamoDB
            client.dynamodb.create_new_apikey(apikey)
            print(f"API key {apikey.ApiKey} has been created in DynamoDB")

    def delete_api_key(self):
        if not isinstance(self.__args, RemoveActionArgs):
            exception("argument exception")

        for env_name, client in self.__aws.items():
            if not self.__args.environments[env_name].apply:
                continue
            
            apikey = client.dynamodb.get_api_key(api_key=self.__args.api_key);
            api_key_id = apikey.get("Item").get("ApiKeyId")
            client.api_gateway.delete_apigateway_apikey(api_key_id=api_key_id)
            client.dynamodb.delete_api_key(api_key=self.__args.api_key)
            
            print(f"Deleted the apikey {self.__args.api_key} in {env_name}")

    def update_api_key(self):
        if not isinstance(self.__args, UpdateActionArgs):
            exception("argument exception")

        for env_name, client in self.__aws.items():
            if not self.__args.environments[env_name].apply:
                continue
            
            apikey = client.dynamodb.get_api_key(api_key=self.__args.api_key);
            
            old_usage_plan_id = apikey.UsagePlanID
            new_usage_plan_id = self.__get_usage_plan_id__(self.__args.plan, env_name)
           
            if old_usage_plan_id != new_usage_plan_id:
                # API Gateway UsagePlan Keys
                client.api_gateway.update_usage_plan_key(apikey.ApiKeyId, old_usage_plan_id, new_usage_plan_id)
                
            # Apply Changes
            apikey.ApiKey = self.__args.api_key
            apikey.ClientName = self.__args.client_name
            apikey.Description = self.__args.description
            apikey.SyncAccess = self.__args.sync_access
            apikey.WrAccess = self.__args.road_access
            apikey.Revoked = self.__args.revoked
            apikey.Plan = self.__args.plan
            apikey.UsagePlanID = new_usage_plan_id
            apikey.ApiId = None
            apikey.StageName = None
            
            # Update item in DynamoDB
            response = client.dynamodb.update_api_key(apikey)
            apikey.ApiKeyId = response.get("Attributes").get("ApiKeyId")

            apikey.ApiId = self.__args.environments[env_name].api_id
            apikey.StageName = self.__args.environments[env_name].stage_name
        
            # Update Api Gateway
            client.api_gateway.update_apigateway_apikey(apikey, client.dynamodb)
            
            print(f"Updated the apikey {apikey.ApiKey} in {env_name}")
