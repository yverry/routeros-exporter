import requests as req

from requests.models import Response
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from prometheus_client import start_http_server, Gauge
import time, os

def mkt_restapi(router_ip,router_username,router_password, path):
    url = 'https://' + router_ip + '/rest/' + path
    req.packages.urllib3.disable_warnings(InsecureRequestWarning)
    try:
        response = req.get(url, auth=(router_username,router_password), verify=False, timeout=5)
    except urllib3.exceptions.ReadTimeoutError:
            print("Connect timeout")
    
    if response.status_code != 200:
        quit()
    
    return response.json()

def init_prometheus_interface_metrics(data,router_ip):

    prom = dict()
    metrics = ['fp_rx_byte','fp_tx_byte','tx_byte','rx_byte']
    # declare all metrics
    for key in metrics:
        name = 'routeros_interface_' + key
        prom[name] = Gauge(name,"RouterOS interface " + key, ['routerip','interface'])

    return prom

def prom_request(data,prom,routerip):
    metrics = {'fp_rx_byte' : 'fp-rx-byte','fp_tx_byte' : 'fp-tx-byte','tx_byte' : 'tx-byte','rx_byte' : 'rx-byte'}

    for key in data:
        for m in metrics:
            name = 'routeros_interface_' +  m      
            interface = key['name']
            value = key[metrics[m]]
            prom[name].labels(routerip=routerip,interface=interface).set(value)


def init_prometheus_cpu_metrics(data,router_ip):

    prom = dict()

    name = 'routeros_load'
    prom[name] = Gauge(name,"RouterOS CPU load " + name, ['routerip','cpu'])
    name = 'routeros_irq'
    prom[name] = Gauge(name,"RouterOS CPU IRQ " + name, ['routerip','cpu'])

    return prom

def prom_cpu_request(data,prom,routerip):

    for key in data:
        name = 'routeros_load'
        cpu = key['cpu']
        value = key['load']
        prom[name].labels(routerip=routerip,cpu=cpu).set(value)

        name = 'routeros_irq'
        cpu = key['cpu']
        value = key['irq']
        prom[name].labels(routerip=routerip,cpu=cpu).set(value)


if __name__ == '__main__':


    try:
        router_ip = os.environ['ROUTER_IP']
        router_username = os.environ['ROUTER_USERNAME']
        router_password = os.environ['ROUTER_PASSWORD']
    except KeyError as e:
        print("Fatal Error missing: " + str(e) + " variable, exiting")
        os._exit(-1)

    # PORT
    try:
        exporter_port = os.environ['PORT']
    except KeyError:
        exporter_port = 8000

    # Interval
    try:
        interval = os.environ['INTERVAL']
    except KeyError:
        interval = 30

    # Start up the server to expose the metrics.
    start_http_server(exporter_port)
    print("Running RouterOS exporter on port " + str(exporter_port) + " fetch interval is " + str(interval) + "s")

    # interface metrics
    data_interface = mkt_restapi(router_ip,router_username,router_password,'interface')
    prom_interface = init_prometheus_interface_metrics(data_interface,router_ip)

    # system/resource/cpu metrics
    data_cpu = mkt_restapi(router_ip,router_username,router_password,'system/resource/cpu')
    prom_cpu = init_prometheus_cpu_metrics(data_cpu,router_ip)


    # Generate requests.
    while True:
        # interface
        data_interface = mkt_restapi(router_ip,router_username,router_password,'interface')
        prom_request(data_interface,prom_interface,router_ip)
        # system/resource/cpu
        data_cpu = mkt_restapi(router_ip,router_username,router_password,'system/resource/cpu')
        prom_cpu_request(data_cpu,prom_cpu,router_ip)

        time.sleep(interval)
