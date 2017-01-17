#from cassandra.cluster import Cluster
from flask import Flask
import subprocess

app = Flask(__name__)

def get_containers(basename, template=None):
    if not template:
        template = '{base}\d'
    try:
        melded = template.format(base=basename)
    except Exception as e:
        print('Incorrect template', e)
        return None
        
    containers = subprocess.Popen("sudo docker ps -f name=\"^/{name}$\" -q".format(name=melded), shell=True, stdout=subprocess.PIPE).stdout.read()
    return containers.decode().split('\n')[:-1]

def get_container_ip(container_name):
    try:
        return subprocess.Popen("sudo docker inspect --format '{{ .NetworkSettings.IPAddress }}' %s"%container_name, shell=True, stdout=subprocess.PIPE).stdout.read().decode().replace('\n','')
    except:
        return None

def get_cluster(basename, template=None):
    return [get_container_ip(container) for container in get_containers(basename) if container] 
