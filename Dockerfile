FROM python:3.13-slim-bullseye

ARG KUBECONFIG=/data/config.conf

WORKDIR /code

# install kubectl
RUN apt update && apt install --no-install-recommends -y curl \
    && curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/$(uname -m | grep -q 'arm64' && echo 'arm64' || echo 'amd64')/kubectl" \
    && install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl \
    && rm -rf /var/lib/apt/lists/* kubectl

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

ENV KUBECTL_CMD="/usr/local/bin/kubectl"
ENV KUBECONFIG=$KUBECONFIG

EXPOSE 80
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
