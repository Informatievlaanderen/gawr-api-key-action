#!/bin/sh -l

python3 /main.py -c "${1}" -e "${2}" -p "${3}" --access-sync "${4}" --access-road-registry "${5}" --env-tst "${6}" --env-stg "${7}" --env-prd "${8}" --aws-tst-access-key-id "${9}" --aws-tst-secret-access-key "${10}" --aws-tst-region-name "${11}" --aws-stg-access-key-id "${12}" --aws-stg-secret-access-key "${13}" --aws-stg-region-name "${14}" --aws-prd-access-key-id "${15}" --aws-prd-secret-access-key "${16}"  --aws-prd-region-name "${17}";