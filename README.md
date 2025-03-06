
# Video Episodes for the ratio1's Naeural Edge Protocol SDK

## Episode #1 - Introduction

We check for `python` and `pip`
```bash
python --version
pip --version
```

Then we install our Naeural Edge Protocol SDK
```bash
pip install --upgrade ratio1
```

We test the network using the `nepctl` command line interface
```bash
nepctl get nodes
```

> Starting with version 2.6 the `nepctl` will not require additional initial configuration as it will automatically connect and self-authenticate with the network.
> For versions 2.5 and below at the first run we'll be required to edit the `~/.nepctl/config` file and put in the template the credentials .



## Episode #2 - Basic connect and passively check nodes

Just create a Session and assign the heartbeat processing callback to its `on_heartbeat` parameter.

```python
from ratio1 import Session

def hb_handler(self, session: Session, node_addr: str, heartbeat: dict):
  """
  This method processes the heartbeat messages received from the nodes.
  It is preferable to create a message handler class and define all the callbacks there.
  """
  print(f"Received heartbeat from {node_addr}")

session = Session(on_heartbeat=hb_handler)
sess.sleep(10)
sess.close()
```


---

## Episode #3 - Using devcontainer and self-configuration

We create a `Dockerfile` and a `devcontainer.json` file to create a development container for our project.
As promissed version 2.6 is here so now the configuration is done automatically by the SDK.


---

## Episode #4 - Basic Filtering

Lets modify the initial example by adding now a extra callback for payload processing and no matter if the payload is encrypted or not we can still see some basic protocol info.
```python

def payload_handler(
    session: Session, 
    node_addr : str, 
    pipeline_name : str, 
    plugin_signature : str, 
    plugin_instance : str,  
    data : Payload      
  ):
  msg = f"Received payload from {node_addr} on pipeline {pipeline_name} with plugin {plugin_signature} and instance {plugin_instance}"
  session.P(msg)
  return
...
session = Session(on_heartbeat=hb_handler, on_payload=payload_handler)
...
```


---

## Episode #5 - Advanced filtering

The so called network data is important as it actually contains the data that various decentralized applications are exchanging between each other within the ratio1 network.

For this episode we will adapt the previous episode's code to include a more advanced filtering mechanism that will allow us to filter specific plugins. 

```python
...

 if plugin_signature not in self.plugin_filter:
      msg = "Received data payload from node <{}>, pipeline '{}', plugin '{}', instance '{}' with {} bytes data".format(
        node_address, pipeline_name, plugin_signature, plugin_instance,
        len(str(payload)),
      )
      session.P(msg, color='dark')
    else:
      # this is the payload we are interested in
      network_map = payload.data.get(PAYLOAD_DATA.NETMON_CURRENT_NETWORK, {})
      nr_peers = len(network_map)
      peers = {
        v.get(PAYLOAD_DATA.NETMON_ADDRESS) : {
          'alias' :  v.get(PAYLOAD_DATA.NETMON_EEID),
          'allows' : v.get(PAYLOAD_DATA.NETMON_WHITELIST),
          'allows_me' :  session.bc_engine.contains_current_address(
            v.get(PAYLOAD_DATA.NETMON_WHITELIST)
          )
          
        } for k, v in network_map.items()
        if v.get(PAYLOAD_DATA.NETMON_STATUS_KEY) == PAYLOAD_DATA.NETMON_STATUS_ONLINE
      }
      session.P(f"Received network data from {node_address} with {nr_peers} peers:\n{json.dumps(peers, indent=2)}")

...
```


---

## Episode #6 - Prepare our own node for development deployment

Assuming you performed a 
```bash
nepctl config show
```
and you copied the node address then on the target machine:

```bash
docker run -d --rm --name r1node --pull=always -v r1vol:/edge_node/_local_cache/ naeural/edge_node:develop
# wait a few seconds for the node to start
sleep 3
docker exec r1node get_node_info
```
at this moment the SDK is not peered with the node so we need to add it. You can check on the development machine the node address by running:
```bash
nepctl get nodes --online
```
and you can see you are not peered with the new node. To add it run on the target machine:

```bash
docker exec r1node add_allowed 0xai_A2Fx1c-WI5e1eRRm-6cGxTYRD8UEZSH-iTfSeHKmlzR6 demo-sdk-ws
```
Certainly replace the above demo-sdk-ws with your own node address then on the development machine:

```bash
nepctl get nodes --online
```

You should see your node peered.
If you want to close the node then run on the node machine:

```bash
docker stop r1node
```

