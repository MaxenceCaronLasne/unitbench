import json
import collections


class TestAttributes():
    """Attributes of a single test.

    Args:
        test_data (dict): data for a single test, parsed from JSON
                          test declaration.
    """

    def __init__(self, test_data):
        self.tag = test_data["tag"]

        #: list of couples of decl: List of IO declarations.
        self.io_decl = self.make_io_decl(test_data)

        #: int: ticks to pass after input application.
        self.ticks_after_inputs = test_data["ticks_after_inputs"]

        #: int: ticks to pass after output checking.
        self.ticks_after_outputs = test_data["ticks_after_outputs"]

    def make_io_decl(self, test_data):
        """Make io_decl dictionaries from data.

        Args:
            test_data (dict): data for a single test parsed from a JSON tests
                              declaration file.

        Returns:
            list: a list of test declarations.
        """

        def compute_decl(decl):
            res = {}

            for signame, value in decl.items():
                if isinstance(value, str):
                    value = int(value, 2)
                res[signame] = value

            return res

        res = []

        for r in test_data["rounds"]:
            res += [(compute_decl(r["inputs"]), compute_decl(r["outputs"]))]

        return res


class TestsDeclaration():
    """Contains test declarations data.

    Args:
        filename (str): name of the test declaration JSON file.
    """

    def __init__(self, filename):
        #: dict: data parsed from JSON tests declaration.
        self.data = self.make_data(filename)

        #: str: name of the testsuite.
        self.name = self.data["name"]

        #: list of TestAttributes(): list of each test's attributes.
        self.testattrs = self.make_testattrs()

    def make_data(self, filename):
        """Parses a JSON tests declaration from filename.

        Args:
            filename (str): name of the JSON file to parse.

        Returns:
            dict: data parsed from JSON file.
        """

        res = None

        with open(filename, 'r') as f:
            res = json.loads(
                f.read(), object_pairs_hook=collections.OrderedDict)

        return res

    def make_testattrs(self):
        """Make a list of TestAttributes() from tests declaration.

        Returns:
            list: a list of TestAttributes().
        """
        res = []

        for t in self.data["tests"]:
            res += [TestAttributes(t)]

        return res
