import pytest
from ...testmodule import SuperTestModule
from ..modules.example import ExampleModule
from migen import *

class MockTestAttributes():
    def __init__(self, tag, io_decl, ticks_after_inputs, ticks_after_outputs):
        self.tag = tag
        self.io_decl = io_decl
        self.ticks_after_inputs = ticks_after_inputs
        self.ticks_after_outputs = ticks_after_outputs

def make_test_module(testattr, dut_class, args=None, specials=None):
    return SuperTestModule(testattr, dut_class, args, specials)

def sim_test_module(mod, ticks_after_input, is_meant_to_succeed):
    yield mod.i_go.eq(1)

    for i in range(ticks_after_input):
        yield

    is_over = yield mod.o_over
    is_success = yield mod.o_success

    assert(is_over and is_success == is_meant_to_succeed)

def test_example_positive_1():
    def make_example_testattr():
        tag = "example-positive-1"
        io_decl = [
            ({"i_first": 1, "i_second": 1}, {"o_first": 1, "o_second": 1}),
            ({"i_first": 2, "i_second": 2}, {"o_first": 2, "o_second": 2})
        ]
        ticks_after_inputs = 1
        ticks_after_outputs = 0

        return MockTestAttributes(tag, io_decl, ticks_after_inputs, ticks_after_outputs)

    ticks_after_input = 1
    is_meant_to_succeed = True

    testattr = make_example_testattr()
    tag = testattr.tag + ".vcd"

    dut_class = ExampleModule
    dut = make_test_module(testattr, dut_class, [8])

    run_simulation(
        dut, sim_test_module(dut, ticks_after_input, is_meant_to_succeed), vcd_name=tag)

def test_example_negative_1():
    def make_example_testattr():
        tag = "example-negative-1"
        io_decl = [
            ({"i_first": 2, "i_second": 2}, {"o_first": 1, "o_second": 1}),
            ({"i_first": 1, "i_second": 1}, {"o_first": 2, "o_second": 2})
        ]
        ticks_after_inputs = 1
        ticks_after_outputs = 0

        return MockTestAttributes(tag, io_decl, ticks_after_inputs, ticks_after_outputs)

    ticks_after_input = 1
    is_meant_to_succeed = False

    testattr = make_example_testattr()
    tag = testattr.tag + ".vcd"

    dut_class = ExampleModule
    dut = make_test_module(testattr, dut_class, [8])

    run_simulation(
        dut, sim_test_module(dut, ticks_after_input, is_meant_to_succeed), vcd_name=tag)
