import os
import sh
import difflib
from nose.tools import eq_

base_dir = '/'.join(__file__.split('/')[:-1])
input_dir = base_dir + '/inputs'
expected_dir = base_dir + '/outputs'


def test_battery():
    input_filenames = gather_filenames(input_dir)
    expected_filenames = gather_filenames(expected_dir)
    pairs = zip(input_filenames, expected_filenames)

    for input_filename, expected_filename in pairs:
        yield _test_tidy, input_filename, expected_filename


def gather_filenames(dirname):
    filenames = sorted(os.listdir(dirname))
    return [
        f for f in filenames if (
            not f.endswith('.swp')
            and not f.endswith('.pyc')
        )]


def _test_tidy(input_filename, expected_filename):
    """ Does tidy produce the expected output? """

    with open(expected_dir + "/" + expected_filename) as f:
        expected = f.read()

    output = sh.python("PythonTidy.py", "tests/inputs/%s" % input_filename)
    difference = ''.join(difflib.unified_diff(
        [line + '\n' for line in expected.split('\n')],
        [line + '\n' for line in output.split('\n')],
        fromfile="expected.py",
        tofile="output.py",
    ))

    assert not difference, '\n' + difference
