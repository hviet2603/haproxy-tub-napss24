#!/bin/bash

if [[ -z $1 ]]; then
    echo "Number of backends required!"
elif [[ ! $1 =~ ^[0-9]+$ ]]; then
    echo "Number of backends invalid!"
else
    python3 template.py --backends="$1"
    echo "" >> templates/haproxy.cfg

    cp templates/docker-compose.yaml ..
    cp templates/prometheus.yml ../monitoring/prometheus/
    cp templates/haproxy.cfg ../haproxy_conf/
fi