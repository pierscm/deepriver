from pypokerengine.players import BasePokerPlayer
from pypokerengine.api.game import setup_config, start_poker
import random
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate
import pandas as pd
from sqlalchemy import create_engine

opp_model = []


class our_bot(BasePokerPlayer):

    def __init__(self, aggressiveness_raise_prob_factor=1, frequency_call_factor=1, raise_percent=1, raise_prob=1, call_prob=1, name='ourbot'):
        self.aggressiveness_raise_prob_factor = aggressiveness_raise_prob_factor
        self.frequency_call_factor = frequency_call_factor
        self.raise_percent = raise_percent
        self.raise_prob = raise_prob
        self.call_prob = call_prob
        self.output = {}

        self.name = name

    def model_dict(self, round_state):
        self.this_round_length = 0
        action_histories = round_state['action_histories']
        for x in self.opponent_model.keys():
            self.opponent_model[x]['fold_this_round'] = 0
            self.opponent_model[x]['raise_this_round'] = 0
            self.opponent_model[x]['call_this_round'] = 0
        for game_round in action_histories.keys():
            for x in range(len(action_histories[str(game_round)])):
                if len(action_histories[str(game_round)]) != 0:
                    self.this_round_length +=1
                if action_histories[str(game_round)][x]['action']=='FOLD':
                    self.opponent_model[action_histories[str(game_round)][x]['uuid']]['fold'] +=1
                    self.opponent_model[action_histories[str(game_round)][x]['uuid']]['fold_this_round'] += 1
                elif action_histories[str(game_round)][x]['action']=='CALL':
                    self.opponent_model[action_histories[str(game_round)][x]['uuid']]['call'] +=1
                    self.opponent_model[action_histories[str(game_round)][x]['uuid']]['call_this_round'] += 1
                elif action_histories[str(game_round)][x]['action']=='RAISE':
                    self.opponent_model[action_histories[str(game_round)][x]['uuid']]['raise'] += 1
                    self.opponent_model[action_histories[str(game_round)][x]['uuid']]['raise_this_round'] += 1
                    amt = action_histories[str(game_round)][x]['amount']
                    self.opponent_model[action_histories[str(game_round)][x]['uuid']]['raise_shares'] += (amt/self.opponent_model[action_histories[str(game_round)][x]['uuid']]['stack'])
        probability_list = []
        self.output['probability_list'] = probability_list
        for x in self.opponent_model.keys():
            try:
                self.opponent_model[x]['frequency'] = (self.opponent_model[x]['call']+self.opponent_model[x]['raise'])/(self.opponent_model[x]['fold']+self.opponent_model[x]['raise']+self.opponent_model[x]['call'])
            except:
                self.opponent_model[x]['frequency'] = 0
            try:
                self.opponent_model[x]['aggressiveness'] = self.opponent_model[x]['raise_shares']/(self.opponent_model[x]['raise'])
            except:
                self.opponent_model[x]['frequency'] = 0
            self.opponent_model[x]['probability']=1/self.nb_player
            #THIS IS WAY TO SIMPLE!
            if self.opponent_model[x]['raise_this_round']>0:
                self.opponent_model[x]['probability'] += (1-self.opponent_model[x]['aggressiveness']*self.aggressiveness_raise_prob_factor)\
                                                         *self.opponent_model[x]['probability']
            if self.opponent_model[x]['call_this_round']>0:
                self.opponent_model[x]['probability'] += ((1 - self.opponent_model[x]['frequency']) * \
                                                         self.opponent_model[x]['probability'])*self.frequency_call_factor
            if self.opponent_model[x]['fold_this_round']>0:
                self.opponent_model[x]['probability']=0
            #print(self.opponent_model[x])
            if self.opponent_model[x]['name'] != self.name:
                self.output['probability_list'].append(self.opponent_model[x]['probability'])
            else:
                self.output['stack'] = self.opponent_model[x]['stack']
        return(self.output)

    def declare_action(self, valid_actions, hole_card, round_state):
        output = self.model_dict(round_state)
        prob_list = self.output['probability_list']
        stack = self.output['stack'] #how to access this?
        max_of_list = max(prob_list)
        #print('Our Bot Estimated max_prob', max_of_list)
        community_card = round_state['community_card']
        win_rate = estimate_hole_card_win_rate(
                nb_simulation=1000,
                nb_player=self.nb_player,
                hole_card=gen_cards(hole_card),
                community_card=gen_cards(community_card)
                )
        # Make sure bot is able to raise by valid amount, then select within range
        if (win_rate >= max_of_list*self.raise_prob) and (valid_actions[2]['amount']['max'] != -1):
            action = valid_actions[2]  # fetch raise action info
            bet = random.uniform(action['amount']['min'], action['amount']['min'] * (action['amount']['min'] * self.raise_percent))
            if bet > action['amount']['max']:
            	bet = int(action['amount']['max'])
        elif (win_rate >= (max_of_list*self.call_prob)) and (stack >= valid_actions[1]['amount']):
            action = valid_actions[1]  # fetch call action info
            bet = int(action['amount'])
        else:
            action = valid_actions[0]  # fetch FOLD action info
            bet = int(action['amount'])
        #print("Our Bot: ", hole_card, "; Prob: ", win_rate)
        return action['action'], bet

    def receive_game_start_message(self, game_info):
        self.nb_player = game_info['player_num']

    def receive_round_start_message(self, round_count, hole_card, seats):
        if round_count==1:
            self.opponent_model = {}
            for x in range(len(seats)):
                self.opponent_model[seats[x]['uuid']] = {}
                self.opponent_model[seats[x]['uuid']]['name'] = seats[x]['name']
                self.opponent_model[seats[x]['uuid']]['fold']=0
                self.opponent_model[seats[x]['uuid']]['call'] = 0
                self.opponent_model[seats[x]['uuid']]['raise'] = 0
                self.opponent_model[seats[x]['uuid']]['fold_this_round']=0
                self.opponent_model[seats[x]['uuid']]['call_this_round'] = 0
                self.opponent_model[seats[x]['uuid']]['raise_this_round'] = 0
                self.opponent_model[seats[x]['uuid']]['total'] = 0
                self.opponent_model[seats[x]['uuid']]['raise_shares'] = 0
                self.opponent_model[seats[x]['uuid']]['frequency'] = 0.5
                self.opponent_model[seats[x]['uuid']]['aggressiveness'] = 0
        for x in range(len(seats)):
            self.opponent_model[seats[x]['uuid']]['stack'] = seats[x]['stack']
            self.output['stack'] = seats[x]['stack']
        opp_model.append(self.opponent_model)
    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass

    def update_opponent_model(self, opponent_model):
        global opponent_model_global
        opponent_model_global = opponent_model

def setup_ai():
    return our_bot(aggressiveness_raise_prob_factor=4.9, frequency_call_factor=0.34,
                   raise_percent=4.95, raise_prob=0.335, call_prob=5.9174 ,name="Our_Bot")