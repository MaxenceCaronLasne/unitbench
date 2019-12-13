import queue
from ...testmodule import SuperUnit
from ..modules.example import ExampleModule
from migen import *


class MockTestAttributes():
    def __init__(self, tag, io_decl, ticks_before_next_input,
                 ticks_before_checking):
        self.tag = tag
        self.io_decl = io_decl
        self.ticks_before_next_input = ticks_before_next_input
        self.ticks_before_checking = ticks_before_checking

    def get_io_queues(self):
        """Generate input and expected io_decl queues.

        Args:
            testcase (TestDeclaration()): current test case.

        Returns:
            (queue.Queue(), queue.Queue()): input and expected declarations
                                            queues.
        """

        def _push_expected_values(q, is_first, expected_values):
            if is_first:
                for _ in range(self.ticks_before_checking):
                    q.put(None)
            else:
                for _ in range(self.ticks_before_next_input - 1):
                    q.put(None)

            q.put(expected_values)

            return q

        def _push_input_values(q, in_values):
            q.put(in_values)
            for _ in range(self.ticks_before_next_input - 1):
                q.put(None)

        in_q = queue.Queue()
        exp_q = queue.Queue()

        is_first = True
        for in_values, expected_values in self.io_decl:
            _push_input_values(in_q, in_values)
            _push_expected_values(exp_q, is_first, expected_values)
            is_first = False

        return in_q, exp_q


class EnvExample():
    def __init__(self):
        self.tag = ""
        self.io_decl = []
        self.ticks_before_next_input = 0
        self.ticks_before_checking = 0
        self.is_meant_to_succeed = True
        self.dut_class = ExampleModule

    def runsim(self):
        testattr = MockTestAttributes(
            self.tag, self.io_decl,
            self.ticks_before_next_input,
            self.ticks_before_checking)

        dut = make_test_module(testattr, self.dut_class, [8])

        run_simulation(
            dut, sim_test_module(dut, testattr, self.is_meant_to_succeed),
            vcd_name=testattr.tag + ".vcd")


def make_test_module(testattr, dut_class, args=None, specials=None):
    return SuperUnit(testattr, dut_class, args, specials)


def sim_test_module(mod, testattr, is_meant_to_succeed):
    yield mod.i_go.eq(1)

    for i in range(testattr.ticks_before_next_input * len(testattr.io_decl) +
                   testattr.ticks_before_checking):
        yield

    is_over = yield mod.o_over
    is_success = yield mod.o_success

    assert(is_over == 1)
    assert((is_success == 1) == is_meant_to_succeed)


def test_example_positive_1():
    env = EnvExample()

    env.tag = "example-positive-1"

    env.io_decl = [
        ({"i_first": 1, "i_second": 1}, {"o_first": 1, "o_second": 1})
    ]

    env.ticks_before_next_input = 1
    env.ticks_before_checking = 2

    env.is_meant_to_succeed = True

    env.runsim()


def test_example_negative_1():
    env = EnvExample()

    env.tag = "example-negative-1"

    env.io_decl = [
        ({"i_first": 2, "i_second": 2}, {"o_first": 1, "o_second": 1}),
    ]

    env.ticks_before_next_input = 1
    env.ticks_before_checking = 2

    env.is_meant_to_succeed = False

    env.runsim()


def test_example_multi_positive_1():
    env = EnvExample()

    env.tag = "example-multi-positive-1"

    env.io_decl = [
        ({"i_first": 1, "i_second": 1}, {"o_first": 1, "o_second": 1}),
        ({"i_first": 2, "i_second": 2}, {"o_first": 2, "o_second": 2})
    ]

    env.ticks_before_next_input = 1
    env.ticks_before_checking = 2

    env.is_meant_to_succeed = True

    env.runsim()


def test_example_multi_negative_1():
    env = EnvExample()

    env.tag = "example-multi-negative-1"

    env.io_decl = [
        ({"i_first": 2, "i_second": 2}, {"o_first": 1, "o_second": 1}),
        ({"i_first": 1, "i_second": 1}, {"o_first": 2, "o_second": 2})
    ]

    env.ticks_before_next_input = 1
    env.ticks_before_checking = 2

    env.is_meant_to_succeed = False

    env.runsim()


def test_example_multi_diff_1():
    env = EnvExample()

    env.tag = "example-multi-diff-1"

    env.io_decl = [
        ({"i_first": 1, "i_second": 1}, {"o_first": 2, "o_second": 2}),
        ({"i_first": 3, "i_second": 3}, {"o_first": 3, "o_second": 3})
    ]

    env.ticks_before_next_input = 1
    env.ticks_before_checking = 2

    env.is_meant_to_succeed = False

    env.runsim()


def test_example_multi_diff_2():
    env = EnvExample()
    env.tag = "example-multi-diff-2"
    env.io_decl = [
        ({"i_first": 1, "i_second": 1}, {"o_first": 1, "o_second": 1}),
        ({"i_first": 2, "i_second": 2}, {"o_first": 3, "o_second": 3})
    ]
    env.ticks_before_next_input = 1
    env.ticks_before_checking = 2

    env.is_meant_to_succeed = False

    env.runsim()
