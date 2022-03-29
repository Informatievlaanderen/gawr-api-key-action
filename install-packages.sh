#!/bin/bash

set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get -y upgrade
apt-get -y install --no-install-recommends curl;
pip --no-cache-dir install --upgrade pip;
pip --no-cache-dir install setuptools wheel boto3 docopt;
apt-get clean
rm -rf /var/lib/apt/lists/*
