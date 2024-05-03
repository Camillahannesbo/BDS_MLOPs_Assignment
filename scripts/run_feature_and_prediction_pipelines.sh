#!/bin/bash

set -e

cd notebooks

# Run the feature pipeline
jupyter nbconvert --to notebook --execute 2_feature_pipeline.ipynb

# Run the batch inference pipeline
jupyter nbconvert --to notebook --execute 4_batch_inference.ipynb
