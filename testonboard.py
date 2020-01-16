#!/usr/bin/env python3
from unitbench.tests.modules.example import ExampleModule, BadExampleModule
from unitbench import UnitBenchBuilder
from migen import Module, If, Cat
from migen.build.platforms import icestick


class BlinkerTopLevel(Module):
    def __init__(self, plat, superunit):
        self.garbage = Cat([plat.request("user_led") for _ in range(3)])
        self.bad_led = plat.request("user_led")
        self.good_led = plat.request("user_led")

        self.submodules += superunit

        self.comb += [
            [g.eq(0) for g in self.garbage]
        ]

        self.sync += [
            If(self.good_led == 0,
               self.good_led.eq(superunit.o_success & superunit.o_over))
            .Else(
                self.good_led.eq(1)),

            If(self.bad_led == 0,
               self.bad_led.eq(~superunit.o_success & superunit.o_over))
            .Else(
                self.bad_led.eq(0))
        ]


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        raise Exception("Missing argument : [platform] [good/bad]")

    plat = None

    if sys.argv[1] == "icestick":
        plat = icestick.Platform()
    else:
        raise Exception("This argument does not exist.")

    ex = None

    if sys.argv[2] == "bad":
        ex = BadExampleModule
    elif sys.argv[2] == "good":
        ex = ExampleModule
    else:
        raise Exception("This argument does not exist.")

    u = UnitBenchBuilder("unitbench/tests/json/example.json", ex, [4])

    su = u._superunits[1]
    dut = BlinkerTopLevel(plat, su)
    plat.build(dut)
