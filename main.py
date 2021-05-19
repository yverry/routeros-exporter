import requests as req
import json

from requests.models import Response
from prometheus_client import start_http_server, Gauge
import random, time, os

def process_request(router_ip,router_username,router_password):
    url = 'https://' + router_ip + '/rest/interface'

    response = req.get(url, auth=(router_username,router_password), verify=False, timeout=5)
    if response.status_code != 200:
        quit()
    
    return response.json()

def declare_prometheus_metrics(data):

    prom = dict()
    metrics = ['fp-rx-byte','fp-tx-byte','tx-byte','rx-byte']
    # declare all metrics
    for key in data:
        name = 'routeros_' + key['name'] + '_rx_byte'
        prom[name] = Gauge(name, "rx_byte " + key['name'])
    return prom

def prom_request(data,prom):
    for key in data:
        name = 'routeros_' + key['name'] + '_rx_byte'
        print(name)
        prom[name].set(key['rx-byte'])


if __name__ == '__main__':

    router_ip = os.environ['ROUTER_IP']
    router_username = os.environ['ROUTER_USERNAME']
    router_password = os.environ['ROUTER_PASSWORD']

    # Start up the server to expose the metrics.
    start_http_server(8000)

    # init metrics
    data = process_request(router_ip,router_username,router_password)
    prom = declare_prometheus_metrics(data)

    # Generate requests.
    while True:
        data = process_request(router_ip,router_username,router_password)
        prom_request(data,prom)
        time.sleep(3)
