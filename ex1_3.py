import json
from naeural_client import Session, PAYLOAD_DATA, HEARTBEAT_DATA, Payload


class SimpleMessageHandler:
  
  def __init__(
    self, 
    node_filter: str = None,  # for later episodes
    pipeline_filter: str = None,  # for later episodes
    plugin_filter: str = None, 
  ):
    self.node_filter = node_filter if isinstance(node_filter, list) else [node_filter]
    self.pipeline_filter = pipeline_filter if isinstance(pipeline_filter, list) else [pipeline_filter]


    if isinstance(plugin_filter, str):
      plugin_filter = [plugin_filter.upper()]
    elif isinstance(node_filter, list):
      plugin_filter = [x.upper() for x in plugin_filter]
    else:
      raise ValueError("Invalid plugin_filter")
    self.plugin_filter = plugin_filter 
    return
  
  def heartbeat_handler(self, session: Session, node_address: str, heartbeat_data: dict):
    node_alias = heartbeat_data.get(PAYLOAD_DATA.EE_ID)
    cpu_info = heartbeat_data.get(HEARTBEAT_DATA.CPU)
    session.P("Received hb from '{}' <{}> with CPU info: '{}'".format(
      node_alias, node_address, cpu_info
    ))
    return
  
  def payload_handler(
    self,
    session: Session,
    node_address: str,
    pipeline_name: str,
    plugin_signature: str,
    plugin_instance: str,
    payload: Payload
  ):
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
    return
  
  
if __name__ == '__main__':
  
  obj_handler  = SimpleMessageHandler(plugin_filter="NET_MON_01")
  
  session = Session(
    silent=False,
    on_heartbeat=obj_handler.heartbeat_handler,
    on_payload=obj_handler.payload_handler,
  )
  
  netdata = session.get_network_known_nodes(online_only=True)
  session.sleep(30)
  session.P(f"The online nodes are:\n{netdata.report}")
  session.close()
  
  
  