#!/usr/bin/python3

from gawr_util import kebab_case, try_get


class Environment:
    def __init__(self, name: str, apply: bool, aws_access_key_id: str, aws_secret_access_key: str, region: str, api_id: str, stage_name: str):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region = region
        self.name = name
        self.apply = apply
        self.api_id = api_id
        self.stage_name = stage_name


class ActionArgs:
    def __init__(self, args):
        self.environments = {
            "tst": Environment(
                name="tst",
                apply=args['--env-tst'] == 'true',
                aws_access_key_id=args['--aws-tst-access-key-id'],
                aws_secret_access_key=args['--aws-tst-secret-access-key'],
                region=args['--aws-tst-region-name'],
                api_id=args['--aws-tst-api-id'],
                stage_name=args['--aws-tst-stage-name']
            ),
            "stg": Environment(
                name="stg",
                apply=args['--env-stg'] == 'true',
                aws_access_key_id=args['--aws-stg-access-key-id'],
                aws_secret_access_key=args['--aws-stg-secret-access-key'],
                region=args['--aws-stg-region-name'],
                api_id=args['--aws-stg-api-id'],
                stage_name=args['--aws-stg-stage-name']
            ),
            "prd": Environment(
                name="prd",
                apply=args['--env-prd'] == 'true',
                aws_access_key_id=args['--aws-prd-access-key-id'],
                aws_secret_access_key=args['--aws-prd-secret-access-key'],
                region=args['--aws-prd-region-name'],
                api_id=args['--aws-prd-api-id'],
                stage_name=args['--aws-prd-stage-name']
            )
        }


class AddActionArgs(ActionArgs):
    def __init__(self, args):
        self.client_name: str = args['--client']
        self.description: str = args['--email']
        self.plan: str = args['--plan']
        self.sync_access: bool = bool(args['--access-sync'] == 'true')
        self.road_access: bool = bool(args['--access-road-registry'] == 'true')
        self.revoked: bool = bool(args['--revoke-access'] == 'true')
        ActionArgs.__init__(self, args)


class RemoveActionArgs(ActionArgs):
    def __init__(self, args):
        self.api_key: str = str(args['--apikey'])
        ActionArgs.__init__(self, args)


class UpdateActionArgs(ActionArgs):
    def __init__(self, args):
        self.api_key: str = str(args['--apikey'])
        self.client_name: str = args['--client']
        self.description: str = args['--email']
        self.plan: str = args['--plan']
        self.sync_access: bool = bool(args['--access-sync'] == 'true')
        self.road_access: bool = bool(args['--access-road-registry'] == 'true')
        self.revoked: bool = bool(args['--revoke-access'] == 'true')
        ActionArgs.__init__(self, args)


class ApiKey:
    def __init__(self, api_key: str, client_name: str, description: str, sync_access: bool, road_access: bool, revoked: bool, plan: str, usage_plan_id: str, api_id: str, stage_name: str, api_key_id: str = ""):
        self.ApiKey = api_key
        self.ClientName = client_name
        self.Description = description
        self.SyncAccess = sync_access
        self.WrAccess = road_access
        self.Revoked = revoked
        self.Plan = plan
        self.UsagePlanID = usage_plan_id
        self.ApiId = api_id
        self.StageName = stage_name
        self.ApiKeyId = api_key_id

    def ParseDynamoDbResult(item: any):
        data = try_get(item, "Item")
        
        if data == None:
            return None;
        
        return ApiKey(
            api_key=try_get(data, "ApiKey"),
            client_name=try_get(data, "ClientName"),
            description=try_get(data, "Description"),
            sync_access=try_get(data, "SyncAccess"),
            road_access=try_get(data, "WrAccess"),
            revoked=try_get(data, "Revoked"),
            plan=try_get(data, "Plan"),
            usage_plan_id=try_get(data, "UsagePlanID"),
            api_id=try_get(data, "ApiId"),
            stage_name=try_get(data, "StageName"),
            api_key_id=try_get(data, "ApiKeyId")
        )


class CreateApiKeyRequest:
    def __init__(self, apikey: ApiKey):
        self.name = kebab_case(apikey.ClientName)
        self.description = apikey.Description
        self.enabled = apikey.Revoked == False
        self.value = apikey.ApiKey
        self.stageKeys = [{
            "restApiId": apikey.ApiId,
            "stageName": apikey.StageName
        }]
        self.tags = {
            'clientname': apikey.ClientName,
            'email': apikey.Description,
            'syncaccess': str(apikey.SyncAccess).lower(),
            'wraccess': str(apikey.WrAccess).lower(),
            'revoked': str(apikey.Revoked).lower(),
            'plan': apikey.Plan
        }
