#!/bin/sh -l

python3 /app/gawr.py update --apikey="${1}" --client="${2}" --email="${3}" --plan="${4}" --access-sync="${5}" --access-road-registry="${6}" --revoke-access="${7}"--env-tst="${8}"--aws-tst-access-key-id="${9}"--aws-tst-secret-access-key="${10}"--aws-tst-region-name="${11}"--aws-tst-api-id="${12}"--aws-tst-stage-name="${13}" --env-stg="${14}"--aws-stg-access-key-id="${15}"--aws-stg-secret-access-key="${16}"--aws-stg-region-name="${17}"--aws-stg-api-id="${18}"--aws-stg-stage-name="${19}"--env-prd="${20}"--aws-prd-access-key-id="${21}"--aws-prd-secret-access-key="${22}" --aws-prd-region-name="${23}" --aws-prd-api-id="${24}" --aws-prd-stage-name="${25}";
