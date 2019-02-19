from cffi import FFI
ffibuilder = FFI()

ffibuilder.cdef("""

    #define INDIGO_NAME_SIZE      128

    #define INDIGO_MAX_SERVERS    10

    typedef struct indigo_client indigo_client;

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
            ...;  // tells CFFI that there is more to this struct
    } indigo_client;

    typedef unsigned long int pthread_t;

    typedef struct {
            ...;
    } indigo_device;

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

    indigo_server_entry indigo_available_servers[INDIGO_MAX_SERVERS];

    extern "Python" indigo_result attach_cb(indigo_client *);

    indigo_client *indigo_build_client(char *client_name, indigo_result (*attach_callback)(indigo_client *client));

    indigo_result indigo_connect_server(const char *name, const char *host, int port, indigo_server_entry **server);

    indigo_result indigo_disconnect_server(indigo_server_entry *server);

    indigo_result indigo_start();

    """)

ffibuilder.set_source("_indigo",  r"""
    #include "indigo_bus.h"
    #include "indigo_client.h"
    indigo_client *indigo_build_client(char *client_name, indigo_result (*attach_callback)(indigo_client *client));
    indigo_result indigo_connect_server(const char *name, const char *host, int port, indigo_server_entry **server);
    indigo_result indigo_disconnect_server(indigo_server_entry *server);
    indigo_result indigo_start();

""",
  include_dirs = ['../indigo_libs'],
  library_dirs = ['../indigo_libs'],
  sources = ['indigo_py_adapter.c'],
  extra_objects = ['../indigo_libs/indigo_client.o', '../indigo_libs/indigo_client_xml.o', '../indigo_libs/indigo_bus.o', '../indigo_libs/indigo_io.o', '../indigo_libs/indigo_xml.o', '../indigo_libs/indigo_version.o', '../indigo_libs/indigo_base64.o']
)


if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
