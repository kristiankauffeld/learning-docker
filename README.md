simple proof of concept (PoC) microservice application that utilizes docker compose with hot reloading for both services.

### Docker Compose Startup Order

In order to control the order of service startup, I've used the `healthcheck` parameter in the docker-compose file as recommended in this post: [devops.stackexchange] (https://devops.stackexchange.com/questions/12092/docker-compose-healthcheck-for-rabbitmq). This seems to be a better approach at least for the FastAPI service, but the NodeJS service uses `wait-port` package.

### Kubernetes workflow

Why use Kubernetes? The simplest reason is to avoid vendor lock-in.
It is also worth using your local Kubernetes instance to practice deployment before embarking on a full production deployment.

Kubectl is the command line tool on our local computer we use to interact with our Kubernetes cluster.

deploy service to local Kubernetes cluster:

```sh
kubectl apply -f scripts/deploy.yaml
```

check running deployment:

```sh
kubectl get deployments
```

delete the deployment to clean up cluster:

```sh
kubectl delete -f scripts/deploy.yaml
```

### Current Issues

Hot reloading for the "stem-separation" service currently doesn't work. The long-running RabbitMQ consumer seems to interfere with FastAPI's hot-reloading feature.

https://github.com/XCanG/fastapi-rabbitmq/blob/master/listener.py

https://aio-pika.readthedocs.io/en/latest/rabbitmq-tutorial/1-introduction.html

https://groups.google.com/g/rabbitmq-users/c/fSrIb6df-yc?pli=1
