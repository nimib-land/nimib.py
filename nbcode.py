import ast
import contextlib
import re
import textwrap
import traceback
from typing import Iterable, Optional
from io import StringIO 
import sys
import nimporter # when called from nb this is not necessary
from nimibpy import add_code

_SPACES_RE = re.compile("\\s*")
_EMPTY_LINE_RE = re.compile("\\s*\n")


@contextlib.contextmanager
def code():
    """Use in a `with` block to show and execute code while capturing the output.
    """
    # adapted from streamlit's st.echo

    try:
        # Get stack frame *before* running the echoed code. The frame's
        # line number will point to the `st.echo` statement we're running.
        frame = traceback.extract_stack()[-3]
        filename, start_line = frame.filename, frame.lineno

        # Read the file containing the source code of the echoed statement.
        with open_python_file(filename) as source_file:
            source_lines = source_file.readlines()

        # Use ast to parse the Python file and find the code block to display
        root_node = ast.parse("".join(source_lines))
        line_to_node_map = {}

        def collect_body_statements(node):
            if not hasattr(node, "body"):
                return
            for child in node.body:
                line_to_node_map[child.lineno] = child
                collect_body_statements(child)

        collect_body_statements(root_node)

        # In AST module the lineno (line numbers) are 1-indexed,
        # so we decrease it by 1 to lookup in source lines list
        echo_block_start_line = line_to_node_map[start_line].body[0].lineno - 1
        echo_block_end_line = line_to_node_map[start_line].end_lineno
        lines_to_display = source_lines[echo_block_start_line:echo_block_end_line]

        code_string = textwrap.dedent("".join(lines_to_display))

        _stdout = sys.stdout
        sys.stdout = StringIO()
        yield
        code_output = sys.stdout.getvalue()
        sys.stdout = _stdout

        #print("add code block")
        #print("code string:", code_string)
        #print("code output:", code_output)
        add_code(code_string, code_output)

    except FileNotFoundError as err:
        print("Unable to display code. %s" % err)


def _get_initial_indent(lines: Iterable[str]) -> int:
    """Return the indent of the first non-empty line in the list.
    If all lines are empty, return 0.
    """
    for line in lines:
        indent = _get_indent(line)
        if indent is not None:
            return indent

    return 0


def _get_indent(line: str) -> Optional[int]:
    """Get the number of whitespaces at the beginning of the given line.
    If the line is empty, or if it contains just whitespace and a newline,
    return None.
    """
    if _EMPTY_LINE_RE.match(line) is not None:
        return None

    match = _SPACES_RE.match(line)
    return match.end() if match is not None else 0


def open_python_file(filename):
    """Open a read-only Python file taking proper care of its encoding.

    In Python 3, we would like all files to be opened with utf-8 encoding.
    However, some author like to specify PEP263 headers in their source files
    with their own encodings. In that case, we should respect the author's
    encoding.
    """
    import tokenize

    if hasattr(tokenize, "open"):  # Added in Python 3.2
        # Open file respecting PEP263 encoding. If no encoding header is
        # found, opens as utf-8.
        return tokenize.open(filename)
    else:
        return open(filename, "r", encoding="utf-8")
