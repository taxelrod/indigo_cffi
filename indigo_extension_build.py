# This file is part of indigo_cffi.
#
# Developed for the LSST Telescope and Site Systems.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from cffi import FFI
ffibuilder = FFI()

ffibuilder.cdef("""

    #define INDIGO_NAME_SIZE      128

    #define INDIGO_VALUE_SIZE     512

    #define INDIGO_MAX_SERVERS    10

    typedef int indigo_glock;

    typedef struct indigo_client indigo_client;

    typedef struct indigo_device indigo_device;

    typedef enum {
            INDIGO_OK = 0,              ///< success
            INDIGO_FAILED,              ///< unspecified error
            INDIGO_TOO_MANY_ELEMENTS,   ///< too many clients/devices/properties/items etc.
            INDIGO_LOCK_ERROR,          ///< mutex lock error
            INDIGO_NOT_FOUND,           ///< unknown client/device/property/item etc.
            INDIGO_CANT_START_SERVER,   ///< network server start failure
            INDIGO_DUPLICATED						///< duplicated items etc.
    } indigo_result;

    typedef enum {
            INDIGO_VERSION_NONE			= 0x0000, ///< undefined version
            INDIGO_VERSION_LEGACY		= 0x0107, ///< INDI compatible version
            INDIGO_VERSION_2_0			= 0x0200,  ///< INDIGO version
            INDIGO_VERSION_CURRENT		= 0x0200  ///< INDIGO version
    } indigo_version;

    typedef enum {
            INDIGO_ENABLE_BLOB_ALSO,
            INDIGO_ENABLE_BLOB_NEVER,
            INDIGO_ENABLE_BLOB_URL
    } indigo_enable_blob_mode;

    typedef struct indigo_enable_blob_mode_record {
            char device[INDIGO_NAME_SIZE];				///< device name
            char name[INDIGO_NAME_SIZE];					///< property name
            indigo_enable_blob_mode mode;					///< mode
            struct indigo_enable_blob_mode_record *next; ///< next record
    } indigo_enable_blob_mode_record;

    /** Property state.
     */
    typedef enum {
            INDIGO_IDLE_STATE = 0,      ///< property is passive (unused by INDIGO)
            INDIGO_OK_STATE,            ///< property is in correct state or if operation on property was successful
            INDIGO_BUSY_STATE,          ///< property is transient state or if operation on property is pending
            INDIGO_ALERT_STATE          ///< property is in incorrect state or if operation on property failed
    } indigo_property_state;

    /** Property data type.
     */
    typedef enum {
            INDIGO_TEXT_VECTOR = 1,     ///< strings of limited width
            INDIGO_NUMBER_VECTOR,       ///< float numbers with defined min, max values and increment
            INDIGO_SWITCH_VECTOR,       ///< logical values representing “on” and “off” state
            INDIGO_LIGHT_VECTOR,        ///< status values with four possible values INDIGO_IDLE_STATE, INDIGO_OK_STATE, INDIGO_BUSY_STATE and INDIGO_ALERT_STATE
            INDIGO_BLOB_VECTOR          ///< binary data of any type and any length
    } indigo_property_type;

    /** Property access permission.
     */
    typedef enum {
            INDIGO_RO_PERM = 1,         ///< read-only
            INDIGO_RW_PERM,             ///< read-write
            INDIGO_WO_PERM              ///< write-only
    } indigo_property_perm;

    /** Switch behaviour rule.
     */
    typedef enum {
            INDIGO_ONE_OF_MANY_RULE = 1,///< radio button group like behaviour with one switch in "on" state
            INDIGO_AT_MOST_ONE_RULE,    ///< radio button group like behaviour with none or one switch in "on" state
            INDIGO_ANY_OF_MANY_RULE     ///< checkbox button group like behaviour
    } indigo_rule;

    /** Property item definition.
     */
    typedef struct {/* there is no .name =  because of g++ C99 bug affecting string initialier */
            char name[INDIGO_NAME_SIZE];        ///< property wide unique item name
            char label[INDIGO_VALUE_SIZE];      ///< item description in human readable form
            char hints[INDIGO_VALUE_SIZE];			///< item GUI hints
            union {
                    /** Text property item specific fields.
                     */
                    struct {
                            char value[INDIGO_VALUE_SIZE];  ///< item value (for text properties)
                    } text;
                    /** Number property item specific fields.
                     */
                    struct {/* there is no .name =  because of g++ C99 bug affecting string initialier */
                            char format[INDIGO_VALUE_SIZE]; ///< item format (for number properties)
                            double min;                     ///< item min value (for number properties)
                            double max;                     ///< item max value (for number properties)
                            double step;                    ///< item increment value (for number properties)
                            double value;                   ///< item value (for number properties)
                            double target;									///< item target value (for number properties)
                    } number;
                    /** Switch property item specific fields.
                     */
                    struct {
                            bool value;                     ///< item value (for switch properties)
                    } sw;
                    /** Light property item specific fields.
                     */
                    struct {
                            indigo_property_state value;    ///< item value (for light properties)
                    } light;
                    /** BLOB property item specific fields.
                     */
                    struct {
                            char format[INDIGO_NAME_SIZE];  ///< item format (for blob properties), known file type suffix like ".fits" or ".jpeg"
                            char url[INDIGO_VALUE_SIZE];		///< item URL on source server
                            long size;                      ///< item size (for blob properties) in bytes
                            void *value;                    ///< item value (for blob properties)
                    } blob;
            };
    } indigo_item;

    /** Property definition.
     */
    typedef struct {
            char device[INDIGO_NAME_SIZE];      ///< system wide unique device name
            char name[INDIGO_NAME_SIZE];        ///< device wide unique property name
            char group[INDIGO_NAME_SIZE];       ///< property group in human readable form (presented as a tab or a subtree in GUI
            char label[INDIGO_VALUE_SIZE];      ///< property description in human readable form
            char hints[INDIGO_VALUE_SIZE];			///< property GUI hints
            indigo_property_state state;        ///< property state
            indigo_property_type type;          ///< property type
            indigo_property_perm perm;          ///< property access permission
            indigo_rule rule;                   ///< switch behaviour rule (for switch properties)
            short version;                      ///< property version INDIGO_VERSION_NONE, INDIGO_VERSION_LEGACY or INDIGO_VERSION_2_0
            bool hidden;                        ///< property is hidden/unused by  driver (for optional properties)
            int count;                          ///< number of property items
            indigo_item items[];                ///< property items
    } indigo_property;

/** Client structure definition
 */
    typedef struct indigo_client {
            char name[INDIGO_NAME_SIZE];
            bool is_remote;
            void *client_context;
            indigo_result last_result;
            indigo_version version;
            indigo_enable_blob_mode_record *enable_blob_mode_records;	///< enable blob mode

            /** callback called when client is attached to the bus
             */
            indigo_result (*attach)(indigo_client *client);
            /** callback called when device broadcast property definition
             */
            indigo_result (*define_property)(indigo_client *client, indigo_device *device, indigo_property *property, const char *message);
            /** callback called when device broadcast property value change
             */
            indigo_result (*update_property)(indigo_client *client, indigo_device *device, indigo_property *property, const char *message);
            /** callback called when device broadcast property removal
             */
            indigo_result (*delete_property)(indigo_client *client, indigo_device *device, indigo_property *property, const char *message);
            /** callback called when device broadcast a message
             */
            indigo_result (*send_message)(indigo_client *client, indigo_device *device, const char *message);
            /** callback called when client is detached from the bus
             */
            indigo_result (*detach)(indigo_client *client);
    } indigo_client;

    typedef struct indigo_device {
            char name[INDIGO_NAME_SIZE];        ///< device name
            indigo_glock lock;                  ///< device global lock
            bool is_remote;                     ///< is remote device
            uint16_t gp_bits;                   ///< general purpose bits for driver specific usage
            void *device_context;               ///< any device specific data
            void *private_data;                 ///< private data
            indigo_device *master_device;       ///< if the device provides many logical devices, this must point to one of the locical devices, otherwise is safe to be NULL
            indigo_result last_result;          ///< result of last bus operation
            indigo_version version;             ///< device version

            /** callback called when device is attached to bus
             */
            indigo_result (*attach)(indigo_device *device);
            /** callback called when client broadcast enumerate properties request on bus, device and name elements of property can be set NULL to address all
             */
            indigo_result (*enumerate_properties)(indigo_device *device, indigo_client *client, indigo_property *property);
            /** callback called when client broadcast property change request
             */
            indigo_result (*change_property)(indigo_device *device, indigo_client *client, indigo_property *property);
            /** callback called when client broadcast enableBLOB mode change request
             */
            indigo_result (*enable_blob)(indigo_device *device, indigo_client *client, indigo_property *property, indigo_enable_blob_mode mode);
            /** callback called when device is detached from the bus
             */
            indigo_result (*detach)(indigo_device *device);
    } indigo_device;

    typedef unsigned long int pthread_t;

    typedef struct {
            char name[INDIGO_NAME_SIZE];            ///< service name
            char host[INDIGO_NAME_SIZE];            ///< server host name
            int port;                               ///< server port
            pthread_t thread;                       ///< client thread ID
            bool thread_started;                    ///< client thread started/stopped
            int socket;                             ///< stream socket
            indigo_device *protocol_adapter;        ///< server protocol adapter
            char last_error[256];		    ///< last error reported within client thread
    } indigo_server_entry;


    extern "Python" indigo_result attach_cb(indigo_client *);

    extern "Python" indigo_result define_property_cb(indigo_client *client, indigo_device *device, indigo_property *property, const char *message);

    extern "Python" indigo_result update_property_cb(indigo_client *client, indigo_device *device, indigo_property *property, const char *message);

    extern "Python" indigo_result delete_property_cb(indigo_client *client, indigo_device *device, indigo_property *property, const char *message);

    extern "Python" indigo_result send_message_cb(indigo_client *client, indigo_device *device, const char *message);

    extern "Python" indigo_result detach_cb(indigo_client *);

    indigo_client *indigo_build_client(char *client_name, indigo_result (*attach_callback)(indigo_client *client),
				   indigo_result (*define_property_cb)(indigo_client *client, indigo_device *device, indigo_property *property, const char *message),
				   indigo_result (*update_property_cb)(indigo_client *client, indigo_device *device, indigo_property *property, const char *message),
				   indigo_result (*delete_property_cb)(indigo_client *client, indigo_device *device, indigo_property *property, const char *message),
				   indigo_result (*send_message_cb)(indigo_client *client, indigo_device *device, const char *message),
				   indigo_result (*detach_cb)(indigo_client *client)
                                   );

    indigo_result indigo_connect_server(const char *name, const char *host, int port, indigo_server_entry **server);

    indigo_result indigo_disconnect_server(indigo_server_entry *server);

    indigo_result indigo_start();

    void print_property_string(indigo_property *property, const char *message);

    """)

