# Model service
This repository contains the service through which we serve our model.

# Ussage
```sh
# Clone repository 
git clone git@github.com:remla25-team13/model-service.git
cd model-service

# Build docker image
docker build -t model-service .

# Run the image
docker run -it --rm -p 8080:8080 model-service
```

Or, you can use the [hosted image](https://github.com/remla25-team13/model-service/pkgs/container/model-service).
```sh
# Pull image
docker pull ghcr.io/remla25-team13/model-service:0.1.0

# Run image
docker run -it --rm -p 8080:8080 ghcr.io/remla25-team13/model-service:0.1.0
```
