from migen import *

class Counter(Module):
    def __init__(self, n):
        # Output
        self.o = Signal(max=n, reset=0)

        ###

        self.sync += [
            If(self.o == n - 1,
                self.o.eq(0)
            ).Else(
                self.o.eq(self.o + 1)
            )
        ]

class SuperTestModule(Module):
    """Migen super-module for a single test.

    Args:
        testattr (TestAttributes): attributes for the test.
        dut_class (class Module): class of the DUT.
        args (list): list of arguments for DUT instanciation.
        specials (list): list of Migen "specials".
    """

    def make_inputs_applications(self, i_decl):
        """Make Migen statements applying inputs declarations to dut signals.

        Args:
            i_decl (dict): A dictionary associating signal names with integers.

        Returns:
            list: A list of Migen statements describing input applications.
        """
        res = []

        for signame, value in i_decl.items():
            res += [ getattr(self.dut, signame).eq(value) ]

        return res


    def make_outputs_checker(self, o_decl):
        """Make Migen statements for checking dut output signals.

        Args:
            o_decl (dict): A dictionary associating signal name to an
                           integer value.

        Returns:
            list: A list of Migen statements describing output checking.
        """
        res = []

        for signame, value in o_decl.items():
            res += [ self.test_outs[signame].eq(getattr(self.dut, signame) != value) ]

        return res

    def make_outputs_signals(self, io_decl):
        """Make a dictionary that contains signals corresponding to o_decl.

        Args:
            io_decl (list of dict): list of (i_decl, o_decl) couples.

        Returns:
            dict: dictionary associating output signal names with test signal.
        """
        res = {}

        for _, o_decl in io_decl:
            for signame in o_decl:
                res[signame] = Signal(name="test_out_" + signame)

        return res

    def __init__(self, testattr, dut_class, args=None, specials=None):
        self.i_go = Signal() # Unused for now.

        # Outputs

        #: Signal: up if the test process is over.
        self.o_over = Signal()

        #: Signal: up if the test result is successful. Relevant only when
        #          `o_over` is up.
        self.o_success = Signal(reset=1)

        # Locals

        #: dict: association between DUT's output signals names and signals.
        self.test_outs = self.make_outputs_signals(testattr.io_decl)

        #: Signal(n): concatenation of all signals contained in
        #             `self.test_outs`.
        self.cat_test_outs = Cat([signal for _, signal in self.test_outs.items()])

        # Sub-modules

        #: Module: device under test's module instance.
        self.dut = dut_class() if args is None else dut_class(*args)

        self.submodules += self.dut

        # Specials
        if specials is not None:
            self.specials += specials

        ###

        cases = {}
        tick_count = 0

        for i_decl, o_decl in testattr.io_decl:
            cases[tick_count] = []
            cases[tick_count] += self.make_inputs_applications(i_decl)
            tick_count += testattr.ticks_after_inputs

            cases[tick_count + 1] = []
            cases[tick_count + 1] += self.make_outputs_checker(o_decl)
            tick_count += testattr.ticks_after_outputs

        # Counter initialization using `tick_count`
        counter = Counter(tick_count + 3)
        self.submodules += counter

        self.sync += Case(counter.o, cases)

        # `self.o_over` control
        self.comb += [ self.o_over.eq(counter.o == tick_count + 2) ]

        # `self.o_success` control
        self.comb += [
            If(self.o_success == 1,
               self.o_success.eq(self.cat_test_outs == 0)
            ).Else(
                self.o_success.eq(0)
            )
        ]


class SupervisorModule(Module):
    def __init__(self, unitmodules):
        self.o_successes = Signal(len(unitmodules))
