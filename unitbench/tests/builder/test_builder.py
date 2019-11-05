import pytest
import io
from ...testbuilder import UnitBenchBuilder
from ..modules.example import ExampleModule


def test_builder_example_1():
    s = io.StringIO("")
    u = UnitBenchBuilder("unitbench/tests/json/example.json",
                         ExampleModule, [10])

    u._gen_verilog_in_stream(s, 0)

    s.seek(0)
    assert(s.read() != "")
