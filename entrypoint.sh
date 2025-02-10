#!/bin/bash

set -e

DIR_LIBS=/app/libs

mkdir -p $DIR_LIBS
cd $DIR_LIBS

if [ ! -d "volatility3" ]; then
    wget -q https://github.com/volatilityfoundation/volatility3/archive/refs/tags/v2.8.0.zip -O "volatility3.zip"
    unzip -q "volatility3.zip" -d "$DIR_LIBS"
    mv "$DIR_LIBS"/volatility3-* "volatility3"
    rm "volatility3.zip"
fi

if [ ! -d "volmemlyzer" ]; then
    wget -q https://github.com/ahlashkari/VolMemLyzer/archive/refs/tags/V2.0.0.zip -O "volmemlyzer.zip"
    unzip -q "volmemlyzer.zip" -d "$DIR_LIBS"
    mv "$DIR_LIBS"/VolMemLyzer-* "volmemlyzer"
    rm "volmemlyzer.zip"
fi

cd ..

exec "$@"
