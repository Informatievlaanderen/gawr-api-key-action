#!/usr/bin/python3

import os, sys, json, argparse, uuid, boto3

# args
parser = argparse.ArgumentParser(description='put new client apikey')

parser.add_argument('-k','--apikey', help='apikey', required=True)
parser.add_argument('-c','--client', help='client name', required=True)
parser.add_argument('-e','--email', help='email', required=True)
parser.add_argument('-p','--plan', help='plan options are ["anon", "standard", "unlimited"]', required=True, default="standard")

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
  
def start_session(aws_access_key_id, aws_secret_access_key, region_name):
    return boto3.Session(aws_access_key_id, aws_secret_access_key, region_name=region_name)

def get_db_table(session):
    return session.resource('dynamodb').Table('basisregisters-api-gate-keys')

def get_client_attribute_updates(apikey):
    if(args.plan == 'anon'):
        usage_plan_id = 'l80flj'
    elif(args.plan == 'unlimited'):
        usage_plan_id = '6rhww4'
    else:
        usage_plan_id = 'yhlc48'

    return {
        "SyncAccess": {
            "Action": "PUT", 
            "Value": args.access_sync == 'true'
        },
        "UsagePlanID": {
            "Action": "PUT", 
            "Value": usage_plan_id
        },
        "Description": {
            "Action": "PUT", 
            "Value": args.email
        },
        "WrAccess": {
            "Action": "PUT", 
            "Value": args.access_road_registry == 'true'
        },
        "ClientName": {
            "Action": "PUT", 
            "Value": args.client
        },
        "Plan": {
            "Action": "PUT", 
            "Value": args.plan
        }
    }

def json_serialize(obj):
    return json.dumps(obj, separators=(',', ':'))

def update_apikey(apikey):
    apply_in_tst = args.env_tst == 'true'
    apply_in_stg = args.env_stg == 'true'
    apply_in_prd = args.env_prd == 'true'

    client_attribute = get_client_attribute_updates(apikey)

    if(apply_in_tst):
        tst_session=start_session(args.aws_tst_access_key_id, args.aws_tst_secret_access_key, args.aws_tst_region_name)
        tst_table = get_db_table(tst_session)
        tst_result = tst_table.update_item(
            Key={"ApiKey": apikey},
            AttributeUpdates= client_attribute,
            ReturnValues="ALL_NEW"
        )
        print("In test:")
        print(tst_result)
    
    if(apply_in_stg):
        stg_session=start_session(args.aws_stg_access_key_id, args.aws_stg_secret_access_key, args.aws_stg_region_name)
        stg_table = get_db_table(stg_session)
        stg_result = stg_table.update_item(
            Key={"ApiKey": apikey},
            AttributeUpdates= client_attribute,
            ReturnValues="ALL_NEW"
        )
        print("In staging:")
        print(stg_result)
    
    if(apply_in_prd):
        prd_session=start_session(args.aws_prd_access_key_id, args.aws_prd_secret_access_key, args.aws_prd_region_name)
        prd_table = get_db_table(prd_session)
        prd_result = prd_table.update_item(
            Key={"ApiKey": apikey},
            AttributeUpdates= client_attribute,
            ReturnValues="ALL_NEW"
        )
        print("In production:")
        print(prd_result)

def main():
    if(args.apikey == None):
        exit(0);
    update_apikey(args.apikey)
    sys.exit()

if __name__ == "__main__":
    main()