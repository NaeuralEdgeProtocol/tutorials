from ratio1 import Session, PAYLOAD_DATA, HEARTBEAT_DATA


class SimpleMessageHandler:
  
  def heartbeat_handler(self, session: Session, node_address: str, heartbeat_data: dict):
    node_alias = heartbeat_data.get(PAYLOAD_DATA.EE_ID)
    cpu_info = heartbeat_data.get(HEARTBEAT_DATA.CPU)
    session.P("Received hb from '{}' <{}> with CPU info: '{}'".format(
      node_alias, node_address, cpu_info
    ))
    return
  
  
if __name__ == '__main__':
  
  obj_handler  = SimpleMessageHandler()
  
  session = Session(
    silent=False,
    on_heartbeat=obj_handler.heartbeat_handler,
  )
  
  netdata = session.get_network_known_nodes(online_only=True)
  session.sleep(10)
  session.P(f"The online nodes are:\n{netdata.report}")
  session.close()
  
  
  