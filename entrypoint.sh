#!/bin/bash

set -e

DIR_LIBS=/app/libs

mkdir -p $DIR_LIBS

if [ ! -d "$DIR_LIBS/volatility3" ]; then
    wget -q https://github.com/volatilityfoundation/volatility3/archive/refs/tags/v2.8.0.zip -O "$DIR_LIBS/volatility3.zip"
    unzip -q "$DIR_LIBS/volatility3.zip" -d "$DIR_LIBS"
    mv "$DIR_LIBS"/volatility3-* "$DIR_LIBS/volatility3"
    rm "$DIR_LIBS/volatility3.zip"
fi

if [ ! -d "$DIR_LIBS/volmemlyzer" ]; then
    wget -q https://github.com/ahlashkari/VolMemLyzer/archive/refs/tags/V2.0.0.zip -O "$DIR_LIBS/volmemlyzer.zip"
    unzip -q "$DIR_LIBS/volmemlyzer.zip" -d "$DIR_LIBS"
    mv "$DIR_LIBS"/VolMemLyzer-* "$DIR_LIBS/volmemlyzer"
    rm "$DIR_LIBS/volmemlyzer.zip"
fi

exec "$@"
