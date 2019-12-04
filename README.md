# Hyperledger Aries Cloud Agent - Webhook Receiver

The [Hyperledger Aries Cloud Agent - Python (ACA-Py)](https://github.com/hyperledger/aries-cloudagent-python/tree/01fc73be644439fa27ab43089353859f08517ba2) currently requires the ACA-Py controller to host several webhook endpoints in order to receive updates about the agents state as described [here](https://github.com/hyperledger/aries-cloudagent-python/blob/01fc73be644439fa27ab43089353859f08517ba2/AdminAPI.md). This introduces a problem for mobile ACA-Py controller clients since it is not possible to expose such endpoints.

This repository aims to solve this problem 'the dirty way' by placing another component (called Webhook Receiver) in between ACA-Py and the Controller. The Webhook Receiver exposes the required webhook endpoints and records the requests made by ACA-Py. It also exposes an endpoint and websocket interface to get the recorded messages that the Controller call to process the messages.

#### A note about the websocket
Whenever a client opens a websocket connection, **all** in-memory messages that the client has missed so far will be send in the order they came in. (**TODO -> create cli flag to make it optional**) All new messages will be forwarded directly as long as the websocket connection lives. Whenever the connection is broken we'll start writing into memory again until the next time the client connects.


## Setup

### Docker Compose
The `docker-compose.yml` file contains a Alice - Faber test setup where both Alice and Faber have their own Webhook Receiver instance. Just run:
```bash
docker-compose build
docker-compose run
# and when you're done
docker-compose down
```

You can now connect to the various components through the following adresses:


**Alice**
Swagger UI: `http://127.0.0.1:8002`
Webhook Receiver (get new messages): `http://127.0.0.1:8080/new_messages`
Webhook Receiver (websocket): `http://127.0.0.1:8080/ws`

**Faber**
Swagger UI: `http://127.0.0.1:7002`
Webhook Receiver (get new messages): `http://127.0.0.1:7080/new_messages`
Webhook Receiver (websocket): `http://127.0.0.1:7080/ws`

### Docker
If you prefer a single container version.

```bash
docker build -t webhook-receiver .
docker run -p 8080:8080 webhook-receiver 
```

### Manual
```bash
# make sure you have virtualenv
pip install virtualenv # or pip3 install virtualenv

# create a virtual environment
virtualenv --python=python3.7 ./webhook-receiver-env

# load it
source ./webhook-receiver-env/bin/activate

# install dependencies
pip install -r requirements.txt
```