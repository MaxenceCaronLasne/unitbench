import json
from jsonschema import validate
import collections


class TestCase():
    """Attributes of a single test.

    Args:
        test_data (dict): data for a single test, parsed from JSON
                          test declaration.
    """
    __test__ = False  #: Ignored by Pytest

    def __init__(self, test_data):
        self.tag = test_data["tag"]

        #: list of couples of decl: List of IO declarations.
        self.io_decl = self._make_io_decl(test_data)

        #: int: ticks to pass after input application.
        self.ticks_after_inputs = test_data["ticks_after_inputs"]

        #: int: ticks to pass after output checking.
        self.ticks_after_outputs = test_data["ticks_after_outputs"]

    def _make_io_decl(self, test_data):
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

    __test__ = False #: Ignored by Pytest

    def __init__(self, filename):
        #: dict: data parsed from JSON tests declaration.
        self._data = self._parse_testfile(filename)

        #: str: name of the testsuite.
        self.name = self._data["name"]

        #: list of TestAttributes(): list of each test's attributes.
        self.testcases = self._make_testcases()


    def _parse_testfile(self, filename):
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

        self._validate_testfile(res)

        return res

    def _validate_testfile(self, data):
        """Validate raw data against JSON Scheme.

        Args:
            data (dict): data parsed from JSON file.
        """
        schema = None

        with open("unitbench/testdecl_scheme.json", "r") as f:
            schema = json.loads(f.read())

        validate(data, schema)

    def _make_testcases(self):
        """Make a list of TestAttributes() from tests declaration.

        Returns:
            list: a list of TestAttributes().
        """
        res = []

        for t in self._data["tests"]:
            res += [TestCase(t)]

        return res
