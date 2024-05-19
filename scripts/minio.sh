#!/bin/bash

# Script for minio initialization on remote server into docker container.
# Create bucket - handle
# Don't forget to change bucket name in file - init-dvc.sh. (current bucket name - test-bucket)

sudo apt update -y
sudo apt-get install ca-certificates curl

sudo install -m 0755 -d /etc/apt/keyrings -y
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

docker run -it \
   -p 9000:9000 \
   -p 9001:9001 \
   --name minio \
   -v ~/minio/data:/data \
   -e "MINIO_ROOT_USER=test1234" \
   -e "MINIO_ROOT_PASSWORD=test1234" \
   quay.io/minio/minio server /data --console-address ":9001"