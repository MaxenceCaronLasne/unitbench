import pytest
import io
from ...testbuilder import UnitBenchBuilder
from ..modules.example import ExampleModule


def test_builder_gen_verilog_in_stream_1():
    s = io.StringIO("")
    u = UnitBenchBuilder("unitbench/tests/json/example.json",
                         ExampleModule, [10])

    u._gen_verilog_in_stream(s, 0)

    s.seek(0)
    assert(s.read() != "")


def test_builder_write_verilog_1(tmpdir):
    u = UnitBenchBuilder("unitbench/tests/json/example.json",
                         ExampleModule, [10])

    u.write_verilog(tmpdir + "/tmp.v", 0)
    with open(tmpdir + "/tmp.v", "r") as t:
        assert(t.read() != "")
