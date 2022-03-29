#!/usr/bin/python3

"""
Usage:
    gawr.py remove [options]

Options:
    -h, --h
    -k, --apikey=<value>                    apikey
    --env-tst=<true|false>                  [default: false] apply changes to test env
    --env-stg=<true|false>                  [default: false] apply changes to staging env
    --env-prd=<true|false>                  [default: false] apply changes to production env
    --aws-tst-access-key-id=<value>         aws key id of test env
    --aws-stg-access-key-id=<value>         aws key id of staging env
    --aws-prd-access-key-id=<value>         aws key id of production env
    --aws-tst-secret-access-key=<value>     aws key of test env
    --aws-stg-secret-access-key=<value>     aws key of staging env
    --aws-prd-secret-access-key=<value>     aws key of production env
    --aws-tst-api-id=<value>                aws gateway restapi id
    --aws-stg-api-id=<value>                aws gateway restapi id
    --aws-prd-api-id=<value>                aws gateway restapi id
    --aws-tst-stage-name=<value>            aws gateway stage name
    --aws-stg-stage-name=<value>            aws gateway stage name
    --aws-prd-stage-name=<value>            aws gateway stage name
    --aws-tst-region-name=<value>           [default: eu-west-1] aws region of test env
    --aws-stg-region-name=<value>           [default: eu-west-1] aws region of staging env
    --aws-prd-region-name=<value>           [default: eu-west-1] aws region of production env
"""

from docopt import docopt