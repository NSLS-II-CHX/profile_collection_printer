import nslsii
from bluesky import RunEngine
RE= RunEngine()
RE.md = {}
nslsii.configure_base(get_ipython().user_ns, 'chx')

