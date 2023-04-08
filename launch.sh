#!/usr/bin/env bash

set -e  # exit immediately if a command fails

export PATH=$PATH:$HOME/.local/bin

echo "Started streamlit launch at $(date +'%Y/%m/%d %H:%M:%S')"

cd /home/heleribera/grocery_list_app
echo "Changed dir"

poetry run streamlit run streamlit_app.py --server.port 8501
echo "Service launched!"