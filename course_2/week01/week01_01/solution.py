# import unittest
#
# from factorization import factorize


class TestFactorize(unittest.TestCase):

    def test_wrong_types_raise_exception(self):
        for x in ['string', 1.5]:
            with self.subTest(case=x):
                self.assertRaises(TypeError, factorize, x)

    def test_negative(self):
        for x in [-1, -10, -100]:
            with self.subTest(case=x):
                self.assertRaises(ValueError, factorize, x)

    def test_zero_and_one_cases(self):
        for x, true_ in zip([0, 1], [(0, ), (1, )]):
            with self.subTest(case=x):
                result = factorize(x)
                self.assertEqual(result, true_)

    def test_simple_numbers(self):
        for x, true_ in zip([3, 13, 29], [(3, ), (13, ), (29, )]):
            with self.subTest(case=x):
                result = factorize(x)
                self.assertEqual(result, true_)

    def test_two_simple_multipliers(self):
        for x, true_ in zip([6, 26, 121],
                            [(2, 3), (2, 13), (11, 11)]):
            with self.subTest(case=x):
                result = factorize(x)
                self.assertIsInstance(result, tuple)
                self.assertCountEqual(result, true_)

    def test_many_multipliers(self):
        for x, true_ in zip([1001, 9699690],
                            [(7, 11, 13), (2, 3, 5, 7, 11, 13, 17, 19)]):
            with self.subTest(case=x):
                result = factorize(x)
                self.assertIsInstance(result, tuple)
                self.assertCountEqual(result, true_)


# if __name__ == '__main__':
#     unittest.main()