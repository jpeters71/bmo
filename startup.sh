#!/bin/bash
# ====================================================
# Startup script for BMO
# ----------------------------------------------------
cd /home/bmo/work/bmo
. ./venv/bin/activate
echo "ENVIRONMENT"
echo "=============="
env 
echo "--------------"
echo "pwd"
pwd
echo "--------------"
python ./main.py >> /tmp/bmo.log 2>&1 &
cd
