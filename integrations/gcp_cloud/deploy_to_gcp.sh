#!/bin/bash
# Deploy Datashare + Neo4j to Google Cloud

set -e

echo "🚀 Deploying Investigation Platform to Google Cloud..."

# Set project
gcloud config set project berjak-development-project

# Create VM instance for Datashare
gcloud compute instances create datashare-investigation \
    --project=berjak-development-project \
    --zone=us-central1-a \
    --machine-type=e2-standard-4 \
    --network-interface=network-tier=PREMIUM,subnet=default \
    --maintenance-policy=MIGRATE \
    --provisioning-model=STANDARD \
    --service-account=jeremy.rich@berjak.com.au \
    --scopes=https://www.googleapis.com/auth/cloud-platform \
    --tags=datashare-server \
    --create-disk=auto-delete=yes,boot=yes,device-name=datashare-investigation,image=projects/cos-cloud/global/images/cos-stable-101-17162-40-8,mode=rw,size=50,type=projects/berjak-development-project/zones/us-central1-a/diskTypes/pd-balanced \
    --container-mount-host-path=mount-path=/home/datashare/Datashare,host-path=/home/datashare/data \
    --metadata-from-file=user-data=cloud-init.yml

# Create firewall rules
gcloud compute firewall-rules create allow-datashare \
    --project=berjak-development-project \
    --direction=INGRESS \
    --priority=1000 \
    --network=default \
    --action=ALLOW \
    --rules=tcp:8080,tcp:7474,tcp:7687 \
    --source-ranges=0.0.0.0/0 \
    --target-tags=datashare-server

echo "✅ Cloud deployment complete!"
echo "🌐 Datashare: http://$(gcloud compute instances describe datashare-investigation --zone=us-central1-a --format='get(networkInterfaces[0].accessConfigs[0].natIP)'):8080"
echo "🔗 Neo4j: http://$(gcloud compute instances describe datashare-investigation --zone=us-central1-a --format='get(networkInterfaces[0].accessConfigs[0].natIP)'):7474"
