# Video Episodes

## Episode #1 - Introduction

We check for `python` and `pip`
```bash
python --version
pip --version
```

Then we install our Naeural Edge Protocol SDK
```bash
pip install --upgrade naeural_client
```

We test the network using the `nepctl` command line interface
```bash
nepctl get nodes
```

> Starting with version 3 the `nepctl` will not require additional initial configuration as it will automatically connect and self-authenticate with the network.
> For versions 2 and below at the first run we'll be required to edit the `~/.nepctl/config` file and put in the template the credentials .

## Episode #2 - Basic connect and passively check nodes

Just create a Session and assign the heartbeat processing callback to its `on_heartbeat` parameter.

```python
from naeural_client import Session

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

## Episode #3 - Using devcontainer and self-configuration

We create a `Dockerfile` and a `devcontainer.json` file to create a development container for our project. Strting with version 


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

## Episode #4 - Filtering for target node messages



