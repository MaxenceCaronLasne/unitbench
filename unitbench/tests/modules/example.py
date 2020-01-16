from migen import Module, Signal


class ExampleModule(Module):
    def __init__(self, width):
        self.i_first = Signal(width)
        self.i_second = Signal(width)

        self.o_first = Signal(width)
        self.o_second = Signal(width)

        ###

        self.sync += [
            self.o_first.eq(self.i_first),
            self.o_second.eq(self.i_second)
        ]


class BadExampleModule(Module):
    def __init__(self, width):
        self.i_first = Signal(width)
        self.i_second = Signal(width)

        self.o_first = Signal(width)
        self.o_second = Signal(width)

        ###

        self.sync += [
            self.o_first.eq(~self.i_first),
            self.o_second.eq(~self.i_second)
        ]
