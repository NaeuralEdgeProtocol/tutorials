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



