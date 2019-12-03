import tempfile
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


def test_builder_write_verilog_1():
    u = UnitBenchBuilder("unitbench/tests/json/example.json",
                         ExampleModule, [10])

    with tempfile.TemporaryDirectory() as tmpd:
        u.write_verilog((tmpd + "/tmp.v").__str__(), 0)
        with open(tmpd + "/tmp.v", "r") as t:
            assert(t.read() != "")
