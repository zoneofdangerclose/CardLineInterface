import argparse
import random
from thefuzz import process
import copy
import os
import pandas as pd
import numpy as np
import logging
logger = logging.getLogger(__name__)
from datetime import date

class bank:
    """Generates and maintains a file that tracks players chip count.

    TODO:
    Current iteration only has a guest username, but has some infrastructure for multiple profiles.
    """
    def __init__(self):
        self.bank_df = pd.DataFrame()
  
    def start_game(self):
        if os.path.exists('bank.csv') is False:
            print('construcing bank')
            bank_df = pd.DataFrame({
                'username': ['guest'],
                'blackjack chip count': [100],
                'poker chip count': [100],
            })

            bank_df.to_csv('bank.csv', index=False)

            self.bank_df = pd.read_csv('bank.csv')

        elif os.path.exists('bank.csv') is True:
            self.bank_df = pd.read_csv('bank.csv')

    def updatechipcount(self, chipcount, username, game, bank_df):
        bank_df.loc[bank_df['username'] == username, f'{game} chip count'] = [chipcount]
        self.bank_df = bank_df
        self.bank_df.to_csv('bank.csv', index=False)

class actor:
    """Describes actors that are computer controlled opponents"""
    def __init__(self, name):
        """Initalize empty containers and standard values."""
        self.hand = []
        self.chip_count = 0
        self.name = name

    def logic(self, logic):
        """Logical flows for decision making"""

        if logic == "aggressive":
            print("Aggressive")
        elif logic == "defensive":
            print("Defensive")
        elif logic == "Random":
            print("Random")
        else:
            print("Random")