ffibuilder.set_source("_indigo",  r"""
    #include "indigo_bus.h"
    #include "indigo_client.h"
    indigo_client *indigo_build_client(char *client_name, indigo_result (*attach_callback)(indigo_client *client),
				   indigo_result (*define_property_cb)(indigo_client *client, indigo_device *device, indigo_property *property, const char *message),
				   indigo_result (*update_property_cb)(indigo_client *client, indigo_device *device, indigo_property *property, const char *message),
				   indigo_result (*delete_property_cb)(indigo_client *client, indigo_device *device, indigo_property *property, const char *message),
				   indigo_result (*send_message_cb)(indigo_client *client, indigo_device *device, const char *message),
				   indigo_result (*detach_cb)(indigo_client *client)
                                   );
    indigo_result indigo_connect_server(const char *name, const char *host, int port, indigo_server_entry **server);
    indigo_result indigo_disconnect_server(indigo_server_entry *server);
    indigo_result indigo_start();
    void print_property_string(indigo_property *property, const char *message);
    """,
  include_dirs = ['../indigo_libs'],
  library_dirs = ['../indigo_libs'],
  sources = ['indigo_py_adapter.c'],
  extra_objects = ['../indigo_libs/indigo_client.o', '../indigo_libs/indigo_client_xml.o', '../indigo_libs/indigo_bus.o', '../indigo_libs/indigo_io.o', '../indigo_libs/indigo_xml.o', '../indigo_libs/indigo_version.o', '../indigo_libs/indigo_base64.o']
)


if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
