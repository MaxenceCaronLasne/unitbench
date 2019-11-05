from migen.fhdl import verilog
from unitbench.testmodule import SuperUnit
from unitbench.testdeclaration import TestsDeclaration


class UnitBenchBuilder():
    def __init__(self, filename, dut_class, args=None, specials=None):
        self._testdecl = TestsDeclaration(filename)
        self._superunits = self._make_superunits(dut_class, args, specials)

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
        with open(filename, "w") as f:
            v.write(f)

