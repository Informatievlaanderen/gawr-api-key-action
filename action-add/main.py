#!/usr/bin/python3

import sys, json, argparse, uuid, boto3

# args
parser = argparse.ArgumentParser(description='add new client apikey')

parser.add_argument('-c','--client', help='client name', required=True)
parser.add_argument('-e','--email', help='email', required=True)
parser.add_argument('-p','--plan', help='plan options are ["anon", "standard", "unlimited"]', required=True, default="standard")
parser.add_argument('--revoke-access', help='["true", "false"] default: false', required=False, default='false')

parser.add_argument('--access-sync', help='["true", "false"] default: false', required=False, default='false')
parser.add_argument('--access-road-registry', help='["true", "false"] default: false', required=False, default='false')

parser.add_argument('--env-tst', help='["true", "false"] default: false', required=False, default='false')
parser.add_argument('--env-stg', help='["true", "false"] default: false', required=False, default='false')
parser.add_argument('--env-prd', help='["true", "false"] default: false', required=False, default='false')

parser.add_argument('--aws-tst-access-key-id', required=True)
parser.add_argument('--aws-tst-secret-access-key', required=True)
parser.add_argument('--aws-tst-region-name', required=False, default='eu-west-1')

parser.add_argument('--aws-stg-access-key-id', required=True)
parser.add_argument('--aws-stg-secret-access-key', required=True)
parser.add_argument('--aws-stg-region-name', required=False, default='eu-west-1')

parser.add_argument('--aws-prd-access-key-id', required=True)
parser.add_argument('--aws-prd-secret-access-key', required=True)
parser.add_argument('--aws-prd-region-name', required=False, default='eu-west-1')

args = parser.parse_args()

usage_plan_ids = {
    "anon": {
        "tst":"l80flj",
        "stg":"dyzrte",
        "prd":"2wb5cd",
    },
    "standard": {
        "tst":"yhlc48",
        "stg":"oh8xgc",
        "prd":"m8vqe3",
    },
    "unlimited": {
        "tst":"6rhww4",
        "stg":"5fbb32",
        "prd":"r5patr",
    }
}

def start_session(aws_access_key_id, aws_secret_access_key, region_name):
    return boto3.Session(aws_access_key_id, aws_secret_access_key, region_name=region_name)

def get_db_table(session):
    return session.resource('dynamodb').Table('basisregisters-api-gate-keys')

def get_client_api_key(apikey, env):
    client_api_key = {
            "ApiKey": apikey,
            "SyncAccess": args.access_sync == 'true',
            "UsagePlanID": usage_plan_ids[args.plan][env],
            "Description": args.email,
            "WrAccess": args.access_road_registry == 'true',
            "Revoked": args.revoke_access == 'true',
            "ClientName": args.client,
            "Plan": args.plan
    }
    return client_api_key

def json_serialize(obj):
    return json.dumps(obj, separators=(',', ':'))

def add_apikey(apikey):
    apply_in_tst = args.env_tst == 'true'
    apply_in_stg = args.env_stg == 'true'
    apply_in_prd = args.env_prd == 'true'

    if(apply_in_tst):
        tst_session=start_session(args.aws_tst_access_key_id, args.aws_tst_secret_access_key, args.aws_tst_region_name)
        tst_table = get_db_table(tst_session)
        tst_item = get_client_api_key(apikey, env='tst')
        tst_table.put_item(Item=tst_item)
        print(json_serialize(tst_item))
        print("Done in test!")
    
    if(apply_in_stg):
        stg_session=start_session(args.aws_stg_access_key_id, args.aws_stg_secret_access_key, args.aws_stg_region_name)
        stg_table = get_db_table(stg_session)
        stg_item = get_client_api_key(apikey, env='stg')
        stg_table.put_item(Item=stg_item)
        print(json_serialize(stg_item))
        print("Done in staging!")
    
    if(apply_in_prd):
        prd_session=start_session(args.aws_prd_access_key_id, args.aws_prd_secret_access_key, args.aws_prd_region_name)
        prd_table = get_db_table(prd_session)
        prd_item = get_client_api_key(apikey, env='prd')
        prd_table.put_item(Item=prd_item)
        print(json_serialize(prd_item))
        print("Done in production!")

def main():
    apikey = str(uuid.uuid4())
    print(f"Adding new client apikey: {apikey}")
    add_apikey(apikey)
    sys.exit()

if __name__ == "__main__":
    main()