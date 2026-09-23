"""Core implementation for Sleep For Duration.

The parser supports a single unit per string: an integer followed by one of
``s`` (seconds), ``m`` (minutes), or ``h`` (hours). The integer must be
non-negative. No compound strings like ``1m30s`` are accepted; this keeps the
parser deterministic and easy to reason about.

We choose to raise ``ValueError`` on malformed input rather than silently
treating it as zero because a bad duration string is almost certainly a bug,
and failing fast is better than sleeping for the wrong amount of time.
"""

import time
from typing import Union

# The clock function is injectable for tests. It defaults to time.sleep, which
# is the real implementation. Tests pass a fake clock that records calls.
def sleep_for_duration(
    duration: str,
    *,
    clock: callable = time.sleep,
) -> None:
    """Parse ``duration`` and suspend execution for that long.

    Args:
        duration: A string like ``"5s"``, ``"2m"``, or ``"1h"``.
            The unit must be exactly one of ``s``, ``m``, or ``h``.
            The number must be an integer and non-negative.
        clock: A callable that accepts a float number of seconds to sleep.
            Defaults to :func:`time.sleep`. Tests may pass a fake to avoid
            actually sleeping.

    Raises:
        ValueError: If ``duration`` is malformed (not a non-negative integer
            followed by a supported unit) or if the integer is negative.

    Returns:
        None
    """
    if not isinstance(duration, str):
        raise ValueError(f"duration must be str, got {type(duration).__name__}")

    if not duration:
        raise ValueError("duration must not be empty")

    # The last character is the unit. Everything before it must be an integer.
    unit = duration[-1]
    if unit not in ("s", "m", "h"):
        raise ValueError(f"unsupported unit {unit!r}; expected one of 's', 'm', 'h'")

    number_str = duration[:-1]
    if not number_str:
        raise ValueError("duration must start with a non-negative integer")

    try:
        number = int(number_str)
    except ValueError:
        raise ValueError(f"invalid integer {number_str!r} in duration") from None

    if number < 0:
        raise ValueError("duration integer must be non-negative")

    # Convert to seconds. The conversion factors are exact for these units.
    seconds = number * {"s": 1, "m": 60, "h": 3600}[unit]
    clock(seconds)
