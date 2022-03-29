#!/bin/sh -l

python3 /app/gawr.py remove --apikey="${1}" --env-tst="${2}" --aws-tst-access-key-id="${3}" --aws-tst-secret-access-key="${4}" --aws-tst-region-name="${5}" --aws-tst-api-id="${6}" --aws-tst-stage-name="${7}" --env-stg="${8}" --aws-stg-access-key-id="${9}" --aws-stg-secret-access-key="${10}" --aws-stg-region-name="${11}" --aws-stg-api-id="${12}" --aws-stg-stage-name="${13}" --env-prd="${14}" --aws-prd-access-key-id="${15}" --aws-prd-secret-access-key="${16}" --aws-prd-region-name="${17}" --aws-prd-api-id="${18}" --aws-prd-stage-name="${19}";
