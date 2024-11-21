# kubernetes-dashboard-token-api

A bearer token generator ui and api that will generate a valid token that can be used to access the kubernetes dashboard

## Usage

Running this assume kubectl is installed and has a valid kubeconfig configured

```sh
KUBECTL_CMD=$(which kubectl) uvicorn app.main:app
```

Visit [localhost:8000](https://localhost:8000) to get a token

Visit [localhost:8000?redirect=false](https://localhost:8000?redirect=false) to get a token without redirecting to a Kubernetes dashboard

### api

retrieve a token RESTfully

```sh
curl http://localhost:8000/json
```

### Docker

When running locally, the target kube config needs passed in as `/data/config.conf` to the container. In kubernetes, the context is already available (at least in microk8s)

```sh
# build the image
docker build -t aidanwallace/kubernetes-dashboard-token-api .

# run the image
docker run --rm -v -d <kube config location>:/data/config.conf -p 8082:80 aidanwallace/kubernetes-dashboard-token-api
# example: 'docker run --rm -d -v ./.cache/config.conf:/data/config.conf -p 8082:80 aidanwallace/kubernetes-dashboard-token-api'

```

## Env

| key                      | description                                                    | type   | required | default      |
| ------------------------ | -------------------------------------------------------------- | ------ | -------- | ------------ |
| HTML_FILE                | Path to the index.html file used to server the root of the api | string | false    | ./index.html |
| KUBECONFIG               | Path to kubeconfig. Used to talk with Kubernetes api           | string | true     |              |
| KUBECTL_CMD              | Command to run kubectl                                         | string | true     |              |
| KUBERNETES_DASHBOARD_URL | Url to the kubernetes dashboard used to redirect               | string | false    | null         |
| STATIC_DIRECTORY         | Path to static data directory                                  | string | false    | ./static     |

## TODO

- Take `KUBECTL_CMD` and `KUBERNETES_DASHBOARD_URL` as build args in the Dockerfile
- Linting action
- Use distroless container
- Add health check endpoints
