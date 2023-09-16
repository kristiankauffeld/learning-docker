# 
# Remove containers from Kubernetes.
#
# Usage:
#
# ./k8s/local-kub/delete.sh
#

kubectl delete -f rabbit.yaml
kubectl delete -f song-upload.yaml
kubectl delete -f postgres.yaml
kubectl delete -f stem-separation.yaml