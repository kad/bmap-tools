""" This test verifies Fiemap module functionality. It generates random sparse
files and make sure FIEMAP returns correct information about the holes. """

import unittest
import itertools

import tests.helpers
from bmaptools import Fiemap

class Error(Exception):
    """ A class for exceptions generated by this test. """
    pass

def _do_test(f_image, mapped, holes):
    """ Verifiy that Fiemap reports the correct mapped areas and holes ranges
    fro the 'f_image' file object. The 'mapped' and 'holes' lists contains the
    correct ranges. """

    # Make sure that Fiemap's get_mapped_ranges() returns the same ranges as
    # we have in the 'mapped' list.
    fiemap = Fiemap.Fiemap(f_image)
    fiemap_iterator = fiemap.get_mapped_ranges(0, fiemap.blocks_cnt)
    iterator = itertools.izip_longest(fiemap_iterator, mapped)

    for range1, range2 in iterator:
        if range1[0] > range1[1]:
            raise Error("bad mapped area range %d-%d" % (range1[0], range1[1]))

        if range1 != range2:
            raise Error("mapped areas mismatch: %d-%d as per Fiemap module, " \
                        "%d-%d in the image file '%s'" \
                        % (range1[0], range1[1], range2[0], range2[1],
                           f_image.name))

    # Make sure that Fiemap's get_unmapped_ranges() returns the same ranges as
    # we have in the 'holes' list.
    fiemap_iterator = fiemap.get_unmapped_ranges(0, fiemap.blocks_cnt)
    iterator = itertools.izip_longest(fiemap_iterator, holes)

    for range1, range2 in iterator:
        if range1[0] > range1[1]:
            raise Error("bad hole range %d-%d" % (range1[0], range1[1]))

        if range1 != range2:
            raise Error("holes mismatch: %d-%d as per Fiemap module, %d-%d " \
                        "in the image file '%s'" \
                        % (range1[0], range1[1], range2[0], range2[1],
                           f_image.name))

class TestCreateCopy(unittest.TestCase):
    """ The test class for this unit tests. Basically executes the '_do_test()'
    function for different sparse files. """

    @staticmethod
    def test():
        """ The test entry point. Executes the '_do_test()' function for files
        of different sizes, holes distribution and format. """

        # Delete all the test-related temporary files automatically
        delete = True
        # Create all the test-related temporary files in the default directory
        # (usually /tmp).
        directory = None

        iterator = tests.helpers.generate_test_files(delete = delete,
                                                     directory = directory)
        for f_image, mapped, holes in iterator:
            _do_test(f_image, mapped, holes)
