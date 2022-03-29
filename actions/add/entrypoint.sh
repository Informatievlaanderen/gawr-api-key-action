#!/bin/sh -l

python3 /app/gawr.py add --client="${1}" --email="${2}" --plan="${3}" --access-sync="${4}" --access-road-registry="${5}" --revoke-access="${6}" --env-tst="${7}" --aws-tst-access-key-id="${8}" --aws-tst-secret-access-key="${9}" --aws-tst-region-name="${10}" --aws-tst-api-id="${11}" --aws-tst-stage-name="${12}" --env-stg="${13}" --aws-stg-access-key-id="${14}" --aws-stg-secret-access-key="${15}" --aws-stg-region-name="${16}" --aws-stg-api-id="${17}" --aws-stg-stage-name="${18}" --env-prd="${19}" --aws-prd-access-key-id="${20}" --aws-prd-secret-access-key="${21}" --aws-prd-region-name="${22}" --aws-prd-api-id="${23}" --aws-prd-stage-name="${24}";
