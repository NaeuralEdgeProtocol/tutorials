from naeural_client import Session, PAYLOAD_DATA, HEARTBEAT_DATA, Payload


class SimpleMessageHandler:
  
  def __init__(
    self, 
    node_filter: str = None, 
    pipeline_filter: str = None,
    plugin_filter: str = None,
  ):
    self.node_filter = node_filter if isinstance(node_filter, list) else [node_filter]
    self.pipeline_filter = pipeline_filter if isinstance(pipeline_filter, list) else [pipeline_filter]
    self.plugin_filter = plugin_filter if isinstance(plugin_filter, list) else [plugin_filter]
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
    data: Payload
  ):
    msg = "Received data payload from node <{}>, pipeline '{}', plugin '{}', instance '{}' with {} bytes data".format(
      node_address, pipeline_name, plugin_signature, plugin_instance,
      len(str(data)),
    )
    session.P(msg, color='magenta')
    return
  
  
if __name__ == '__main__':
  
  obj_handler  = SimpleMessageHandler()
  
  session = Session(
    silent=False,
    on_heartbeat=obj_handler.heartbeat_handler,
    on_payload=obj_handler.payload_handler,
  )
  
  netdata = session.get_network_known_nodes(online_only=True)
  session.sleep(30)
  session.P(f"The online nodes are:\n{netdata.report}")
  session.close()
  
  
  