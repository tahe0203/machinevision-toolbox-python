import numpy as np

import numpy.testing as nt
import unittest
from pathlib import Path

import color as color

# for debugging purposes
import matplotlib.pyplot as plt
import cv2 as cv

class TestColor(unittest.TestCase):

    def test_blackbody(self):
        e = color.blackbody(500e-9, 4000)
        self.assertAlmostEqual(e, 2.86512308e+12, delta=1e4)

        e = color.blackbody([400e-9, 500e-9], 4000)
        self.assertEqual(len(e), 2)
        self.assertAlmostEqual(e[0], 1.44662486e+12, delta=1e4)
        self.assertAlmostEqual(e[1], 2.86512308e+12, delta=1e4)

    def test_loadspectrum(self):
        data_dir = Path.cwd() / 'data'

        # test with filename = "data/solar.dat"
        nm = 1e-9
        lam = np.linspace(400, 700, 30) * nm
        brick = color.loadspectrum(lam, (data_dir / 'redbrick.dat').as_posix())
        # might need .as_uri() instead of .as_posix() for Windows OS
        self.assertEqual(brick.s.shape, (30, 1))
        nt.assert_array_almost_equal(lam, brick.lam)

        cone = color.loadspectrum(lam, (data_dir / 'cones').as_posix())
        self.assertEqual(cone.s.shape, (30, 3))

        # tests outside of interpolation range
        lam2 = np.linspace(300, 1000, 50) * nm
        solar = color.loadspectrum(lam2, (data_dir / 'solar').as_posix())
        self.assertEqual(solar.s.shape, (50, 1))

        # lam_water = np.linspace(400, 700, 30) * nm
        # water = color.loadspectrum(lam_water,
        #                     (data_dir / 'water').as_posix())

    def test_chromaticity(self):
        # these tests just check if the code runs
        rg = color.lambda2rg(555e-9)
        rg = color.lambda2rg(lam=np.array([555e-9, 666e-9]),
                             e=np.array([4, 1, 2]))
        xy = color.lambda2xy(555e-9)
        xy = color.lambda2rg(lam=np.array([555e-9, 666e-9]),
                             e=np.array([4, 1, 2]))

        im = np.zeros((2, 2, 3))
        # 0 - red channel, 1 - green channel, 2 - blue channel
        im[0, 0, 0] = 1  # top left = red
        im[0, 1, 1] = 1  # top right = green
        im[1, 0, 1] = 1  # bottom left = green
        im[1, 1, 2] = 1  # bottom right = blue

        cc = color.tristim2cc(im)
        cc_ans = np.array([[[1, 0], [0, 1]], [[0, 1], [0, 0]]])
        nt.assert_array_almost_equal(cc, cc_ans)

        print(cc)


# ---------------------------------------------------------------------------------------#
if __name__ == '__main__':

    unittest.main()