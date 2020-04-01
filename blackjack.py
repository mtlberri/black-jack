# Black Jack Game

import numpy as np


class Card:

    # Class Object attribute
    rank_set = {2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'}
    suit_symbol_dict = {'Clubs': '\u2663', 'Diamonds': '\u2666', 'Hearts': '\u2665', 'Spades': '\u2660'}

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
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


if __name__ == "__main__":
    test_deck = Deck()