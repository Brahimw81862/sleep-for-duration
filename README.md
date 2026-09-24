# Sleep For Duration

Sleep For Duration parses a duration string like `5s` or `2m` and suspends execution for that long.

```python
from sleep_for_duration import sleep_for_duration

sleep_for_duration("10s")
```

The library exists because sprinkling `time.sleep(5)` through scripts makes the delay opaque. A string like `5s` is self-documenting and easier to change. The trade-off is that only simple integer durations are supported: one number followed by exactly one of `s`, `m`, or `h`. Compound strings like `1m30s` are deliberately rejected.

Malformed input raises `ValueError`. The most likely edge you will hit is forgetting the unit or passing `1.5s`; both fail immediately.

Exported names: `sleep_for_duration`.