class blackjack:
    def __init__(self):
        """Initalize empty containers and standard values based on the game mode."""
        self.player_hand = []
        self.dealer_hand = []
        # self.chip_count = []

        self.player_hand_score = 0
        self.dealer_hand_score = 0

        self.card_rank_dict = {
            'A': 11,
            'K': 10,
            'Q': 10,
            'J': 10,
            'T': 10,
        }

        self.handsize = 2

        self.deck = ['A♣', '2♣', '3♣', '4♣', '5♣', '6♣', '7♣', '8♣', '9♣', 'T♣', 'J♣', 'Q♣', 'K♣', 'A♦', '2♦', '3♦', '4♦', '5♦', '6♦', '7♦', '8♦', '9♦', 'T♦', 'J♦', 'Q♦', 'K♦', 'A♥', '2♥', '3♥', '4♥', '5♥', '6♥', '7♥', '8♥', '9♥', 'T♥', 'J♥', 'Q♥', 'K♥', 'A♠', '2♠', '3♠', '4♠', '5♠', '6♠', '7♠', '8♠', '9♠', 'T♠', 'J♠', 'Q♠', 'K♠']

        self.metadata = {
            'player_hand':self.player_hand,
            'dealer_hand':self.dealer_hand,
            'player_hand_score':self.player_hand_score,
            'dealer_hand_score':self.dealer_hand_score
        }
    
    def metadata_update(self, update_key, update_value):
        """"Utility function that updates key values for logging."""
        keys = self.metadata.keys()
        if update_key in keys:
            self.metadata.update({update_key:update_value})
        else:
            self.metadata.add({update_key:update_value})

    def game_state(self):
        """Main game loop that generates an instance of the game.
        
        Hardcoded values:
        username - Set to 'guest', multiple profiles in future implmentation.
        bet - Set to 10, number of chips to wager should be dynamic in future, different levels/tables i.e. high roller, bigger bets?
        finite - Used in while loops to prevent run away edgecases as per rule 2 in The Power of 10: Rules for Developing Safety-Critical Code.
        i - Iteration counter.
        """
        game = blackjack()
        bank_instance = bank()
        bank_instance.start_game()

        username = 'guest'

        chipcount = bank_instance.bank_df.loc[bank_instance.bank_df['username'] == username, 'blackjack chip count'][0]
        bet = 10
        
        os.system('cls' if os.name == 'nt' else 'clear')
        game.header_print()
        # print(len(self.deck))
        print('\n')
        print('Dealers Hand:\n')
        game.deal_hand('dealer', 2)
        game.metadata_update('dealer_hand',game.dealer_hand)
        dealer_hand_shown = copy.copy(game.dealer_hand)
        dealer_hand_shown[1] = "??"
        print(dealer_hand_shown)

        print('\n')
        
        print('Your Hand:\n')
        game.deal_hand('player', 2)
        game.metadata_update('player_hand',game.player_hand)
        print(game.player_hand)

        print('\n')

        print(f'Chip Count\n{chipcount}')
        print(f'Bet\n{bet}')

        hit = input("Hit? (y/n) ")
        finite = 5
        i = 0
        while hit == "y" and i < finite:
            # print('hit')
            i = i + 1
            game.deal_hand('player', 1)
            game.metadata_update('player_hand',game.player_hand)
            print(game.player_hand)
            hit = input("Hit? (y/n) ")
            
        if i >= finite:
            logger.info(f'Player max handsize reached')
            
        game.score_hand('player', game.player_hand)
        game.metadata_update('player_hand_score',game.player_hand_score)
        game.score_hand('dealer', game.dealer_hand)
        game.metadata_update('dealer_hand_score',game.dealer_hand_score)

        game.dealer_logic(dealer_score = game.dealer_hand_score, player_score =game.player_hand_score)
        game.metadata_update('dealer_hand',game.dealer_hand)
        game.metadata_update('dealer_hand_score',game.dealer_hand_score)

        # \033 is the escape character (ASCII code 27 in octal).
        # [2J clears the entire screen.
        # [H moves the cursor to the top-left corner.
        # print("\033[2J\033[H")
        os.system('cls' if os.name == 'nt' else 'clear')

        game.header_print()

        print('\n')
        print('Dealers Hand:\n')
        print(game.dealer_hand)
        print(game.dealer_hand_score)
        print('\n')
        
        print('Your Hand:\n')
        print(game.player_hand)
        print(game.player_hand_score)

        playerwins = False
        playerdraw = False
        if game.dealer_hand_score > 21 and game.player_hand_score <=21:
            print('Dealer Busts!')
            print('Player wins!')
            playerwins = True
        elif game.dealer_hand_score <= 21 and game.player_hand_score > 21:
            print('Player Busts!')
            print('Dealer wins!')
        elif game.dealer_hand_score > 21 and game.player_hand_score > 21:
            print('Double Bust!')
            print('Draw!')
            playerdraw = True
        elif game.dealer_hand_score > game.player_hand_score:
            print('Dealer wins!')
        elif game.dealer_hand_score < game.player_hand_score:
            print('Player wins!')
            playerwins = True
        elif game.dealer_hand_score == game.player_hand_score:
            print('Draw!')
            playerdraw = True

        if playerwins == True:
            chipcount = chipcount + bet
        elif playerdraw == True:
            pass
        else:
            chipcount = chipcount - bet


        bank_instance.updatechipcount(chipcount, username, game = 'blackjack', bank_df= bank_instance.bank_df)

        logger.info(game.metadata)

        play_again = input("Play another round? (y/n) ")

        if play_again == "y":
            try:
                blackjack().game_state()
            except Exception as e:
                print(f'Casino is closed due to: \n {type(e).__name__} \n we apologize for any inconvenience')
                logger.exception(e)
        else:
            print("See you around partner!")

    def deal_hand(self, actor, numcards):
        """Draws card from instance of game deck and inserts into actors hand, removing that card from being drawn in future."""
        for card in range(numcards):
            card_temp = random.choice(self.deck)
            index_temp = self.deck.index(card_temp)
            if index_temp in range(len(self.deck)):
                self.deck.remove(card_temp)
            else:
                print(card_temp)
                print(self.deck.index(card_temp))

            if actor == 'player':
                self.player_hand.append(card_temp)
            elif actor == 'dealer':
                self.dealer_hand.append(card_temp)
 
    def score_hand(self, actor, hand):
        """"Adds up value of cards in hand and adds value to named actor.
        Accounts of face cards having a value of 10.
        Accounts for Aces having a value of 11 or 1.
        """
        score = 0
        ace_in_hand = False
        for card in range(len(hand)):
            # print(card)
            rank = hand[card][0]
            if rank == "A":
                ace_in_hand = True
            # print(rank)

            if rank in self.card_rank_dict.keys():
                rank_value = self.card_rank_dict[rank]
                score = score + rank_value
            else:
                score = score + int(rank)
            # print(score)
        if score > 21 and ace_in_hand:
            score = score - 10

        if actor == 'player':
            self.player_hand_score =  self.player_hand_score + score
        elif actor == 'dealer':
            self.dealer_hand_score =  self.dealer_hand_score + score

    def dealer_logic(self, dealer_score, player_score):
        """Simple dealer AI to draw cards until conditions are met and returns hand.
        Has common a USA Las Vegas convention, hit at 15 no matter player hand value.

        Hardcoded values:
        finite - Used in while loops to prevent run away edgecases as per rule 2 in The Power of 10: Rules for Developing Safety-Critical Code.
        i - Iteration counter.
        """

        if player_score > 21:
            return
    

        if dealer_score == 15:
            logger.info(f'Dealer score 15')
            self.deal_hand('dealer', 1)
            self.dealer_hand_score = 0
            self.score_hand('dealer', self.dealer_hand)
            dealer_score = self.dealer_hand_score
            

        finite = 5
        i = 0
        while dealer_score < player_score and dealer_score <= 21 and i < finite:
            self.deal_hand('dealer', 1)
            self.dealer_hand_score = 0
            self.score_hand('dealer', self.dealer_hand)
            dealer_score = self.dealer_hand_score
            i = i + 1
        
        if i >= finite:
            logger.info(f'Dealer max handsize reached')

    def header_print(self):
        """Pretty header to display at top of screen."""
        print("*♣♣♣♣ ♦♦♦♦ ♥♥♥♥ ♠♠♠♠*")
        print("CardLineInterface: Blackjack")
        print("Dealer hits on 15")
        print("*♣♣♣♣ ♦♦♦♦ ♥♥♥♥ ♠♠♠♠*")

