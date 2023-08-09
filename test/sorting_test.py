import unittest
from parameterized import parameterized

from app.service.finders import sort_keys
from app.db.models import UaLocationsSettlement


def create_dummy_settlements(input_arr):
    return [UaLocationsSettlement(name_lower=name) for name in input_arr]


class Test(unittest.TestCase):

    @parameterized.expand([
        [
            ['іскоростень', 'ямпіль', 'алушта', 'їванків', 'інакше', 'іванків'],
            ['алушта', 'іванків', 'інакше', 'іскоростень', 'їванків', 'ямпіль']
        ]
    ])
    def test_sorting(self, input_arr, expected_result):
        input_settlements = create_dummy_settlements(input_arr)

        input_settlements.sort(key=sort_keys)
        actual_result = [s.name_lower for s in input_settlements]

        self.assertEqual(expected_result, actual_result)


if __name__ == '__main__':
    unittest.main()
