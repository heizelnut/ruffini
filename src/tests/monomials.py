from unittest import TestCase

from ruffini import Monomial as M
from ruffini import VariablesDict as VD


class Test (TestCase):
    def setUp(self):
        self.m0 = M(2, {'x': 1, 'y': 1})
        self.m1 = M(-6, {'x': 1, 'y': 3})
        self.m2 = M(8, {'x': 1, 'y': 1})
        self.m3 = M(3, {})
        self.m4 = M(1.16, {'a': 4})
        self.m5 = M(-9, {'y': 3})

    def test_initializing(self):
        # Coefficient must be int or float
        self.assertRaises(TypeError, M, "3", {})

        # Variables must be a dict
        self.assertRaises(TypeError, M, 8, [])

        # Variables are stored in a new VariabesDict
        self.assertIsInstance(M(3, {}).variables, VD)
        variables = {}
        self.assertIsNot(M(2, variables).variables, variables)

        # If variables is a variablesdict, it won't
        # be regenerated
        variables = VD()
        self.assertIs(M(2, variables).variables, variables)

        # check the degree
        self.assertEqual(M(2, {'x': 2, 'y': 7}).degree, 9)

    def test_similarity(self):
        # two monomials are simimlar if they have the
        # same variables
        self.assertTrue(self.m0.similar_to(self.m2))
        self.assertFalse(self.m0.similar_to(self.m1))

        # if the second operator is not a monomial
        # they are never similar
        self.assertFalse(self.m2.similar_to(""))

        # if the first operator has no variables, it
        # can be compared to floats or integers
        self.assertTrue(self.m3.similar_to(6.28))

    def test_gcd_lcm(self):
        # only works with numbers and monomials
        self.assertRaises(TypeError, self.m0.gcd, "")
        self.assertRaises(TypeError, self.m0.lcm, [])

        # can work with numbers
        self.assertEqual(self.m1.gcd(3), self.m1.gcd(M(3, {})))

        # only integer coefficient
        self.assertRaises(ValueError, self.m3.gcd, self.m4)
        self.assertRaises(ValueError, self.m4.gcd, self.m3)

        # always positive result
        self.assertGreater(self.m0.gcd(self.m5).coefficient, 0)
        self.assertGreater(self.m2.lcm(self.m3).coefficient, 0)

        # return 0 if one term is 0
        self.assertRaises(ValueError, self.m5.gcd, 0)
        self.assertRaises(ValueError, M(0, {}).gcd, self.m3)

        # values
        self.assertEqual(self.m1.gcd(self.m2), M(2, {'x': 1, 'y': 1}))
        self.assertEqual(self.m0.lcm(self.m5), M(18, {'x': 1, 'y': 3}))

        # commutative property
        self.assertEqual(self.m0.gcd(self.m2), self.m2.gcd(self.m0))
        self.assertEqual(self.m0.lcm(self.m2), self.m2.lcm(self.m0))