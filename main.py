import requests as req

from requests.models import Response
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from prometheus_client import start_http_server, Gauge
import time, os

def process_request(router_ip,router_username,router_password):
    url = 'https://' + router_ip + '/rest/interface'
    req.packages.urllib3.disable_warnings(InsecureRequestWarning)
    try:
        response = req.get(url, auth=(router_username,router_password), verify=False, timeout=5)
    except urllib3.exceptions.ReadTimeoutError:
            print("Connect timeout")
    
    if response.status_code != 200:
        quit()
    
    return response.json()

def declare_prometheus_metrics(data,router_ip):

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


if __name__ == '__main__':


    router_ip = os.environ['ROUTER_IP']
    router_username = os.environ['ROUTER_USERNAME']
    router_password = os.environ['ROUTER_PASSWORD']

    # Start up the server to expose the metrics.
    start_http_server(8000)

    # init metrics
    data = process_request(router_ip,router_username,router_password)
    prom = declare_prometheus_metrics(data,router_ip)

    # Generate requests.
    while True:
        data = process_request(router_ip,router_username,router_password)
        prom_request(data,prom,router_ip)
        time.sleep(3)
