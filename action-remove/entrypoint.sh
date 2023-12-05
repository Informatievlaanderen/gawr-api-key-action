#!/bin/sh -l

python3 /main.py -k "${1}"\
 --env-tst "${2}"\
 --env-stg "${3}"\
 --env-prd "${4}"\
 --env-newprd "${5}"\
 --aws-tst-access-key-id "${6}"\
 --aws-tst-secret-access-key "${7}"\
 --aws-tst-region-name "${8}"\
 --aws-stg-access-key-id "${9}"\
 --aws-stg-secret-access-key "${10}"\
 --aws-stg-region-name "${11}"\
 --aws-prd-access-key-id "${12}"\
 --aws-prd-secret-access-key "${13}"\
 --aws-prd-region-name "${14}"\
 --aws-newprd-access-key-id "${15}"\
 --aws-newprd-secret-access-key "${16}"\
 --aws-newprd-region-name "${17}"\
 --aws-tst-redis-sync-url "${18}"\
 --aws-stg-redis-sync-url "${19}"\
 --aws-prd-redis-sync-url "${20}"\
 --aws-newprd-redis-sync-url "${21}";