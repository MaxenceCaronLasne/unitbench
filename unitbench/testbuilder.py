from migen.fhdl import verilog
from migen.sim import run_simulation
from unitbench.testmodule import SuperUnit
from unitbench.testdeclaration import TestsDeclaration


class UnitBenchBuilder():
    def __init__(self, filename, dut_class, args=[], specials=[],
                 gen_vcd=False):
        self._dut_class = dut_class
        self._args = args
        self._specials = specials
        self._testdecl = TestsDeclaration(filename)
        self._superunits = self._make_superunits(dut_class, args, specials)
        self._gen_vcd = gen_vcd

    def _make_superunits(self, dut_class, args, specials):
        res = []

        for testcase in self._testdecl.testcases:
            su = SuperUnit(testcase, dut_class, args, specials)
            res.append(su)

        return res

    def _generate_verilog(self, testcase_index):
        su = self._superunits[testcase_index]
        return verilog.convert(su, {su.o_over, su.o_success})

    def _gen_verilog_in_stream(self, stream, testcase_index):
        v = self._generate_verilog(testcase_index)
        stream.write(v.__str__())

    def write_verilog(self, filename, testcase_index):
        v = self._generate_verilog(testcase_index)
        v.write(filename)

    def _get_vcd_name(self, testname, tag, outdir):
        if not self._gen_vcd:
            return None

        # TODO: standardize path generation
        return outdir + "/" + testname + "_" + tag + ".vcd"

    def _sim_and_asrt_testcase(self, testcase, testname, outdir):
        def _make_dut(self):
            if self._args is not None:
                return self._dut_class(*self._args)

            return self._dut_class()

        def _set_input(dut, signame, in_value):
            return getattr(dut, signame).eq(in_value)

        def _get_output(dut, signame):
            return (yield getattr(dut, signame))

        def _unitbench_assert(signame, out_value, expected_value, testname,
                              round_idx):
            message = ("unitbench: `{}`, round {}, "
                       + "test failed: `{}`: {}; expected {}").format(
                testname, round_idx, signame, out_value, expected_value)

            assert out_value == expected_value, message

        def sim(dut, testcase):
            round_idx = 0
            for in_values, expected_values in testcase.io_decl:
                # Set input signals to given values
                for signame, in_value in in_values.items():
                    yield _set_input(dut, signame, in_value)

                # Pass given ticks after inputs setting
                for _ in range(testcase.ticks_after_inputs):
                    yield

                # Get output signals result and check errors in respect with
                # espected values
                for signame, expected_value in expected_values.items():
                    out_value = yield from _get_output(dut, signame)
                    _unitbench_assert(signame, out_value, expected_value,
                                      testname, round_idx)

                # Pass given ticks after output checking
                for _ in range(testcase.ticks_after_outputs * 0):
                    yield

                round_idx += 1

        dut = self._dut_class(*self._args)

        run_simulation(dut, sim(dut, testcase),
                       vcd_name=self._get_vcd_name(testname, testcase.tag,
                                                   outdir))

    def simulate_and_assert(self, outdir="."):
        for testcase in self._testdecl.testcases:
            self._sim_and_asrt_testcase(testcase, self._testdecl.name, outdir)
