# indigo_cffi
## Purpose
indigo_cffi is a Python 3 interface to [INDIGO Astronomy](http://www.indigo-astronomy.org/), which provides a uniform interace
to a wide variety of cameras, filter wheels, and other hardware useful
for astronomical telescopes.
## Requirements
These prerequisites are required before installing indigo_cffi:
- [INDIGO](https://github.com/indigo-astronomy/indigo.git)
- Python 3.7 or greater (Python 3.5 will work with minor source changes)
- [CFFI](https://cffi.readthedocs.io/en/latest/)
## Installing
1. Build INDIGO from source - you will need the source in the following steps.  Build instructions are [here](http://www.indigo-astronomy.org/downloads.html).
2. The source is configured to work with indigo_cffi cloned into a
subdirectory of indigo.  This is not required, but if you make a
different choice, change `include_dirs`, `library_dirs`, and
`extra_objects` appropriately in `indigo_extension_build.py`
3. In the `indigo_cffi` directory, build the package with `python indigo_extension_build.py`
4. Set your `PYTHONPATH` to include the `indigo_cffi` directory 
## Examples
Several simple examples are provided in the `Examples` subdirectory.  To run them, you first need to start the INDIGO server.  It is easiest, but not essential, to start the server with the driver(s) you need for your hardware (the ASI driver is shown here).
```
cd indigo/build/bin
./indigo_server indigo_ccd_asi
```

- `dumpProperties.py` dumps the INDIGO properties of all devices
- `takeExposure.py [expTime]` takes an exposure of `expTime` seconds using the `ZWO ASI1600MM Pro #0` camera (this can be readily changed)
