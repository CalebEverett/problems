# create a deck of 52 cards
# ranks (2-10 and J,Q,K,A)
# suits (spades, diamonds, clubs, hearts)

# print all cards
# get first/last card
# get last 3 cards
# get number of cards in deck
# is 3 of diamonds in the deck
# get random card

# reverse deck
# shuffle deck
# =============================================================================

from dataclasses import dataclass
from enum import Enum
from functools import total_ordering
import random


Rank = Enum("Rank", (" ").join(map(str, range(2, 11))) + " Jack Queen King Ace")
Suit = Enum("Suit", "Club Diamond Heart Spade")


@total_ordering
@dataclass
class Card:
    rank: Rank
    suit: Suit

    def _is_valid_operand(self, other):
        return other.__class__ == self.__class__

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return (self.rank.value, self.suit.value) == (
            other.rank.value,
            other.suit.value,
        )

    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return (self.rank.value, self.suit.value) < (other.rank.value, other.suit.value)

    def __repr__(self):
        symbols = (
            "\N{Black Club Suit}",
            "\N{Black Diamond Suit}",
            "\N{Black Heart Suit}",
            "\N{Black Spade Suit}",
        )

        symbol = symbols[self.suit.value - 1]

        return (
            f"{self.__class__.__name__}<{self.rank.name} of {self.suit.name}s {symbol}>"
        )


class Deck:
    def __init__(self):
        self.cards = [
            Card(Rank(r), Suit(s)) for s in range(4, 0, -1) for r in range(13, 0, -1)
        ]

    def __len__(self):
        return len(self.cards)

    def shuffle(self):
        random.shuffle(self.cards)

    def reverse(self):
        self.cards = self.cards[::-1]

    def get_card(
        self,
        rank: str,
        suit: str,
    ) -> Card:
        card_to_get = Card(Rank[rank], Suit[suit])
        for i, card in enumerate(self.cards):
            if card == card_to_get:
                return self.cards.pop(i)
        msg = f"{rank} of {suit}s not found."
        raise Exception(msg)

    def __iter__(self):
        return self

    def __next__(self):
        if not self.cards:
            raise StopIteration
        return self.cards.pop()

    def __getitem__(self, slice):
        cards = self.cards[slice]
        for card in cards:
            self.cards.remove(card)
        return cards

    def __repr__(self):
        cards_string = ("\n").join([f"\t{c.__repr__()}" for c in self.cards])
        return f"{self.__class__.__name__}<{self.__len__()} cards>\n{cards_string}"


if __name__ == "__main__":
    counter = 0
    print_n = 5
    deck = Deck()

    print(f"Createe deck with {len(deck)} cards.\n")

    print("Printing card...")
    card = deck.get_card("Ace", "Spade")
    print(card, "\n")

    print("Printing cards from deck...")
    for card in deck:
        print(card)
        counter += 1
        if counter == print_n:
            break
    print("\n")

    counter = 0
    print("Printing cards from reversed deck...")
    deck.reverse()
    for card in deck:
        print(card)
        counter += 1
        if counter == print_n:
            break
    print("\n")

    counter = 0
    print("Printing cards from shuffled deck...")
    deck.shuffle()
    for card in deck:
        print(card)
        counter += 1
        if counter == print_n:
            break
    print("\n")

    print("Printing deck ...")
    print(deck)
    print("\n")
