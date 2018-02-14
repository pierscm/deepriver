from pypokerengine.players import BasePokerPlayer
from pypokerengine.api.game import setup_config, start_poker
import random
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate

NB_SIMULATION=1000
class TightConservative(BasePokerPlayer):  # Do not forget to make parent class as "BasePokerPlayer"

    def declare_action(self, valid_actions, hole_card, round_state):
        self.pot_size = round_state['pot']['main']['amount']
        community_card = round_state['community_card']
        win_rate = estimate_hole_card_win_rate(
                nb_simulation=NB_SIMULATION,
                nb_player=self.nb_player,
                hole_card=gen_cards(hole_card),
                community_card=gen_cards(community_card)
                )
        if win_rate >= 2.0 / (self.nb_player):
            action = valid_actions[1]  # fetch raise action info
            bet = action['amount']
        else:
            action = valid_actions[0]  # fetch FOLD action info
            bet = action['amount']
        print("Tight Conservative: ", hole_card, "; Prob: ", win_rate)
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


class TightAggressive(BasePokerPlayer):  # Do not forget to make parent class as "BasePokerPlayer"

    def declare_action(self, valid_actions, hole_card, round_state):
        self.pot_size = round_state['pot']['main']['amount']
        community_card = round_state['community_card']
        win_rate = estimate_hole_card_win_rate(
                nb_simulation=NB_SIMULATION,
                nb_player=self.nb_player,
                hole_card=gen_cards(hole_card),
                community_card=gen_cards(community_card)
                )
        if win_rate >= 1.5 / self.nb_player:
            action = valid_actions[2]  # fetch raise action info
            bet = action['amount']['max']*0.75
        else:
            action = valid_actions[0]  # fetch FOLD action info
            bet = action['amount']
        print("Tight Aggressive: ", hole_card, "; Prob: ", win_rate)
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




#TODO: Add action history

class LooseAggressive(BasePokerPlayer):

    def declare_action(self, valid_actions, hole_card, round_state):
        community_card = round_state['community_card']
        win_rate = estimate_hole_card_win_rate(
                nb_simulation=NB_SIMULATION,
                nb_player=self.nb_player,
                hole_card=gen_cards(hole_card),
                community_card=gen_cards(community_card)
                )
        if win_rate >= 1.0 / self.nb_player:
            action = valid_actions[2]  # fetch raise action info
            bet = action['amount']['max']*0.75
        elif win_rate >= 1.0/ (self.nb_player*2):
            action = valid_actions[1]  # fetch FOLD action info
            bet = action['amount']
        else:
            action = valid_actions[0]  # fetch FOLD action info
            bet = action['amount']
        print("Loose Aggressive: ", hole_card, "; Prob: ", win_rate)
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

class LooseConservative(BasePokerPlayer):

    def declare_action(self, valid_actions, hole_card, round_state):
        community_card = round_state['community_card']
        win_rate = estimate_hole_card_win_rate(
                nb_simulation=NB_SIMULATION,
                nb_player=self.nb_player,
                hole_card=gen_cards(hole_card),
                community_card=gen_cards(community_card)
                )
        if win_rate >= 1.0 / self.nb_player:
            action = valid_actions[2]  # fetch raise action info
            bet = action['amount']['min']*1.25
        elif win_rate >= 1.0/ (self.nb_player*2):
            action = valid_actions[1]  # fetch FOLD action info
            bet = action['amount']
        else:
            action = valid_actions[1]  # fetch Call action info
            bet = action['amount']
        print("Loose Conservative: ", hole_card, "; Prob: ", win_rate)
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



class our_bot(BasePokerPlayer):

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

        self.probability_list = []
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

            self.varA = 1
            self.varB = 0.1
            if self.opponent_model[x]['raise_this_round']>0:
                self.opponent_model[x]['probability'] += (1-self.opponent_model[x]['aggressiveness']*self.varA)*self.opponent_model[x]['probability']
            if self.opponent_model[x]['call_this_round']>0:
                self.opponent_model[x]['probability'] += ((1 - self.opponent_model[x]['frequency'] * self.varA) * \
                                                         self.opponent_model[x]['probability'])*self.varB
            if self.opponent_model[x]['fold_this_round']>0:
                self.opponent_model[x]['probability']=0
            print(self.opponent_model[x])
            if self.opponent_model[x]['name'] != 'oubot':
                self.probability_list.append(self.opponent_model[x]['probability'])
        return(self.probability_list)

    def declare_action(self, valid_actions, hole_card, round_state):
        prob_list = self.model_dict(round_state)
        max_of_list = max(prob_list)
        print('max_prob', max_of_list)
        community_card = round_state['community_card']

        win_rate = estimate_hole_card_win_rate(
                nb_simulation=NB_SIMULATION,
                nb_player=self.nb_player,
                hole_card=gen_cards(hole_card),
                community_card=gen_cards(community_card)
                )
        if win_rate >= max_of_list:
            action = valid_actions[2]  # fetch raise action info
            bet = action['amount']['max']*(random.randint(40,60)/100)
        elif win_rate >= (max_of_list*0.75):
            action = valid_actions[1]  # fetch call action info
            bet = action['amount']
        else:
            action = valid_actions[0]  # fetch FOLD action info
            bet = action['amount']
        print("Our Bot: ", hole_card, "; Prob: ", win_rate)
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
    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass






config = setup_config(max_round=20, initial_stack=10000, small_blind_amount=20)
config.register_player(name="TightConservative", algorithm=TightConservative())
config.register_player(name="LooseAgggressive", algorithm=LooseAggressive())
config.register_player(name="TightAggressive", algorithm=TightAggressive())
config.register_player(name="LooseConservative", algorithm=LooseConservative())
config.register_player(name="ourbot", algorithm=our_bot())
game_result = start_poker(config, verbose=1)

