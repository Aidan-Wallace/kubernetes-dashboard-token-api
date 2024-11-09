# kubernetes-dashboard-token-api on Kubernetes

## Usage

### Setup

Create the token api deployment

```sh
kubectl apply -f manifests/kubernetes-dashboard-token.api.yaml
```

To create an ingress, change the host in the [ingress.yaml](./manifests/ingress.yaml) file

```sh
kubectl apply -f manifests/ingress.yaml
```

Incase there are permission issues when creating a token from the ui, create the cluster role manifest file

```sh
kubectl apply -f manifests/cluster-role.yaml
```

### Teardown

```sh
kubectl delete -f manifests/
```
