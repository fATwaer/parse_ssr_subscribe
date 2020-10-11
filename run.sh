#!/bin/bash

set -ex

python get_ssr_server_config.py

pushd $(pwd)/shadowsocks
python shadowsocks/local.py -c config.json -d start
popd
