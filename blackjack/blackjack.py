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

        # Place a bet (get user input for bet)
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
        if dealer.check_if_blackjack():
            player.win_with_blackjack()
            print('\n########## Player Wins with Black Jack !!!')
            sleep(3)
            continue

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
                print('\n########## Player has 21 !!!')
                player.turn = False
                break
            # Else player Bust
            else:
                player.bust()
                print('\n########## Player Bust !!!')
                sleep(3)
                player.turn = False
                break
        # If the player Bust, then start new hand (back on top)
        if player.bust_status:
            continue

        # If player not bust, it is now the turn of the dealer
        dealer.turn = True
        # Dealer reveals his second card
        dealer.cards[-1].up = True
        table.display()

        # Dealer Hits until he Beats or Busts
        while True:
            dealer.hit()
            table.display()
            # Check if the dealer has beat
            if (dealer.cards_value() > player.cards_value()) and \
                    (dealer.cards_value() <= 21):
                dealer.beat()
                sleep(3)
                print('\n########## Dealer Beat the player !!!')
                sleep(3)
                break
            elif dealer.cards_value() == player.cards_value() == 21:
                player.tie()
                sleep(3)
                print('\n########## This is a Tie !!!')
                sleep(3)
                break
            # Else, dealer Busts
            else:
                dealer.bust()
                sleep(3)
                print('\n########## Dealer has Bust !!!')
                sleep(3)
                break

        # Continue playing
        player_is_playing = True
