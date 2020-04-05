import blackjackclasses as bj
from time import sleep

# Global parameters
initial_player_bankroll = 1000
initial_dealer_bankroll = 50000
minimum_bet = 10


class InvalidBetAmount(Exception):
    pass


class InvalidAction(Exception):
    pass


if __name__ == "__main__":

    # Create the player, the dealer and set the table
    player = bj.Player(initial_player_bankroll)
    dealer = bj.Dealer(player=player, bankroll=initial_dealer_bankroll)
    player.dealer = dealer
    table = bj.Table(dealer=dealer, player=player)
    # Initialize the player as being playing
    player_is_playing = True

    while player_is_playing:
        # Reset the player and dealer cards
        player.cards = []
        dealer.cards = []
        player.bust_status = False
        # Display the table
        table.display()
        # Place a bet
        while True:
            try:
                bet = int(input('Place your bet:'))
                if (bet < player.bankroll) and (bet >= minimum_bet):
                    out = player.set_bet(bet)
                    break
                else:
                    raise InvalidBetAmount
            except InvalidBetAmount:
                print(f'Please enter a valid bet amount (in between ${minimum_bet:,} and ${player.bankroll:,})')
            except Exception:
                print('Please enter a valid bet amount')
        # Dealer deals cards (1 for player, 1 for dealer, 1 for player, 1 for dealer face down)
        player.hit()
        table.display()
        dealer.hit()
        table.display()
        player.hit()
        table.display()
        dealer.hit(up=False)
        table.display()
        # Dealer check the cards distributed and verify if there is a Black Jack

        # Player Hits or Stays
        # Loop as long as it it the player's turn (as long as he does not Bust or Stay)
        player.turn = True
        while player.turn:

            # Get the player action
            while True:
                try:
                    action = input('Hit or Stay [H/S]:')
                    if action.upper() == 'H':
                        player.hit()
                        table.display()
                        break
                    elif action.upper() == 'S':
                        player.turn = False
                        break
                    else:
                        raise InvalidAction
                except InvalidAction:
                    print(f'Please enter a valid action ("H" for Hit or "S" for Stay)')

            # If the player is still under 21, he can continue to chose to either Hit or Stay
            if player.cards_value() < 21:
                continue
            # Else if 21, then it is the dealer's turn (still possibility of tie if dealer gets 21 as well)
            elif player.cards_value() == 21:
                print('Player has 21')
                player.turn = False
                break
            # Else player Bust
            else:
                player.bust()
                print('\n########## Player Bust !!! \u26b0')
                sleep(3)
                player.turn = False
                break

        # If the player is out of his turn because he Bust, then go back straight at the start of the game loop
        if player.bust_status:
            continue

        # If player not bust, It is now the turn of the dealer
        dealer.turn = True
        # Dealer reveals his second card
        dealer.cards[-1].up = True
        table.display()
        # Dealer Hits until he Beats or Busts
        while dealer.cards_value() < 21:
            dealer.hit()
            table.display()
        # End of that hand
        print('END OF THAT HAND')
        # Refresh Bankroll amounts

        # Ask the player if he wants to continue
        player_is_playing = False
