#!/usr/bin/env bash

uvicorn src.api.data_controller:app --host 0.0.0.0 --port 8001 --reload