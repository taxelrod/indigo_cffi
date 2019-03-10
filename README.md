# indigo_cffi
## Purpose
indigo_cffi is a Python 3 interface to [INDIGO Astronomy]
(http://www.indigo-astronomy.org/), which provides a uniform interace
to a wide variety of cameras, filter wheels, and other hardware useful
for astronomical telescopes.
## Requirements
These prerequisites are required before installing indigo_cffi:
- [INDIGO] (https://github.com/indigo-astronomy/indigo.git)
- Python 3.7 or greater (Python 3.5 will work with minor source changes)
- [CFFI] (https://cffi.readthedocs.io/en/latest/)
- [xml.etree.ElementTree] (https://docs.python.org/3.7/library/xml.etree.elementtree.html)
## Installing
1. Build INDIGO from source - you will need the source in the following steps
2. The source is configured to work with indigo_cffi cloned into a
subdirectory of indigo.  This is not required, but if you make a
different choice, change `include_dirs`, `library_dirs`, and
`extra_objects` appropriately in `indigo_extension_build.py`
3. In the indigo_cffi directory, build the package with `python indigo_extension_build.py`
## Examples
