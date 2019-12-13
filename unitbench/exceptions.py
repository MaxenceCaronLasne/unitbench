class UnitBenchAssertionError(AssertionError):
    def __init__(self, out, exp, message, round_idx):
        self.out = out
        self.exp = exp
        self.message = message
        self.round_idx = round_idx
