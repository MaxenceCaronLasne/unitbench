from migen import Module, Signal, If, Cat, Case


class Counter(Module):
    def __init__(self, n):
        # Output
        self.o = Signal(max=n, reset=0)

        ###

        self.sync += [
            If(self.o == n - 1,
                self.o.eq(0))
            .Else(
                self.o.eq(self.o + 1)
            )
        ]


class SuperUnit(Module):
    """Migen super-module for a single test.

    Args:
        testattr (TestAttributes): attributes for the test.
        dut_class (class Module): class of the DUT.
        args (list): list of arguments for DUT instanciation.
        specials (list): list of Migen "specials".
    """

    def _make_inputs_applications(self, i_decl):
        """Make Migen statements applying inputs declarations to dut signals.

        Args:
            i_decl (dict): A dictionary associating signal names with integers.

        Returns:
            list: A list of Migen statements describing input applications.
        """
        res = []

        for signame, value in i_decl.items():
            res += [getattr(self._dut, signame).eq(value)]

        return res

    def _make_outputs_checker(self, o_decl):
        """Make Migen statements for checking dut output signals.

        Args:
            o_decl (dict): A dictionary associating signal name to an
                           integer value.

        Returns:
            list: A list of Migen statements describing output checking.
        """
        res = []

        for signame, value in o_decl.items():
            res += [self._test_outs[signame]
                    .eq(getattr(self._dut, signame) != value)]

        return res

    def _make_outputs_signals(self, io_decl):
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

    def __init__(self, testcase, dut_class, args=None, specials=None):
        self.i_go = Signal()  # Unused for now.

        # Outputs

        #: Signal: up if the test process is over.
        self.o_over = Signal()

        #: Signal: up if the test result is successful. Relevant only when
        #          `o_over` is up.
        self.o_success = Signal(reset=1)

        # Locals

        #: dict: association between DUT's output signals names and signals.
        self._test_outs = self._make_outputs_signals(testcase.io_decl)

        #: Signal(n): concatenation of all signals contained in
        #             `self.test_outs`.
        self._cat_test_outs = Cat(
            [signal for _, signal in self._test_outs.items()])

        # Sub-modules

        #: Module: device under test's module instance.
        self._dut = dut_class() if args is None else dut_class(*args)

        self.submodules += self._dut

        # Specials
        if specials is not None:
            self.specials += specials

        ###

        cases = {}
        tick_count = 0

        in_q, exp_q = testcase.get_io_queues()

        while not in_q.empty() or not exp_q.empty():
            cases[tick_count] = []

            in_values = None if in_q.empty() else in_q.get()
            if in_values is not None:
                cases[tick_count] += self._make_inputs_applications(in_values)

            exp_values = None if exp_q.empty() else exp_q.get()
            if exp_values is not None:
                cases[tick_count] += self._make_outputs_checker(exp_values)

            tick_count += 1

        # Counter initialization using `tick_count`
        counter = Counter(tick_count + 1)
        self.submodules += counter

        self.sync += Case(counter.o, cases)

        # `self.o_over` control
        self.comb += [self.o_over.eq(counter.o == tick_count)]

        # `self.o_success` control
        self.comb += [
            If(self.o_success == 1,
               self.o_success.eq(self._cat_test_outs == 0))
            .Else(
                self.o_success.eq(0))
        ]


class SuperUnitSupervisor(Module):
    def __init__(self, unitmodules):
        self.o_successes = Signal(len(unitmodules))
