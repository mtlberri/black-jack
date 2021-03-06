import unittest
from blackjack import blackjackclasses as bj


class TestBlackJack(unittest.TestCase):

    def test_card_attributes_assignment(self):
        card = bj.Card('A', 'Spades')
        self.assertEqual((card.rank, card.suit), ('A', 'Spades'))

    def test_deck_created_with_52_cards(self):
        deck = bj.Deck()
        self.assertEqual(len(deck.cards), 52)

    def test_player_set_bet(self):
        test_player = bj.Player(1000)
        success = test_player.set_bet(100)
        self.assertEqual((success, test_player.bet, test_player.bankroll), (True, 100, 900))

    def test_player_receives_a_card_when_first_hit(self):
        # Test player and dealer initialization
        test_player = bj.Player(1000)
        test_dealer = bj.Dealer(player=test_player)
        test_player.dealer = test_dealer
        # Test player hits the dealer
        initial_nb_cards = len(test_player.cards)
        test_player.hit()
        nb_cards_after_hit = len(test_player.cards)
        self.assertEqual(initial_nb_cards + 1, nb_cards_after_hit)

    def test_player_bust(self):
        # Test player and dealer initialization
        test_player = bj.Player(1000)
        test_dealer = bj.Dealer(player=test_player)
        test_player.dealer = test_dealer
        # Test player sets a $100 bet, hits and bust
        test_player.set_bet(100)
        test_player.hit()
        test_player.bust()
        self.assertEqual((test_player.bankroll, test_player.bet, test_dealer.bankroll),
                         (900, 0, 50000 + 100))

    def test_dealer_hit(self):
        test_dealer = bj.Dealer()
        initial_nb_cards = len(test_dealer.cards)
        test_dealer.hit()
        nb_cards_after_hit = len(test_dealer.cards)
        self.assertEqual(initial_nb_cards + 1, nb_cards_after_hit)

    def test_dealer_beat(self):
        # Test player and dealer initialization
        test_player = bj.Player(1000)
        test_player.set_bet(400)
        test_dealer = bj.Dealer(player=test_player)
        test_player.dealer = test_dealer
        test_dealer.beat()
        self.assertEqual((test_dealer.bankroll, test_player.bankroll, test_player.bet),
                         (50000 + 400, 600, 0))

    def test_dealer_bust(self):
        # Test player and dealer initialization
        test_player = bj.Player(1000)
        test_player.set_bet(400)
        test_dealer = bj.Dealer(player=test_player)
        test_player.dealer = test_dealer
        test_dealer.bust()
        self.assertEqual((test_dealer.bankroll, test_player.bankroll, test_player.bet),
                         (50000 - 400, 1400, 0))

    def test_dealer_check_blackjack(self):
        # Test player and dealer initialization
        test_player = bj.Player(1000)
        test_player.set_bet(400)
        test_dealer = bj.Dealer(player=test_player)
        test_player.dealer = test_dealer
        # Give the player a Black Jack hand
        test_player.cards.append(bj.Card('A', 'Clubs'))
        test_player.cards.append(bj.Card('K', 'Diamonds'))
        self.assertEqual(test_dealer.check_if_blackjack(), True)

    def test_Aces_Adjustment(self):
        # Test player and dealer initialization
        test_dealer = bj.Dealer()
        test_player = bj.Player(1000)
        # Dealer hand: AAJ7 = 19
        test_dealer.cards = [bj.Card('A', 'Clubs'), bj.Card('A', 'Clubs'),
                             bj.Card('J', 'Clubs'), bj.Card(7, 'Clubs')]
        test_dealer.aces = 2
        # Player hand A2 = 13
        test_player.cards = [bj.Card('A', 'Clubs'), bj.Card(2, 'Clubs')]
        test_player.aces = 1
        self.assertEqual((test_dealer.cards_value(), test_player.cards_value()),
                         (19, 13))


if __name__ == "__main__":
    unittest.main()
