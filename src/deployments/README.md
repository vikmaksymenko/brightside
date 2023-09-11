Mount app folder
----------------
'''
minikube mount .:/app
'''

Deploy Brightside to Kubernetes
--------------------------------
'''
kubectl apply -f .\src\deployments\brightside.yaml
'''