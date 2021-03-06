# RouterOS Prometheus Exporter



## Setup

You need to create a user on routerOS (>7.1):

```
/user group
add name=prometheus policy=api,rest-api,!local,!telnet,!ssh,!ftp,!reboot,!write,!policy,!test,!password,!web,!sniff,!sensitive,!romon,!dude,!tikapp
/user
add group=prometheus name=prometheus password=<your super secret password>
````

You also need `www-ssl` [enable](https://help.mikrotik.com/docs/display/ROS/REST+API)

## Docker

On docker hub:

```
docker pull yverry/routeros-exporter
```

docker-compose:

```
routeros-exporter:
    image: yverry/routeros-exporter
    restart: always
    environment:
        - ROUTER_IP=<your ROUTERIP>
        - ROUTER_USERNAME=<your prometheus username>
        - ROUTER_PASSWORD=<your super secret password>
```
### build

simply use `make build`

## Metrics

Today thoose metrics was fetched by this exporter:
* interfaces
  * tx
  * rx
  * fastTrack 
* cpu 
  * load
  * irq
