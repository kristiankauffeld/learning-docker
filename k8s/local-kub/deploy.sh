# 
# Deploys all microservices to a local Kubernetes instance.
#
# Usage:
#
# ./k8s/local-kub/deploy.sh
#

#
# Deploy containers to Kubernetes.
#
kubectl apply -f rabbit.yaml
kubectl apply -f song-upload.yaml
