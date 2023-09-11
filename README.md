BrightSide
==========

BrightSide is a simple stateless service for running browser containers in Kubernetes. It can be used as a Selenium grid replacement as a part of your testing infrastructure.

## Usage

### Python 3.9+ (for Selenium grid and Docker only)
```bash
pip install -r requirements.txt
python app.py
```

### Kubernetes

1. Deploy Brightside pod to your Kubernetes cluster. 
    ```bash
    kubectl apply -f src/platforms/k8s/deployments/brightside.yaml
    ```
2. Create a service for Brightside pod or connect to it from the inside of the cluster.

### Docker 
```
docker run -it --rm -p 4444:4444 -v //var/run/docker.sock:/var/run/docker.sock --name brightside  vikmaksimenko/brightside:0.1 --platform docker --host $YOUR_HOST_OR_IP
```

## Browser images 
Right now, it supports only [standalone-chrome](https://hub.docker.com/r/selenium/standalone-chrome).
**TBD**

## TODO

- [ ] Error handling
- [ ] Browser images
- [ ] Tests
- [ ] Logging
- [ ] Helm chart

## Contributing

Feel free to contribute by creating issues and pull requests.
That's my pet project, so I'm not sure how much time I can spend on it, but I'll do my best to review and merge your PRs.

