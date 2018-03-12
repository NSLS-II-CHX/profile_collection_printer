import nslsii
from bluesky import RunEngine
from bluesky.utils import get_history
RE = RunEngine(get_history())
nslsii.configure_base(get_ipython().user_ns, 'chx')
