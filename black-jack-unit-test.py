import unittest
import blackjack as bj


class TestBlackJack(unittest.TestCase):

    def test_card_attributes_assignment(self):
        card = bj.Card('A', 'Spades')
        self.assertEqual((card.rank, card.suit), ('A', 'Spades'))

    def test_deck_created_with_52_cards(self):
        deck = bj.Deck()
        self.assertEqual(len(deck.cards), 52)


if __name__ == "__main__":
    unittest.main()
