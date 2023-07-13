#!/bin/sh -l

python3 /main.py -k "${1}"\
 -c "${2}"\
 -e "${3}"\
 -p "${4}"\
 --access-sync "${5}"\
 --access-road-registry "${6}"\
 --env-tst "${7}"\
 --env-stg "${8}"\
 --env-prd "${9}"\
 --env-newprd "${10}"\
 --aws-tst-access-key-id "${11}"\
 --aws-tst-secret-access-key "${12}"\
 --aws-tst-region-name "${13}"\
 --aws-stg-access-key-id "${14}"\
 --aws-stg-secret-access-key "${15}"\
 --aws-stg-region-name "${16}"\
 --aws-prd-access-key-id "${17}"\
 --aws-prd-secret-access-key "${18}"\
 --aws-prd-region-name "${19}"\
 --aws-newprd-access-key-id "${20}"\
 --aws-newprd-secret-access-key "${21}"\
 --aws-newprd-region-name "${22}"\
 --revoke-access "${23}"\
 --access-tickets "true";