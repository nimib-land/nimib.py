import inspect
import nimporter
from nimibpy import do_init, add_text, save
from nbcode import code


def init():
    frame = inspect.stack()[-1]
    do_init(frame.filename)

def text(s: str):
    print("add text block")
    add_text(s)

