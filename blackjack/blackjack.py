# Black Jack Game

import numpy as np
from os import system, name
from time import sleep

# Global parameter used to configure the default init value of the Dealer's bank
dealer_default_init_bank = 50000


class Card:

    # Class Object attribute
    rank_set = {2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'}
    suit_symbol_dict = {'Clubs': '\u2663', 'Diamonds': '\u2666', 'Hearts': '\u2665', 'Spades': '\u2660'}

    def __init__(self, rank, suit, up=True):
        self.rank = rank
        self.suit = suit
        self.up = up
        # Initialize the value
        if type(self.rank) == int:
            self.value = self.rank
        elif self.rank in {'J', 'Q', 'K'}:
            self.value = 10
        elif self.rank == 'A':
            self.value = (1, 10)

    def __str__(self):
        return f"------------\n" \
               "|{0!s:<10}|\n".format(self.rank) + \
               "|          |\n" + \
               "|{0!s:^10}|\n".format(Card.suit_symbol_dict[self.suit]) + \
               "|          |\n" + \
               "|{0!s:>10}|\n".format(self.rank) + \
               f"------------\n"


class Deck:

    def __init__(self):
        # Initialize the Deck with its 52 cards
        cards = []
        for suit in Card.suit_symbol_dict:
            for rank in Card.rank_set:
                cards.append(Card(rank, suit))
        self.cards = cards

    def shuffle(self):
        """Shuffles the deck of cards"""
        np.random.shuffle(self.cards)

    def pop_card(self):
        """Pops a card from the deck
        :return a Card
        """
        # If there are still cards in the deck, pop a card. Else create a new deck and pop a card
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            self.__init__()
            print('Using a new deck of card')
            self.shuffle()
            return self.cards.pop()


# A CardHolder will be a parent Class for Dealer and Player as both hold cards and share common methods
class CardHolder:

    def __init__(self):
        self.cards = []

    def cards_str(self):
        """Returns a string representing the dealer's current cards"""
        nb_cards = len(self.cards)
        if nb_cards > 0:
            card_down_block = "|"+"\u2591"*8 +"|  "
            line1 = f"----------  " * nb_cards + "\n"
            line2_lst = []
            for k in range(nb_cards):
                # If the card is up: simply add the string and display the card rank and suit
                if self.cards[k].up:
                    line2_lst.append("|{0!s:<8}|  ".format(self.cards[k].rank))
                # Else (card down): hide card characteristics
                else:
                    line2_lst.append(card_down_block)
            line2 = ''.join(line2_lst) + "\n"
            line3_lst = []
            for k in range(nb_cards):
                if self.cards[k].up:
                    line3_lst.append("|        |  ".format(self.cards[k].rank))
                else:
                    line3_lst.append(card_down_block)
            line3 = ''.join(line3_lst) + "\n"
            line4_lst = []
            for k in range(nb_cards):
                # If the card is up: simply add the string and display the card rank and suit
                if self.cards[k].up:
                    line4_lst.append("|{0!s:^8}|  ".format(Card.suit_symbol_dict[self.cards[k].suit]))
                # Else (card down): hide card characteristics
                else:
                    line4_lst.append(card_down_block)
            line4 = ''.join(line4_lst) + "\n"
            line5 = line3
            # line6_lst = ["|{0!s:>8}|  ".format(self.cards[x].rank) for x in range(nb_cards)]
            line6_lst = []
            for k in range(nb_cards):
                # If the card is up: simply add the string and display the card rank and suit
                if self.cards[k].up:
                    line6_lst.append("|{0!s:>8}|  ".format(self.cards[k].rank))
                # Else (card down): hide card characteristics
                else:
                    line6_lst.append("|        |  ")
            line6_lst = []
            for k in range(nb_cards):
                if self.cards[k].up:
                    line6_lst.append("|{0!s:>8}|  ".format(self.cards[k].rank))
                else:
                    line6_lst.append(card_down_block)
            line6 = ''.join(line6_lst) + "\n"
            line7 = line1
            my_string = ''.join([line1, line2, line3, line4, line5, line6, line7])
            return my_string
        # Else, if no cards in the deck, return an empty spot for the card
        else:
            return "----------\n" \
            "|        |\n" \
            "|        |\n" \
            "|        |\n" \
            "|        |\n" \
            "|        |\n" \
            "----------\n"


class Dealer(CardHolder):

    def __init__(self, bankroll=dealer_default_init_bank, player=None):
        CardHolder.__init__(self)
        self.deck = Deck()
        self.deck.shuffle()
        self.bankroll = bankroll
        self.player = player

    def hit(self):
        """Dealer hits the deck:
        a card is popped out of the dealer's deck and appended to the dealer's cards"""
        self.cards.append(self.deck.pop_card())

    def beat(self):
        """Dealer beats the player: he gets the bet from the player and the player's bet is reset to 0"""
        self.bankroll += self.player.bet
        self.player.bet = 0

    def bust(self):
        """Player busts: the player gets his bet back and gets paid 2x his bet by the dealer"""
        self.bankroll -= self.player.bet * 2
        # The player gets his bet back (x1) and get paid 2x his bet by the dealer
        self.player.bankroll += self.player.bet * 3
        # The player bet is reset to 0
        self.player.bet = 0


class Player (CardHolder):

    def __init__(self, bankroll, dealer=None):
        CardHolder.__init__(self)
        self.bankroll = bankroll
        self.bet = 0
        self.dealer = dealer

    def set_bet(self, bet):
        """Player bets: his bet is taken out of his bankroll and set on his bet attribute
        :return True if bankroll is sufficient to place the bet, else False"""
        if self.bankroll >= self.bet:
            self.bankroll -= bet
            self.bet = bet
            return True
        else:
            return False

    def hit(self):
        """Player hits the dealer:
        a card is popped out of the dealer's deck and appended to the player's list of cards"""
        self.cards.append(self.dealer.deck.pop_card())

    def stay(self):
        pass

    def bust(self):
        """Player busts: the dealer gets the bet and the player loses it"""
        self.dealer.bankroll += self.bet
        self.bet = 0


def clear():
    """Define a function to clear the screen in terminal"""
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


class Table:

    def __init__(self, dealer=None, player=None):
        self.dealer = dealer
        self.player = player

    # define our clear function

    def display(self):
        """Display the table with the dealer and player cards, bet, status, call for action"""
        # Start by clearing the terminal
        clear()
        print('-'*10 + '{0!s:<16}'.format(' DEALER \u23ea') + '-'*10)
        # Bankroll and action
        print('{0!s:<10}${1:>11,}'.format('BANKROLL:', self.dealer.bankroll))
        print(self.dealer.cards_str())
        # print(f'BET \u229a {self.player.bet}')
        print('{0!s:>10}${1:>11,}'.format('BET: ', self.player.bet))
        # Player's side
        print(self.player.cards_str())
        # Print bars meant to visually represent the amount of money in the bank
        # print('.'*5)
        print('{0!s:<10}${1:>11,}'.format('BANKROLL:', self.player.bankroll))
        print('-'*10 + '{0!s:<16}'.format(' PLAYER \u23ea') + '-'*10)


if __name__ == "__main__":
    # Create a test player and dealer
    test_player = Player(1000)
    test_dealer = Dealer(player=test_player)
    test_player.dealer = test_dealer
    # Create the Table
    table = Table(dealer=test_dealer, player=test_player)
    # Dealer hits two cards
    for i in range(3):
        test_dealer.hit()
        if i == 1:
            test_dealer.cards[-1].up = False
        test_player.hit()
    # Display the table
    table.display()
