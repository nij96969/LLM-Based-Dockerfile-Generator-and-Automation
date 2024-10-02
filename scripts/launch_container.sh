#!/bin/bash
container_id=$(docker run -dit $1)
echo "Container Id :: $container_id"