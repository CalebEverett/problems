from deck import Card, Deck, Rank, Suit
from parens import parens_from_strings, parens_from_partitions
import unittest


class TestDeck(unittest.TestCase):
    def test_card_eq(self):
        """Cards with same rank and same suit are equal."""

        for r in Rank:
            with self.subTest("Rank", r=r):
                self.assertEqual(Card(r, Suit(1)), Card(r, Suit(1)))

    def test_card_lt(self):
        """Cards with lower rank are less than cards with higher rank."""

        rank_list = list(Rank)
        for i in range(1, len(rank_list)):
            with self.subTest("Rank", i=i):
                self.assertLess(
                    Card(rank_list[i - 1], Suit(1)), Card(rank_list[i], Suit(1))
                )

    def test_card_gt(self):
        """Cards with higher rank are greater than cards with lower rank."""

        rank_list = list(Rank)
        for i in range(1, len(rank_list)):
            with self.subTest("Rank", i=i):
                self.assertGreater(
                    Card(rank_list[i], Suit(1)), Card(rank_list[i - 1], Suit(1))
                )

    def test_card_pop_slice(self):
        """Cards returned by indexing are removed from deck."""

        deck = Deck()
        cards = deck[:3]
        self.assertEqual(len(cards), 3)
        self.assertEqual(len(deck), 49)


class TestParens(unittest.TestCase):
    def test_strings(self):
        """Binary string construction returns the correct number of valid combinations."""

        correct = {1: 1, 2: 2, 3: 5, 4: 14}

        for n in correct:
            with self.subTest("Rank", n=n):
                self.assertEqual(len(parens_from_strings(n)), correct[n])

    def test_partitions(self):
        """Permutations of partitions construction returns the correct number of valid
        combinations."""

        correct = {1: 1, 2: 2, 3: 5, 4: 14}

        for n in correct:
            with self.subTest("Rank", n=n):
                self.assertEqual(len(parens_from_partitions(n)), correct[n])

    def test_methods_equal(self):
        """Both methods return the same result for larger values of n."""

        for n in [6, 8, 10]:
            with self.subTest("Rank", n=n):
                self.assertEqual(
                    len(parens_from_strings(n)), len(parens_from_partitions(n))
                )


if __name__ == "__main__":
    unittest.main()
