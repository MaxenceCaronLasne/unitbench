from migen import *

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
        pass


    def make_outputs_checker(self, o_decl):
        """Make Migen statements for checking dut output signals.

        Args:
            o_decl (dict): A dictionary associating signal name to an
                           integer value.

        Returns:
            list: A list of Migen statements describing output checking.
        """
        pass

    def __init__(self, testattr, dut_class, args=None, specials=None):
        self.i_go = Signal()
        self.o_over = Signal()
        self.o_success = Signal()

        if args is not None:
            self.dut = dut_class(*args)
        else:
            self.dut = dut_class()

        # Sub-modules
        self.submodules += self.dut

        if specials is not None:
            self.specials += specials

#    Pseudo code for __init__:
#
#        generate_io_assignations(testattr.signals_decl)
#
#        cases = {}
#        tick_count = 0
#
#        # Add some signals for output checking
#        for i_decl, o_decl in testattr.io_decl:
#            cases[tick_count] = self.make_inputs_applications(i_decl)
#            tick_count += testattr.ticks_after_inputs
#
#            cases[tick_count] = self.make_output_checker(o_decl)
#            tick_count += testattr.ticks_after_outputs
#
#        self.sync += Case(counter.o, cases)

class SupervisorModule(Module):
    def __init__(self, unitmodules):
        self.o_successes = Signal(len(unitmodules))
