#!/bin/bash
cd scripts
docker build -t $1 .
cd ..
