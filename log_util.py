# log_util.py
# A simple in-memory log that flushes to disk at the end of a run.

import time

_LOG_LINES: list[str] = []   # module-level buffer; cleared after each flush


def log(message: str) -> None:
    """Append a timestamped entry to the in-memory buffer and print it."""
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"
    _LOG_LINES.append(line)
    print(line)


def flush_log(path: str) -> None:
    """Write all buffered entries to path (append mode) and clear the buffer."""
    with open(path, "a") as f:
        for line in _LOG_LINES:
            f.write(line + "\n")
    _LOG_LINES.clear()
