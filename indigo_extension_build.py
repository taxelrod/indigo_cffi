from cffi import FFI
ffibuilder = FFI()

ffibuilder.cdef("""

    #define INDIGO_NAME_SIZE      128

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
            char name[INDIGO_NAME_SIZE];															///< client name
            bool is_remote;																						///< is remote client
            void *client_context;																			///< any client specific data
            indigo_result last_result;																///< result of last bus operation
            indigo_version version;																		///< client version
            indigo_enable_blob_mode_record *enable_blob_mode_records;	///< enable blob mode

            /** callback called when client is attached to the bus
             */
            indigo_result (*attach)(indigo_client *client);
            /** callback called when device broadcast property definition
             */
            ...;  // tells CFFI that there is more to this struct
    } indigo_client;

    extern "Python" indigo_result attach_cb(indigo_client *);

    indigo_client *indigo_build_client(char *client_name, indigo_result (*attach_callback)(indigo_client *client));
    """)

ffibuilder.set_source("_indigo",  r"""
    #include "indigo_bus.h"
    indigo_client *indigo_build_client(char *client_name, indigo_result (*attach_callback)(indigo_client *client));
""",
  include_dirs = ['../indigo_libs'],
  library_dirs = ['../indigo_libs'],
  sources = ['indigo_py_adapter.c'],
  extra_objects = ['../indigo_libs/indigo_client.o', '../indigo_libs/indigo_client_xml.o', '../indigo_libs/indigo_bus.o', '../indigo_libs/indigo_io.o', '../indigo_libs/indigo_xml.o', '../indigo_libs/indigo_version.o', '../indigo_libs/indigo_base64.o']
)


if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
