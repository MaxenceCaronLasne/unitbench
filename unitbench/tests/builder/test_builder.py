import pytest
import io
from ...testbuilder import UnitBenchBuilder
from ..modules.example import ExampleModule


@pytest.fixture
def unitbenchbuilder():
    return UnitBenchBuilder("unitbench/tests/json/example.json",
                            ExampleModule, [10])


@pytest.fixture
def unitbenchbuilder_genvcd():
    return UnitBenchBuilder("unitbench/tests/json/example.json",
                            ExampleModule, [10], gen_vcd=True)


@pytest.fixture
def unitbenchbuilder_bad():
    return UnitBenchBuilder("unitbench/tests/json/bad_example.json",
                            ExampleModule, [10], gen_vcd=True)


def test_builder_gen_verilog_in_stream_1(unitbenchbuilder):
    s = io.StringIO("")
    u = unitbenchbuilder

    u._gen_verilog_in_stream(s, 0)

    s.seek(0)
    assert(s.read() != "")


def test_builder_write_verilog_1(unitbenchbuilder, tmpdir):
    u = unitbenchbuilder

    u.write_verilog(tmpdir + "/tmp.v", 0)
    with open(tmpdir + "/tmp.v", "r") as t:
        assert(t.read() != "")


def test_vcd_name_none(unitbenchbuilder):
    u = unitbenchbuilder

    res = u._get_vcd_name("testname", "tag", ".")

    assert res is None


def test_vcd_name_current_dir(unitbenchbuilder_genvcd):
    u = unitbenchbuilder_genvcd

    res = u._get_vcd_name("testname", "tag", ".")

    assert res == "./testname_tag.vcd"


def test_vcd_name_outdir(unitbenchbuilder_genvcd):
    u = unitbenchbuilder_genvcd

    res = u._get_vcd_name("testname", "tag", "outdir1/outdir2")

    assert res == "outdir1/outdir2/testname_tag.vcd"


def test_simulation_example(unitbenchbuilder_genvcd):
    u = unitbenchbuilder_genvcd

    u.simulate_and_assert()


@pytest.mark.xfail
def test_simulation_bad_example(unitbenchbuilder_bad):
    u = unitbenchbuilder_bad

    u.simulate_and_assert()
