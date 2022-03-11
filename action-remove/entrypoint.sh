#!/bin/sh -l

python3 /main.py -k "${1}" --env-tst "${2}" --env-stg "${3}" --env-prd "${4}" --aws-tst-access-key-id "${5}" --aws-tst-secret-access-key "${6}" --aws-tst-region-name "${7}" --aws-stg-access-key-id "${8}" --aws-stg-secret-access-key "${9}" --aws-stg-region-name "${10}" --aws-prd-access-key-id "${11}" --aws-prd-secret-access-key "${12}"  --aws-prd-region-name "${13}";