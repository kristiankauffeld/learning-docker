simple proof of concept (PoC) microservice application that utilizes docker compose with hot reloading for both services.

### Docker Compose Startup Order

In order to control the order of service startup, I've used the `healthcheck` parameter in the docker-compose file as recommended in this post: [devops.stackexchange] (https://devops.stackexchange.com/questions/12092/docker-compose-healthcheck-for-rabbitmq). This seems to be a better approach at least for the FastAPI service, but the NodeJS service uses `wait-port` package.

### Current Issues

Hot reloading for the "stem-separation" service currently doesn't work. The long-running RabbitMQ consumer seems to interfere with FastAPI's hot-reloading feature.

https://github.com/XCanG/fastapi-rabbitmq/blob/master/listener.py

https://aio-pika.readthedocs.io/en/latest/rabbitmq-tutorial/1-introduction.html

https://groups.google.com/g/rabbitmq-users/c/fSrIb6df-yc?pli=1
