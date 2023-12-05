#!/usr/bin/python3

import os, sys, json, argparse, uuid, boto3, requests

# args
parser = argparse.ArgumentParser(description='put new client apikey')

parser.add_argument('-k','--apikey', help='apikey', required=True)
parser.add_argument('-c','--client', help='client name', required=True)
parser.add_argument('-e','--email', help='email', required=True)
parser.add_argument('--revoke-access', help='revoked', required=False, default='false')
parser.add_argument('-p','--plan', help='plan options are ["anon", "abuse", "standard", "unlimited"]', required=True, default="standard")

parser.add_argument('--access-sync', help='["true", "false"] default: false', required=False, default='false')
parser.add_argument('--access-road-registry', help='["true", "false"] default: false', required=False, default='false')

parser.add_argument('--env-tst', help='["true", "false"] default: false', required=False, default='false')
parser.add_argument('--env-stg', help='["true", "false"] default: false', required=False, default='false')
parser.add_argument('--env-prd', help='["true", "false"] default: false', required=False, default='false')
parser.add_argument('--env-newprd', help='["true", "false"] default: false', required=False, default='false')

parser.add_argument('--aws-tst-access-key-id', required=True)
parser.add_argument('--aws-tst-secret-access-key', required=True)
parser.add_argument('--aws-tst-region-name', required=False, default='eu-west-1')

parser.add_argument('--aws-stg-access-key-id', required=True)
parser.add_argument('--aws-stg-secret-access-key', required=True)
parser.add_argument('--aws-stg-region-name', required=False, default='eu-west-1')

parser.add_argument('--aws-prd-access-key-id', required=True)
parser.add_argument('--aws-prd-secret-access-key', required=True)
parser.add_argument('--aws-prd-region-name', required=False, default='eu-west-1')

parser.add_argument('--aws-newprd-access-key-id', required=True)
parser.add_argument('--aws-newprd-secret-access-key', required=True)
parser.add_argument('--aws-newprd-region-name', required=False, default='eu-west-1')

parser.add_argument('--access-tickets', help='["true", "false"] default: true', required=False, default='true')

parser.add_argument('--aws-tst-redis-sync-url', required=False, default='')
parser.add_argument('--aws-stg-redis-sync-url', required=False, default='')
parser.add_argument('--aws-prd-redis-sync-url', required=False, default='')
parser.add_argument('--aws-newprd-redis-sync-url', required=False, default='')

args = parser.parse_args()

usage_plan_ids = {
    "anon": {
        "tst":"l80flj",
        "stg":"dyzrte",
        "prd":"2wb5cd",
        "newprd":"85vqi7",
    },
    "abuse": {
        "tst":"jgivsn",
        "stg":"ccfy0v",
        "prd":"9nrj1z",
        "newprd":"wbaqmh",
    },
    "standard": {
        "tst":"yhlc48",
        "stg":"oh8xgc",
        "prd":"m8vqe3",
        "newprd":"wrbda6",
    },
    "unlimited": {
        "tst":"6rhww4",
        "stg":"5fbb32",
        "prd":"r5patr",
        "newprd":"y8kou4",
    }
}

def sync_redis_all_env(apikey):
    sync_tst = args.aws_tst_redis_sync_url != ''
    sync_stg = args.aws_stg_redis_sync_url != ''
    sync_prd = args.aws_prd_redis_sync_url != ''
    sync_newprd = args.aws_newprd_redis_sync_url != ''
    
    if sync_tst:
        sync_redis(args.aws_tst_redis_sync_url, apikey)
    if sync_stg:
        sync_redis(args.aws_stg_redis_sync_url, apikey)
    if sync_prd:
        sync_redis(args.aws_prd_redis_sync_url, apikey)
    if sync_newprd:
        sync_redis(args.aws_newprd_redis_sync_url, apikey)
        
def sync_redis(base_url,apikey): 
    url = f"{base_url}/?x-api-key={apikey}"
    response = requests.get(url)

    if response.status_code == 200:
        print(f"Redis sync OK!")
        return
    
    print(f"Error: {response.status_code}")
    print(response.text)

def start_session(aws_access_key_id, aws_secret_access_key, region_name):
    return boto3.Session(aws_access_key_id, aws_secret_access_key, region_name=region_name)

def get_db_table(session):
    return session.resource('dynamodb').Table('basisregisters-api-gate-keys')

def get_client_attribute_updates(env):
    return {
        "SyncAccess": {
            "Action": "PUT", 
            "Value": args.access_sync == 'true'
        },
        "UsagePlanID": {
            "Action": "PUT", 
            "Value":  usage_plan_ids[args.plan][env]
        },
        "Description": {
            "Action": "PUT", 
            "Value": args.email
        },
        "WrAccess": {
            "Action": "PUT", 
            "Value": args.access_road_registry == 'true'
        },
        "Revoked": {
            "Action": "PUT", 
            "Value": args.revoke_access == 'true'
        },
        "ClientName": {
            "Action": "PUT", 
            "Value": args.client
        },
        "Plan": {
            "Action": "PUT", 
            "Value": args.plan
        },
        "Tickets": {
            "Action": "PUT", 
            "Value": args.access_tickets == 'true'
        }
    }

def json_serialize(obj):
    return json.dumps(obj, separators=(',', ':'))

def update_apikey(apikey):
    apply_in_tst = args.env_tst == 'true'
    apply_in_stg = args.env_stg == 'true'
    apply_in_prd = args.env_prd == 'true'
    apply_in_newprd = args.env_newprd == 'true'

    if(apply_in_tst):
        tst_session=start_session(args.aws_tst_access_key_id, args.aws_tst_secret_access_key, args.aws_tst_region_name)
        tst_table = get_db_table(tst_session)
        tst_item = get_client_attribute_updates(env='tst')
        tst_result = tst_table.update_item(
            Key={"ApiKey": apikey},
            AttributeUpdates= tst_item,
            ReturnValues="ALL_NEW"
        )
        print(f"In test:{tst_result}")
    
    if(apply_in_stg):
        stg_session=start_session(args.aws_stg_access_key_id, args.aws_stg_secret_access_key, args.aws_stg_region_name)
        stg_table = get_db_table(stg_session)
        stg_item = get_client_attribute_updates(env='stg')
        stg_result = stg_table.update_item(
            Key={"ApiKey": apikey},
            AttributeUpdates= stg_item,
            ReturnValues="ALL_NEW"
        )
        print(f"In staging: {stg_result}")
    
    if(apply_in_prd):
        prd_session=start_session(args.aws_prd_access_key_id, args.aws_prd_secret_access_key, args.aws_prd_region_name)
        prd_table = get_db_table(prd_session)
        prd_item = get_client_attribute_updates(env='prd')
        prd_result = prd_table.update_item(
            Key={"ApiKey": apikey},
            AttributeUpdates= prd_item,
            ReturnValues="ALL_NEW"
        )
        print(f"In production: {prd_result}")

    if(apply_in_newprd):
        newprd_session=start_session(args.aws_newprd_access_key_id, args.aws_newprd_secret_access_key, args.aws_newprd_region_name)
        newprd_table = get_db_table(newprd_session)
        newprd_item = get_client_attribute_updates(env='newprd')
        newprd_result = newprd_table.update_item(
            Key={"ApiKey": apikey},
            AttributeUpdates= newprd_item,
            ReturnValues="ALL_NEW"
        )
        print(f"In New production: {newprd_result}")

    sync_redis_all_env(apikey)

def main():
    if(args.apikey == None):
        exit(0);
    update_apikey(args.apikey)
    sys.exit()

if __name__ == "__main__":
    main()