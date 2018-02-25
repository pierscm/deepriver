from pypokerengine.players import BasePokerPlayer
from pypokerengine.api.game import setup_config, start_poker
import random
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate
import pandas as pd
from sqlalchemy import create_engine

class TightAggressive(BasePokerPlayer):  # Do not forget to make parent class as "BasePokerPlayer"

    def declare_action(self, valid_actions, hole_card, round_state):
        self.pot_size = round_state['pot']['main']['amount']
        community_card = round_state['community_card']
        win_rate = estimate_hole_card_win_rate(
                nb_simulation=1000,
                nb_player=self.nb_player,
                hole_card=gen_cards(hole_card),
                community_card=gen_cards(community_card)
                )
        if (win_rate >= 1.5 / self.nb_player) and (valid_actions[2]['amount']['max'] != -1):
            action = valid_actions[2]  # fetch raise action info
            bet = int(action['amount']['max']*0.75)
        elif (win_rate >= 1/self.nb_player):
        	action = valid_actions[1]
        	bet = int(action['amount'])
        else:
            action = valid_actions[0]  # fetch FOLD action info
            bet = action['amount']
        #print("Tight Aggressive: ", hole_card, "; Prob: ", win_rate)
        return action['action'], bet

    def receive_game_start_message(self, game_info):
        self.nb_player = game_info['player_num']

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass

def setup_ai():
    return TightAggressive()