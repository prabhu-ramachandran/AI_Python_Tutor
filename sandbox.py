import sys
import io
import contextlib
import traceback

def execute_code_safely(code):
    """
    Executes Python code and captures stdout/stderr.
    Includes basic security checks (blocking dangerous imports).
    """
    # 1. Basic Security Check
    forbidden = ["import os", "import sys", "import subprocess", "open(", "exec(", "eval("]
    for term in forbidden:
        if term in code:
            return "Security Alert: This sandbox does not allow file/system operations."

    # 2. Capture Output
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()

    try:
        with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
            # We use a shared local dict to allow variables to persist between lines in the same block
            # But for now, let's keep it stateless per run for simplicity
            exec(code, {"__builtins__": {}}) # minimal builtins for safety
    except Exception:
        # Capture the traceback if it crashes
        traceback.print_exc(file=stderr_capture)

    output = stdout_capture.getvalue()
    error = stderr_capture.getvalue()

    return output + "\n" + error if error else output
