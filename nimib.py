import inspect
import nimporter
from nimibpy import do_init, add_text, add_html, save, use_pyscript
from nbcode import code


def init(pyscript=False):
    frame = inspect.stack()[-1]
    do_init(frame.filename)
    if pyscript:
        use_pyscript()

def text(s: str):
    print("add text block")
    add_text(s)

def html(s: str):
    print("add html block")
    add_html(s)

