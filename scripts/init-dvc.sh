#!/bin/bash

git init
dvc init

git config --global user.email "example@mail.com"
git config --global user.name "Test Name"

dvc remote add -d minio s3://test-bucket -f
dvc remote modify minio endpointurl http://my.domain:9000
dvc remote modify minio access_key_id testuser
dvc remote modify minio secret_access_key testpassword

git add .dvc/.gitignore .dvc/config .dvcignore
git commit -m "dvc init"