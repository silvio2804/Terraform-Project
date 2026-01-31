# 1. Aggiungi il repo (se non lo hai già fatto)
helm repo add chaos-mesh https://charts.chaos-mesh.org

# 2. Aggiorna i pacchetti
helm repo update

# 3. Installa

helm install chaos-mesh chaos-mesh/chaos-mesh \
  --namespace=chaos-mesh \
  --create-namespace \
  --set chaosDaemon.runtime=containerd \
  --set chaosDaemon.socketPath=/run/containerd/containerd.sock \
  --set dashboard.securityMode=false \
  --set chaosDaemon.privileged=true