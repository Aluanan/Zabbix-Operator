from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.group import NS
from diagrams.k8s.podconfig import Secret
from diagrams.k8s.network import SVC
from diagrams.k8s.compute import STS, Deployment
from diagrams.k8s.storage import PV, PVC
from diagrams.k8s.rbac import ClusterRole, RoleBinding, ServiceAccount
from diagrams.k8s.others import CRD

with Diagram("Zabbix-Operator"):
    with Cluster("minikube-v1.9.2"):
        with Cluster("operator"):
            operatorDeployment = [ClusterRole("zabbix-operator"),
                                  RoleBinding("zabbix-operator"),
                                  ServiceAccount("zabbix-operator"),
                                  NS("operator"),
                                  Deployment("zabbix-operator"),
                                  CRD("zabbixes.monitoring.frenchtoastman.com")]
        with Cluster("zabbix"):
            zabbixInstance = [Secret("zabbix-postgres"),
                              SVC("postgres-server"),
                              SVC("zabbix-server"),
                              SVC("zabbix-web"),
                              STS("postgres-server"),
                              [PV("postgres-data"), PVC("postgres-data")],
                              Deployment("zabbix-server"),
                              Deployment("zabbix-web")]