class poker:
    """Texas Holdem Poker"""
    def __init__(self):
        """Initalize empty containers and standard values based on the game mode."""
        self.player_hand = []
        # ['Nelly', 'Smith', 'Ocean']
        # self.nelly_hand = []
        # self.smith_hand = []
        # self.ocean_hand = []
        # self.dealer_hand = []
        # self.chip_count = []

        self.player_hand_score = 0
        # self.dealer_hand_score = 0

        self.card_rank_dict = {
            'A': 14,
            'K': 13,
            'Q': 12,
            'J': 11,
            'T': 10,
        }

        self.card_suite_dict = {
            '♣': 4,
            '♦': 3,
            '♥': 2,
            '♠': 1,
        }


        self.deck = ['A♣', '2♣', '3♣', '4♣', '5♣', '6♣', '7♣', '8♣', '9♣', 'T♣', 'J♣', 'Q♣', 'K♣', 'A♦', '2♦', '3♦', '4♦', '5♦', '6♦', '7♦', '8♦', '9♦', 'T♦', 'J♦', 'Q♦', 'K♦', 'A♥', '2♥', '3♥', '4♥', '5♥', '6♥', '7♥', '8♥', '9♥', 'T♥', 'J♥', 'Q♥', 'K♥', 'A♠', '2♠', '3♠', '4♠', '5♠', '6♠', '7♠', '8♠', '9♠', 'T♠', 'J♠', 'Q♠', 'K♠']

        self.metadata = {
            'player_hand':self.player_hand,
            'player_hand_score':self.player_hand_score,
        }

    def metadata_update(self, update_key, update_value):
        """"Utility function that updates key values for logging."""
        keys = self.metadata.keys()
        if update_key in keys:
            self.metadata.update({update_key:update_value})
        else:
            self.metadata.add({update_key:update_value})

    def game_state(self):
        """Main game loop that generates an instance of the game.
        
        Hardcoded values:
        username - Set to 'guest', multiple profiles in future implmentation.
        bet - Set to 10, number of chips to wager should be dynamic in future, different levels/tables i.e. high roller, bigger bets?
        finite - Used in while loops to prevent run away edgecases as per rule 2 in The Power of 10: Rules for Developing Safety-Critical Code.
        i - Iteration counter.
        """
        game = poker()
        bank_instance = bank()
        bank_instance.start_game()

        username = 'guest'

        chipcount = bank_instance.bank_df.loc[bank_instance.bank_df['username'] == username, 'poker chip count'][0]
        bet = 10

        handsize = 2
        
        os.system('cls' if os.name == 'nt' else 'clear')
        game.header_print()

        nelly = actor(name = 'Nelly')
        smith = actor(name = 'Smith')
        ocean = actor(name = 'Ocean')

        table = actor(name = 'Table')

        cpu_players = [nelly, smith, ocean]
        
        cpu_players_print_str = ''
        cpu_card_print_str = ''
        for cpu in cpu_players:
            game.deal_hand(hand = cpu.hand, numcards = handsize)
    

            cpu_players_print_str = cpu_players_print_str + cpu.name + '\t'
            cpu_card_print_str = cpu_card_print_str + "[?? ??]" + '\t'

        game.deal_hand(hand = game.player_hand, numcards = handsize)
        game.metadata_update('player_hand',game.player_hand)
        # flop
        game.deal_hand(hand = table.hand, numcards = 3)

        print(cpu_players_print_str)
        print(cpu_card_print_str)
        print('\n')
        print('Flop: ')
        print(table.hand)
        print('\n')
        print('Your Hand:')
        print(game.player_hand)

        proceed = input(f"Bet? ${bet} (y/n) ")

        if proceed == "y":
            game.deal_hand(hand = table.hand, numcards = 1)
            os.system('cls' if os.name == 'nt' else 'clear')
        else:
            1/0

        print(cpu_players_print_str)
        print(cpu_card_print_str)
        print('\n')
        print('Flop: ')
        print(table.hand)
        print('\n')
        print('Your Hand:')
        print(game.player_hand)

        proceed = input(f"Bet? ${bet} (y/n) ")

        if proceed == "y":
            game.deal_hand(hand = table.hand, numcards = 1)
            os.system('cls' if os.name == 'nt' else 'clear')
        else:
            1/0

        print(cpu_players_print_str)
        print(cpu_card_print_str)
        print('\n')
        print('Flop: ')
        print(table.hand)
        print('\n')
        print('Your Hand:')
        print(game.player_hand)

        bank_instance.updatechipcount(chipcount, username, game = 'poker', bank_df= bank_instance.bank_df)

        logger.info(game.metadata)

        play_again = input("Play another round? (y/n) ")

        if play_again == "y":
            try:
                poker().game_state()
            except Exception as e:
                print(f'Casino is closed due to: \n {type(e).__name__} \n we apologize for any inconvenience')
                logger.exception(e)
        else:
            print("See you around partner!")

    def deal_hand(self, numcards, hand, actor = None):
        """Draws card from instance of game deck and inserts into actors hand, removing that card from being drawn in future."""
        for card in range(numcards):
            card_temp = random.choice(self.deck)
            index_temp = self.deck.index(card_temp)
            if index_temp in range(len(self.deck)):
                self.deck.remove(card_temp)
            else:
                print(card_temp)
                print(self.deck.index(card_temp))

            hand.append(card_temp)

    def header_print(self):
        """Pretty header to display at top of screen."""
        print("*♣♣♣♣ ♦♦♦♦ ♥♥♥♥ ♠♠♠♠*")
        print("CardLineInterface: Texas Hold'em")
        print("*♣♣♣♣ ♦♦♦♦ ♥♥♥♥ ♠♠♠♠*'\n'")
        print('Still under construction!')

    def score_hand(self, hand, score):
        """"Adds up value of cards in hand and adds value to named actor.
        """
        score = 0
        rank_list = []
        suite_list = []

        for card in range(len(hand)):
            rank = hand[card][0]
            suite = hand[card][1]

            rank_list.append(rank)
            suite_list.append(suite)
        
        rank_list_unique = list(np.unique(rank_list))

        if len(rank_list) > len(rank_list_unique):
            pass

        club_count = suite_list.count('♣')
        diamond_count = suite_list.count('♦')
        heart_count = suite_list.count('♥')
        spade_count = suite_list.count('♠')

        suite_count = [club_count, diamond_count, heart_count, spade_count]

        if max(suite_count) >= 5:
            pass


