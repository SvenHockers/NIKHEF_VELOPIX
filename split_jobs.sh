#!/usr/bin/env bash
for cfg in velopix/configurations/*.json; do
    echo "Submitting with config: $cfg"
    condor_submit job.sub \
        -append "CONFIG=$cfg"
done