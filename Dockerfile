FROM python:3.12-slim

WORKDIR /code

# install kubectl
RUN apt update && apt install --no-install-recommends curl -y && rm -rf /var/lib/apt/lists/*
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/$(uname -m | grep -q 'arm64' && echo 'arm64' || echo 'amd64')/kubectl"
RUN install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl && rm -rf kubectl

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

ENV KUBECTL_CMD="/usr/local/bin/kubectl"
ENV KUBECONFIG=/data/config.conf
ENV KUBERNETES_DASHBOARD_URL=https://k8s-dashboard.mayall.local

EXPOSE 80
CMD ["fastapi", "run", "main.py", "--port", "80"]
