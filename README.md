BrightSide
==========

BrightSide is a simple tool for proxing Selenium grid sessions. It's designed for running browser containers in a Kubernetes cluster, but it can be extended for proxying any Selenium grid session.

## Usage

### Python 3
```bash
pip install -r requirements.txt
python app.py
```

### Docker 
**TBD**

## Supported platforms

- **Selenium grid** (not very useful, but OK as a proof of concept)
- **Docker** - creating and managing containers with browsers
- **Kubernetes** - Run Brightside pod in a Kubernetes cluster and it will create and manage browser pods on-demand

## TODO

- [ ] Error handling
- [ ] Parametrized configuration
- [ ] Tests
- [ ] Logging
- [ ] App dockerization

## Contributing

Feel free to contribute by creating issues and pull requests.
That's my pet project, so I'm not sure how much time I can spend on it, but I'll do my best to review and merge your PRs.

