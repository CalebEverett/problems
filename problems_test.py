from deck import Card, Rank, Suit
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


if __name__ == "__main__":
    unittest.main()
