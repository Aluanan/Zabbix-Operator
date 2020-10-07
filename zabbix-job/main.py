from pyzabbix import ZabbixAPI
import argparse
import base64
import logging
import sys


class Monitoring(object):
    def __init__(self, username: str, passwordb64: str):
        password = base64.b64decode(passwordb64)
        self.zapi = ZabbixAPI("http://zabbix-web")
        try:
            self.zapi.login(user=username, password=password.decode())
        except Exception as e:
            logger.debug("Failure to login: ERROR: %s" % e)
            sys.exit(1)

    def add_cluster(self, nodes: list):
        if not self.zapi.hostgroup.get(filter={"name": "Kubernetes-cluster"}):
            logger.debug("Creating hostgroup")
            hostgroup = self.zapi.hostgroup.create(
                name="Kubernetes-cluster"
            )
            groupid = hostgroup['groupids'][0]
        else:
            logger.debug("Found host")
            hostgroup = self.zapi.hostgroup.get(filter={"name": "Kubernetes-cluster"})
            groupid = hostgroup[0].get('groupid')

        for node in nodes:
            if not self.zapi.host.get(filter={"host": node}):
                logger.debug("Creating host")
                if node != "postgres-server":
                    self.zapi.host.create(
                        host=node,
                        tags=[
                            {"tag": "kubernetes.io/type", "value": "database"},
                            {"tag": "prometheus/node-exporter", "value": "true"},
                            {"tag": "zabbix/agent", "value": "false"}
                        ],
                        groups=[
                            {"groupid": groupid}
                        ],
                        interfaces=[
                            {
                                "type": 1,
                                "main": 1,
                                "useip": 1,
                                "ip": node,
                                "dns": "",
                                "port": "10050"
                            }
                        ],
                        macros=[
                            {
                                "macro": "{$NODE_IP}",
                                "value": node
                            }
                        ]
                    )
                elif node == "postgres-server":
                    template = self.zapi.template.get(filter={"name": "Template DB PostgreSQL"})
                    templateid = template[0].get("templateid")
                    self.zapi.host.create(
                        host=node+"-0",
                        tags=[
                            {"tag": "kubernetes.io/type", "value": "node"},
                            {"tag": "prometheus/node-exporter", "value": "false"},
                            {"tag": "zabbix/agent", "value": "true"}
                        ],
                        groups=[
                            {"groupid": groupid}
                        ],
                        interfaces=[
                            {
                                "type": 1,
                                "main": 1,
                                "useip": 0,
                                "ip": "127.0.0.1",
                                "dns": node,
                                "port": "10050"
                            }
                        ],
                        templates=[
                            {
                                "templateid": str(templateid)
                            }
                        ]
                    )
            if node != "postgres-server":
                host = self.zapi.host.get(filter={"name": node})
                logger.debug("Found host")
                hostid = host[0].get('hostid')
                logger.debug("Searching for interface")
                interfaces = self.zapi.hostinterface.get(filter={"host": node})
                interfaceid = 1
                for interface in interfaces:
                    if interface['ip'] == node:
                        interfaceid = interface['interfaceid']
                        logger.debug("Found interface")
                if not self.zapi.item.get(filter={"key": "master", "host": node}):
                    logger.debug("Creating item")
                    self.zapi.item.create(
                        name="Prometheus Node Exporter",
                        key="master",
                        type=19,
                        value_type=4,
                        url="http://"+node+":9100/metrics",
                        delay="30s",
                        hostid=hostid,
                        key_="master",
                        interfaceid=interfaceid
                    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-user", help="Username to connect to zabbix")
    parser.add_argument("-passwd", help="Password for zabbix")
    parser.add_argument("-nodes", help="Comma string of hostnames")

    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    args = parser.parse_args()
    logger.debug("Creating Monitoring objects")
    hosts = args.nodes.split(',')

    zabbix = Monitoring(username=args.user, passwordb64=args.passwd)
    logger.debug("Adding hosts")
    zabbix.add_cluster(nodes=hosts)
    logger.debug("Cluster monitoring added")
    sys.exit(0)
