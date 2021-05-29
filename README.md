# RouterOS Restful API

## Setup

You need to create a user on routerOS (>7.1):

```
/user group
add name=prometheus policy=read,winbox,api,rest-api,!local,!telnet,!ssh,!ftp,!reboot,!write,!policy,!test,!password,!web,!sniff,!sensitive,!romon,!dude,!tikapp
add group=prometheus name=prometheus
````

You also need to `www-ssl` [enable](https://help.mikrotik.com/docs/display/ROS/REST+API)

## Docker

```
routerosapi:
    image: python-routeros
    restart: always
    environment:
        - ROUTER_IP=<your ROUTERIP>
        - ROUTER_USERNAME=<your prometheus username>
        - ROUTER_PASSWORD=<your super secret password>
```