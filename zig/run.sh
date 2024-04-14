#!/usr/bin/env bash

if [ -z "$1" ]; then
    echo "Usage: ./run.sh test/easy.txt"
    exit 1
fi

zig build -Doptimize=ReleaseFast run < <(cat $1)
