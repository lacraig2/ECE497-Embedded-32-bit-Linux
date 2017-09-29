#!/bin/bash
BONE=${1:-192.168.7.2}
USER=debian
./setDNS.sh $BONE
./ipMasquerade.sh enp1s0f0
./ipMasquerade.sh wlp2s0