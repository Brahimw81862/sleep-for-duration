"""Tests for sleep_for_duration.core."""

import unittest

from sleep_for_duration import sleep_for_duration


class FakeClock:
    """Records calls instead of sleeping."""

    def __init__(self):
        self.calls = []

    def __call__(self, seconds):
        self.calls.append(seconds)


class SleepForDurationTests(unittest.TestCase):
    def test_parses_seconds(self):
        fake = FakeClock()
        sleep_for_duration("5s", clock=fake)
        self.assertEqual(fake.calls, [5.0])

    def test_parses_minutes(self):
        fake = FakeClock()
        sleep_for_duration("2m", clock=fake)
        self.assertEqual(fake.calls, [120.0])

    def test_parses_hours(self):
        fake = FakeClock()
        sleep_for_duration("1h", clock=fake)
        self.assertEqual(fake.calls, [3600.0])

    def test_zero_seconds(self):
        fake = FakeClock()
        sleep_for_duration("0s", clock=fake)
        self.assertEqual(fake.calls, [0.0])

    def test_large_number(self):
        fake = FakeClock()
        sleep_for_duration("1000000s", clock=fake)
        self.assertEqual(fake.calls, [1000000.0])

    def test_empty_string_raises(self):
        with self.assertRaises(ValueError):
            sleep_for_duration("", clock=FakeClock())

    def test_missing_number_raises(self):
        with self.assertRaises(ValueError):
            sleep_for_duration("s", clock=FakeClock())

    def test_non_integer_raises(self):
        with self.assertRaises(ValueError):
            sleep_for_duration("1.5s", clock=FakeClock())

    def test_negative_number_raises(self):
        with self.assertRaises(ValueError):
            sleep_for_duration("-1s", clock=FakeClock())

    def test_unsupported_unit_raises(self):
        with self.assertRaises(ValueError):
            sleep_for_duration("1d", clock=FakeClock())

    def test_non_string_raises(self):
        with self.assertRaises(ValueError):
            sleep_for_duration(5, clock=FakeClock())

    def test_clock_not_called_on_error(self):
        fake = FakeClock()
        with self.assertRaises(ValueError):
            sleep_for_duration("bad", clock=fake)
        self.assertEqual(fake.calls, [])


if __name__ == "__main__":
    unittest.main()
