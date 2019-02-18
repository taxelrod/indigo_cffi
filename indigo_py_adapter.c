// Package up a few functions for easier CFFI interface
//

#include "indigo_bus.h"
#include "indigo_client.h"
#include "indigo_xml.h"
#include <string.h>

/*
indigo_server_entry *indigo_adapter_connect_server(char *hostname, int port) {
  
  indigo_server_entry *server;
  indigo_result result;
  result = indigo_connect_server(hostname, hostname, port, &server);
  return(server);
}
*/

// Create and attach an indigo_client (see indigo_bus.h) with Python callbacks

static indigo_client client;

indigo_client *indigo_build_client(char *client_name, indigo_result (*attach_callback)(indigo_client *client))
{

  strncpy(client.name, client_name, INDIGO_NAME_SIZE);
  client.is_remote = false;
  client.client_context = NULL;
  client.last_result = INDIGO_OK;
  client.version = INDIGO_VERSION_CURRENT;
  client.enable_blob_mode_records = NULL;
  client.attach = attach_callback;
  indigo_attach_client(&client);
  return &client;
}
