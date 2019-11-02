class TestAttributes():
    """Attributes of a single test.

    Args:
        test_data (dict): data for a single test, parsed from JSON
                          test declaration.
    """

    def __init__(self, test_data):
        self.tag = None

        #: list of couples of decl: List of IO declarations.
        self.io_decl = None

        #: int: ticks to pass after input application.
        self.ticks_after_inputs = None

        #: int: ticks to pass after output checking.
        self.ticks_after_outputs = None


class TestsDeclaration():
    """Contains test declarations data.

    Args:
        filename (str): name of the test declaration JSON file.
    """
    def __init__(self, filename):
        #: str: name of the testsuite
        self.name = ""
        #: list of TestAttributes(): list of each test's attributes.
        self.testattrs = []
