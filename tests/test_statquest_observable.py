import random
from unittest import TestCase

from statquest_observable import Observable


class TestObservable(TestCase):

    def setUp(self):
        self.N = 100
        data_int = {i: int(100 * i) for i in range(1, self.N + 1)}
        data_float = {i: float(100 * i) for i in range(1, self.N + 1)}
        data_str = {i: str(100 * i) for i in range(1, self.N + 1)}
        self.observable_ordinal = Observable('ord obs', data_int)
        self.observable_continuous = Observable('cont obs', data_float)
        self.observable_nominal = Observable('nom obs', data_str)
        del data_int
        del data_float
        del data_str

    def tearDown(self):
        del self.observable_ordinal
        del self.observable_continuous
        del self.observable_nominal

    def test___init__1(self):
        self.assertIsInstance(self.observable_ordinal, Observable)
        self.assertIsNotNone(self.observable_ordinal.name)
        self.assertIsNotNone(self.observable_ordinal.data)
        self.assertEqual(True, self.observable_ordinal.IS_ORDINAL)
        self.assertEqual(False, self.observable_ordinal.IS_CONTINUOUS)
        self.assertEqual(False, self.observable_ordinal.IS_NOMINAL)

    def test___init__2(self):
        self.assertIsInstance(self.observable_continuous, Observable)
        self.assertIsNotNone(self.observable_continuous.name)
        self.assertIsNotNone(self.observable_continuous.data)
        self.assertEqual(False, self.observable_continuous.IS_ORDINAL)
        self.assertEqual(True, self.observable_continuous.IS_CONTINUOUS)
        self.assertEqual(False, self.observable_continuous.IS_NOMINAL)

    def test___init__3(self):
        self.assertIsInstance(self.observable_nominal, Observable)
        self.assertIsNotNone(self.observable_nominal.name)
        self.assertIsNotNone(self.observable_nominal.data)
        self.assertEqual(False, self.observable_nominal.IS_ORDINAL)
        self.assertEqual(False, self.observable_nominal.IS_CONTINUOUS)
        self.assertEqual(True, self.observable_nominal.IS_NOMINAL)

    def test___getitem__1(self):
        for i in range(1, self.N + 1):
            vo = self.observable_ordinal[i]
            vc = self.observable_continuous[i]
            vn = self.observable_nominal[i]
            self.assertIsInstance(vo, int)
            self.assertIsInstance(vc, float)
            self.assertIsInstance(vn, str)
            self.assertEqual(int(100 * i), vo)
            self.assertEqual(float(100 * i), vc)
            self.assertEqual(str(100 * i), vn)

    def test___getitem__2(self):
        for i in range(self.N, 0, -1):
            vo = self.observable_ordinal[i]
            vc = self.observable_continuous[i]
            vn = self.observable_nominal[i]
            self.assertIsInstance(vo, int)
            self.assertIsInstance(vc, float)
            self.assertIsInstance(vn, str)
            self.assertEqual(int(100 * i), vo)
            self.assertEqual(float(100 * i), vc)
            self.assertEqual(str(100 * i), vn)

    def test___getitem__3(self):
        for j in range(self.N):
            i = random.randint(1, self.N)
            vo = self.observable_ordinal[i]
            vc = self.observable_continuous[i]
            vn = self.observable_nominal[i]
            self.assertIsInstance(vo, int)
            self.assertIsInstance(vc, float)
            self.assertIsInstance(vn, str)
            self.assertEqual(int(100 * i), vo)
            self.assertEqual(float(100 * i), vc)
            self.assertEqual(str(100 * i), vn)

    def test___len__1(self):
        lo = len(self.observable_ordinal)
        lc = len(self.observable_continuous)
        ln = len(self.observable_nominal)
        self.assertEqual(self.N, lo)
        self.assertEqual(self.N, lc)
        self.assertEqual(self.N, ln)

    def test___len__2(self):
        obs = Observable('an observable', {})
        result = len(obs)
        expected = 0
        self.assertEqual(expected, result)

    def test___str__1(self):
        self.assertEqual('ord obs', str(self.observable_ordinal))
        self.assertEqual('cont obs', str(self.observable_continuous))
        self.assertEqual('nom obs', str(self.observable_nominal))

    def test_nominals_1(self):
        result = self.observable_ordinal.nominals()
        expected = [str(100 * i) for i in range(1, self.N + 1)]
        self.assertListEqual(sorted(expected), sorted(result))

    def test_nominals_2(self):
        result = self.observable_continuous.nominals()
        expected = [str(100.0 * i) for i in range(1, self.N + 1)]
        self.assertEqual(sorted(expected), sorted(result))

    def test_nominals_3(self):
        result = self.observable_nominal.nominals()
        expected = [str(100 * i) for i in range(1, self.N + 1)]
        self.assertListEqual(sorted(expected), sorted(result))

    def test_ordinals_1(self):
        result = self.observable_ordinal.ordinals()
        expected = [100 * i for i in range(1, self.N + 1)]
        self.assertListEqual(expected, result)

    def test_ordinals_2(self):
        result = self.observable_continuous.ordinals()
        expected = [100 * i for i in range(1, self.N + 1)]
        self.assertListEqual(expected, result)

    def test_ordinals_3(self):
        result = self.observable_nominal.ordinals()
        expected = [100 * i for i in range(1, self.N + 1)]
        self.assertListEqual(expected, result)

    def test_values_as_sorted_list_1(self):
        result = self.observable_ordinal.values_as_sorted_list()
        expected = [int(100 * i) for i in range(1, self.N + 1)]
        expected = sorted(expected)
        self.assertListEqual(expected, result)

    def test_values_as_sorted_list_2(self):
        result = self.observable_continuous.values_as_sorted_list()
        expected = [float(100 * i) for i in range(1, self.N + 1)]
        expected = sorted(expected)
        self.assertListEqual(expected, result)

    def test_values_as_sorted_list_3(self):
        result = self.observable_nominal.values_as_sorted_list()
        expected = [str(100 * i) for i in range(1, self.N + 1)]
        expected = sorted(expected)
        self.assertListEqual(expected, result)

    def test_values_to_indices_dict_1(self):
        result = self.observable_ordinal.values_to_indices_dict()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertEqual(self.N, len(result))

    def test_values_to_indices_dict_2(self):
        result = self.observable_continuous.values_to_indices_dict()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertEqual(self.N, len(result))

    def test_values_to_indices_dict_3(self):
        result = self.observable_nominal.values_to_indices_dict()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertEqual(self.N, len(result))

    def test_values_to_indices_dict_4(self):
        obs = Observable('O', {12: 5, 21: -1, 40: 15, 100: 9, 200: 15})
        result = obs.values_to_indices_dict()
        expected = {-1: 0, 5: 1, 9: 2, 15: 3}
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertDictEqual(expected, result)

    def test_values_to_indices_dict_5(self):
        obs = Observable('O',
                         {12: 5.0, 21: -1.0, 40: 15.2, 100: 9.0, 200: 15.2})
        result = obs.values_to_indices_dict()
        expected = {-1.0: 0, 5.0: 1, 9.0: 2, 15.2: 3}
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertDictEqual(expected, result)

    def test_values_to_indices_dict_6(self):
        obs = Observable('O', {12: '5.0', 21: '-1.0', 40: '15.2', 100: '9.0',
                               200: '15.2'})
        result = obs.values_to_indices_dict()
        expected = {'-1.0': 0, '15.2': 1, '5.0': 2, '9.0': 3}
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertDictEqual(expected, result)

    def test_values_to_indices_dict_7(self):
        obs = Observable('O', dict())
        result = obs.values_to_indices_dict()
        expected = dict()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertDictEqual(expected, result)

    def test_frequency_table_1(self):
        result = self.observable_ordinal.frequency_table()
        expected = {int(100 * i): 1 for i in range(1, self.N + 1)}
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertDictEqual(expected, result)

    def test_frequency_table_2(self):
        result = self.observable_continuous.frequency_table()
        expected = {float(100 * i): 1 for i in range(1, self.N + 1)}
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertDictEqual(expected, result)

    def test_frequency_table_3(self):
        result = self.observable_nominal.frequency_table()
        expected = {str(100 * i): 1 for i in range(1, self.N + 1)}
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertDictEqual(expected, result)

    def test_frequency_table_4(self):
        obs = Observable('obs', {5: 1, 7: 1, 8: 1, 20: 2, 21: 33, 22: 33})
        result = obs.frequency_table()
        expected = {1: 3, 2: 1, 33: 2}
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertDictEqual(expected, result)

    def test_frequency_table_5(self):
        obs = Observable('obs',
                         {5: 1.0, 7: 1.0, 8: 1.0, 20: 2.0, 21: 33.0, 22: 33})
        result = obs.frequency_table()
        expected = {1.0: 3, 2.0: 1, 33.0: 2}
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertDictEqual(expected, result)

    def test_frequency_table_6(self):
        obs = Observable('obs',
                         {5: '1', 7: '1', 8: '1', 20: '2.0', 21: 'X', 22: 'X'})
        result = obs.frequency_table()
        expected = {'1': 3, '2.0': 1, 'X': 2}
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertDictEqual(expected, result)

    def test_frequency_table_7(self):
        obs = Observable('obs',
                         {5: 1, 7: 1, 8: 1, 20: 2.0, 21: 'X', 22: 'X'})
        result = obs.frequency_table()
        expected = {1: 3, 2.0: 1, 'X': 2}
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertDictEqual(expected, result)

    def test_frequency_table_8(self):
        result = Observable('obs', {}).frequency_table()
        expected = {}
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertDictEqual(expected, result)

    # def test_descriptive_statistics(self):
    #     self.fail()
    #
    # def test_print_descriptive_statistics(self):
    #     self.fail()

    def test__check_data_kind_1(self):
        r_int = self.observable_ordinal._check_data_kind(int)
        r_float = self.observable_ordinal._check_data_kind(float)
        r_str = self.observable_ordinal._check_data_kind(str)
        self.assertEqual(True, r_int)
        self.assertEqual(False, r_float)
        self.assertEqual(False, r_str)

    def test__check_data_kind_2(self):
        r_int = self.observable_continuous._check_data_kind(int)
        r_float = self.observable_continuous._check_data_kind(float)
        r_str = self.observable_continuous._check_data_kind(str)
        self.assertEqual(False, r_int)
        self.assertEqual(True, r_float)
        self.assertEqual(False, r_str)

    def test__check_data_kind_3(self):
        r_int = self.observable_nominal._check_data_kind(int)
        r_float = self.observable_nominal._check_data_kind(float)
        r_str = self.observable_nominal._check_data_kind(str)
        self.assertEqual(False, r_int)
        self.assertEqual(False, r_float)
        self.assertEqual(True, r_str)

    def test__check_data_kind_4(self):
        obs = Observable('O', {1: 1, 2: 2.0, 3: 'iii'})
        r_int = obs._check_data_kind(int)
        r_float = obs._check_data_kind(float)
        r_str = obs._check_data_kind(str)
        self.assertEqual(False, r_int)
        self.assertEqual(False, r_float)
        self.assertEqual(False, r_str)

    def test__check_data_kind_5(self):
        obs = Observable('O', {})
        r_int = obs._check_data_kind(int)
        r_float = obs._check_data_kind(float)
        r_str = obs._check_data_kind(str)
        self.assertEqual(False, r_int)
        self.assertEqual(False, r_float)
        self.assertEqual(False, r_str)
