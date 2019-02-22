// Package up a few functions for easier CFFI interface
//

#include "indigo_bus.h"
#include "indigo_client.h"
#include "indigo_xml.h"
#include <string.h>


// Create and attach an indigo_client (see indigo_bus.h) with Python callbacks

static indigo_client client;

indigo_client *indigo_build_client(char *client_name, indigo_result (*attach_cb)(indigo_client *client),
				   indigo_result (*define_property_cb)(indigo_client *client, indigo_device *device, indigo_property *property, const char *message),
				   indigo_result (*update_property_cb)(indigo_client *client, indigo_device *device, indigo_property *property, const char *message),
				   indigo_result (*delete_property_cb)(indigo_client *client, indigo_device *device, indigo_property *property, const char *message),
				   indigo_result (*send_message_cb)(indigo_client *client, indigo_device *device, const char *message),
				   indigo_result (*detach_cb)(indigo_client *client)
				   )
{

  strncpy(client.name, client_name, INDIGO_NAME_SIZE);
  client.is_remote = false;
  client.client_context = NULL;
  client.last_result = INDIGO_OK;
  client.version = INDIGO_VERSION_CURRENT;
  client.enable_blob_mode_records = NULL;
  client.attach = attach_cb;
  client.define_property = define_property_cb;
  client.update_property = update_property_cb;
  client.delete_property = delete_property_cb;
  client.detach = detach_cb;
  
  indigo_attach_client(&client);
  return &client;
}

/*  This code extracted from indigo_prop_tool.c as temporary standin for later python code */

static bool print_verbose = false;
static bool change_requested = false;

void print_property_string(indigo_property *property, const char *message) {
	indigo_item *item;
	int i;
	if (print_verbose && !change_requested) {
		char perm_str[3] = "";
		switch(property->perm) {
		case INDIGO_RW_PERM:
			strcpy(perm_str, "RW");
			break;
		case INDIGO_RO_PERM:
			strcpy(perm_str, "RO");
			break;
		case INDIGO_WO_PERM:
			strcpy(perm_str, "WO");
			break;
		}

		char type_str[20] = "";
		switch(property->type) {
		case INDIGO_TEXT_VECTOR:
			strcpy(type_str, "TEXT_VECTOR");
			break;
		case INDIGO_NUMBER_VECTOR:
			strcpy(type_str, "NUMBER_VECTOR");
			break;
		case INDIGO_SWITCH_VECTOR:
			strcpy(type_str, "SWITCH_VECTOR");
			break;
		case INDIGO_LIGHT_VECTOR:
			strcpy(type_str, "LIGHT_VECTOR");
			break;
		case INDIGO_BLOB_VECTOR:
			strcpy(type_str, "BLOB_VECTOR");
			break;
		}

		char state_str[20] = "";
		switch(property->state) {
		case INDIGO_IDLE_STATE:
			strcpy(state_str, "IDLE");
			break;
		case INDIGO_ALERT_STATE:
			strcpy(state_str, "ALERT");
			break;
		case INDIGO_OK_STATE:
			strcpy(state_str, "OK");
			break;
		case INDIGO_BUSY_STATE:
			strcpy(state_str, "BUSY");
			break;
		}

		printf("Name : %s.%s (%s, %s)\nState: %s\nGroup: %s\nLabel: %s\n", property->device, property->name, perm_str, type_str, state_str, property->group, property->label);
		if (message) {
			printf("Message:\"%s\"\n", message);
		}
		printf("Items:\n");
	}

	for (i = 0; i < property->count; i++) {
		item = &(property->items[i]);
		switch (property->type) {
		case INDIGO_TEXT_VECTOR:
			printf("%s.%s.%s = \"%s\"\n", property->device, property->name, item->name, item->text.value);
			break;
		case INDIGO_NUMBER_VECTOR:
			printf("%s.%s.%s = %f\n", property->device, property->name, item->name, item->number.value);
			break;
		case INDIGO_SWITCH_VECTOR:
			if (item->sw.value)
				printf("%s.%s.%s = ON\n", property->device, property->name, item->name);
			else
				printf("%s.%s.%s = OFF\n", property->device, property->name, item->name);
			break;
		case INDIGO_LIGHT_VECTOR:
			printf("%s.%s.%s = %d\n", property->device, property->name, item->name, item->light.value);
			break;
		case INDIGO_BLOB_VECTOR:
			break;
		}
	}
	if (print_verbose) printf("\n");
}
