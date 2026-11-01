import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import logic  # noqa: E402


class TestIndexing(unittest.TestCase):
    def test_alphabet_size(self):
        self.assertEqual(logic.N_ALPHABET, 31)

    def test_letter_index(self):
        self.assertEqual(logic.letter_index("A"), 1)
        self.assertEqual(logic.letter_index("Ă"), 2)
        self.assertEqual(logic.letter_index("Z"), 31)
        self.assertEqual(logic.letter_index("ș"), 23)

    def test_name_minterms(self):
        self.assertEqual(logic.minterms_from_text("SIMION"), [0, 1, 2, 6, 11])
        self.assertEqual(logic.minterms_from_text("SIMIONESCU"), [0, 1, 2, 5, 6, 7, 10, 11])


class TestMinimization(unittest.TestCase):
    def setUp(self):
        self.ms = logic.minterms_from_text("SIMIONESCU")

    def test_expression(self):
        covers = logic.minimal_covers(self.ms)
        self.assertEqual(logic.expression(covers[0]), "A'B'C' + A'CD' + A'BD + AB'C")

    def test_all_covers_correct(self):
        for cover in logic.minimal_covers(self.ms):
            for m in range(16):
                self.assertEqual(logic.evaluate(cover, m), m in self.ms)

    def test_full_function(self):
        self.assertEqual(logic.expression(logic.minimal_covers(list(range(16)))[0]), "1")


if __name__ == "__main__":
    unittest.main()
