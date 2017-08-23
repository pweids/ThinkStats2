"""This file contains code for use with "Think Stats",
by Allen B. Downey, available from greenteapress.com

Copyright 2014 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html

write a function that reads
the respondent file, 2002FemResp.dat.gz.
The variable pregnum is a recode that indicates how many times each respondent
has been pregnant. Print the value counts for this variable and
compare them to the published results in the NSFG codebook.
You can also cross-validate the respondent and pregnancy files by comparing
pregnum for each respondent with the number of records in the pregnancy
file.
You can use nsfg.MakePregMap to make a dictionary that maps from each
caseid to a list of indices into the pregnancy DataFrame.


"""

from __future__ import print_function

import numpy as np
import sys

import nsfg
import thinkstats2

def readFemResp(dct_file="2002FemResp.dct",
                dat_file="2002FemResp.dat.gz",
                nrows = None):
    dct = thinkstats2.ReadStataDct(dct_file)
    df = dct.ReadFixedWidth(dat_file, compression="gzip", nrows=nrows)
    nsfg.CleanFemResp(df)
    return df


def readFemPreg(dct_file="2002FemPreg.dct",
                dat_file="2002FemPreg.dat.gz",
                nrows = None):
    dct = thinkstats2.ReadStataDct(dct_file)
    df = dct.ReadFixedWidth(dat_file, compression="gzip", nrows=nrows)
    return df

def cross_validate(femResp, femPreg):

    # make the map from caseid to list of pregnancy indices
    preg_map = nsfg.MakePregMap(femPreg)

    # iterate through the respondent pregnum series
    for index, pregnum in femResp.pregnum.iteritems():
        caseid = femResp.caseid[index]
        indices = preg_map[caseid]

        # check that pregnum from the respondent file equals
        # the number of records in the pregnancy file
        if len(indices) != pregnum:
            print(caseid, len(indices), pregnum)
            return False

    return True

def CleanFemResp(df):
    pass


def main(script):
    """Tests the functions in this module.

    script: string script name
    """
    print("Reading fem resp...")
    fr = readFemResp()
    print("Reading fem preg...")
    fp = readFemPreg()
    assert(cross_validate(fr, fp))
    print('%s: All tests passed.' % script)


if __name__ == '__main__':
    main(*sys.argv)