if __name__ == "__main__":
    """Command line argument parser and logic to steer users to the right place."""
    parser = argparse.ArgumentParser(description="Select blackjack")


    parser.add_argument("-g", '--game', type=str, help="Game mode select")

    gamemodes = ['blackjack', 'poker']

    mode = None


    args = parser.parse_args()

    if args.game in gamemodes:
        mode = args.game
    elif args.game is None:
        print(f'Game options are {gamemodes}')
    else:
        fuzzfind = process.extract(args.game, choices= gamemodes, limit=1)
        game_maybe = fuzzfind[0][0]
        score_maybe = fuzzfind[0][1]
        if score_maybe > 84:
            print(f'Did you mean {game_maybe}?')
        else:
            print(f'Game options are {gamemodes}')

    today = str(date.today())
    logging.basicConfig(filename=f'{today}.log', level=logging.INFO)
    logger.info(f'Started {mode}')

    if mode == 'blackjack':
        try:
            blackjack().game_state()
        except Exception as e:
            print(f'Casino is closed due to: \n {type(e).__name__} \n we apologize for any inconvenience')
            logger.exception(e)

        

    elif mode == 'poker':
        # print("Under construction")
        try:
            poker().game_state()
        except Exception as e:
            print(f'Casino is closed due to: \n {type(e).__name__} \n we apologize for any inconvenience')
            logger.exception(e)





