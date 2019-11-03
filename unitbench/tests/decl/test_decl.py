import pytest
from ...testdeclaration import TestAttributes, TestsDeclaration


@pytest.fixture
def td():
    filename = "unitbench/tests/json/example.json"
    td = TestsDeclaration(filename)

    return td


def test_tests_declaration_name(td):
    assert(td.name == "example")


def test_test_attributes_tag(td):
    testattr = td.testattrs[0]
    assert(testattr.tag == "first-test")

    testattr = td.testattrs[1]
    assert(testattr.tag == "second-test")


def test_test_attributes_ticks(td):
    testattr = td.testattrs[0]
    assert(testattr.ticks_after_inputs == 1)
    assert(testattr.ticks_after_outputs == 1)

    testattr = td.testattrs[1]
    assert(testattr.ticks_after_inputs == 1)
    assert(testattr.ticks_after_outputs == 1)


def test_test_attributes_io_decl(td):
    testattr = td.testattrs[0]
    assert(testattr.io_decl[0] == ({"i_first": 1, "i_second": 1},
                                   {"o_first": 1, "o_second": 1}))
    assert(testattr.io_decl[1] == ({"i_first": 2, "i_second": 2},
                                   {"o_first": 2, "o_second": 2}))

    testattr = td.testattrs[1]
    assert(testattr.io_decl[0] == ({"i_first": 3, "i_second": 3},
                                   {"o_first": 3, "o_second": 3}))
    assert(testattr.io_decl[1] == ({"i_first": 4, "i_second": 4},
                                   {"o_first": 4, "o_second": 4}))
