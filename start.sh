#!/bin/bash

set -x

kill -s SIGINT $(pgrep nodeos)
sleep 5

DATADIR="/root/opt/eos"
#nodeos --data-dir $DATADIR --config-dir $DATADIR --genesis-json  $DATADIR/mainnet-genesis.json
nodeos --data-dir $DATADIR --config-dir $DATADIR --verbose-http-errors  > $DATADIR/stdout.txt 2> $DATADIR/stderr.txt &  echo $! > $DATADIR/nodeos.pid
