import unittest
from parameterized import parameterized

from src.constants import UKR_ALPHABET_LOWER

def ind(s):
    print(s)
    result = []
    for c in s:
        result.append(UKR_ALPHABET_LOWER.index(c.lower()))
    return result

class Test(unittest.TestCase):

    @parameterized.expand([
        [
            ['іскоростень', 'Ямпіль', 'Алушта', 'Їванків', 'Інакше', 'Іванків'],
            ['Алушта', 'Іванків', 'Інакше', 'іскоростень', 'Їванків', 'Ямпіль']
        ]
    ])
    def test_sorting(self, input_arr, expected):
        # input_arr.sort(key=lambda word: [UKR_ALPHABET_LOWER.index(c.lower()) for c in word])
        input_arr.sort(key=ind)
        self.assertEqual(expected, input_arr)


if __name__ == '__main__':
    unittest.main()
