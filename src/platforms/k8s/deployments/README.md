Mount app folder
----------------
'''
minikube mount .:/app
'''

Deploy Brightside to Kubernetes
--------------------------------
'''
kubectl apply -f .\src\platforms\kubernetes\deployments\brightside.yaml
'''