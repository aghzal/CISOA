from kubernetes import client, config
from controller.create_update_from_yaml import create_from_yaml, FailToCreateError
import os
import yaml
import io

try:
    config.load_incluster_config()
    print("inside cluster")
except:
    print("outside cluster")
    config.load_kube_config()

def create_client_objects(client_name, email_admin):
    cluster_domain = os.environ.get("CLUSTER_DOMAIN")
    if cluster_domain:
        print(f"CLUSTER_DOMAIN {cluster_domain}")
    with open("template/client_template.yaml") as f:
        data = f.read()
        if cluster_domain:
            data = data.replace("%CLUSTER_DOMAIN%", cluster_domain)
        data = data.replace("%CLIENT_NAME%", client_name)
        data = data.replace("%EMAIL_ADMIN%", email_admin)
        yml_document_all = yaml.safe_load_all(io.StringIO(data))
        print(f"Start creating k8s objects for {client_name}/{email_admin}")
        try:
            create_from_yaml(client.ApiClient(), yaml_objects=yml_document_all, namespace="default")
        except FailToCreateError as e:
            print("failed to create k8s objects:", e)
        print(f"Done creating k8s objects for {client_name}/{email_admin}")

