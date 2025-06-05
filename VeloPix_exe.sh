#!/usr/bin/env bash                    
set -e                                  

# Unpack all the files
tar xzf velopix.tar.gz
   
# build env 
python3 -m venv env
source env/bin/activate
pip install -r velopix/requirements.txt

# Install custom velopix wheel
pip install velopix/velopix-0.7.7-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

# run the Python analysis script
for cfg in configurations/*.json; do
    python3 velopix/VeloPix_HyperParamHandler.py --config "$cfg"
    mv result.json output/result_$(basename "$cfg")
done
# deactivate venv
deactivate                                
