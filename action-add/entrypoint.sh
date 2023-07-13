#!/bin/sh -l

python3 /main.py -c "${1}"\
 -e "${2}"\
 -p "${3}"\
 --access-sync "${4}"\
 --access-road-registry "${5}"\
 --env-tst "${6}"\
 --env-stg "${7}"\
 --env-prd "${8}"\
 --env-newprd "${9}"\
 --aws-tst-access-key-id "${10}"\
 --aws-tst-secret-access-key "${11}"\
 --aws-tst-region-name "${12}"\
 --aws-stg-access-key-id "${13}"\
 --aws-stg-secret-access-key "${14}"\
 --aws-stg-region-name "${15}"\
 --aws-prd-access-key-id "${16}"\
 --aws-prd-secret-access-key "${17}"\
 --aws-prd-region-name "${18}"\
 --aws-newprd-access-key-id "${19}"\
 --aws-newprd-secret-access-key "${20}"\
 --aws-newprd-region-name "${21}"\
 --revoke-access "${22}"\
 --access-tickets "${23}";
