# kubernetes-dashboard-token-api

Returns html but still

When running locally, the target kube config needs passed in as `/data/config.conf` to the container. In kubernetes, the context is already available

## Usage

The bearer-token-api requires a kube config

```sh
fastapi dev main.py
```

### Docker

```sh
# build the image
docker build -t aidanwallace/k8s-dashboard-token-api -f bearer-token-api/Dockerfile bearer-token-api

# run the image
docker run --rm -v -d <kube config location>:/data/config.conf -p 8082:80 aidanwallace/k8s-dashboard-token-api
# example: 'docker run --rm -v -d ./.cache/config.conf:/data/config.conf -p 8082:80 aidanwallace/k8s-dashboard-token-api'

```

## Env

| key                      | description                                      | type   | required | default |
| ------------------------ | ------------------------------------------------ | ------ | -------- | ------- |
| KUBECTL_CMD              | Command to run kubectl                           | string | true     |         |
| KUBERNETES_DASHBOARD_URL | Url to the kubernetes dashboard used to redirect | string | true     |         |

