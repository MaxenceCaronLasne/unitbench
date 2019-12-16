from migen import Module, Signal


class test_module_2(Module):
    def __init__(self, size):
        self.a = Signal(size * 2)
        self.b = Signal(max=size)
        self.c = Signal()

        self.d = Signal(max=size)
        self.e = Signal()
        self.f = Signal()

        self.comb += [
            self.d.eq(self.b + 1),
            self.e.eq(1),
            self.f.eq(1)
        ]
