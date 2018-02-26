from pypokerengine.players import BasePokerPlayer
from pypokerengine.api.game import setup_config, start_poker
import random
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate
import pandas as pd
import numpy as np
from scipy.stats import binom

NB_SIMULATION = 1000

# prob_dif_tracker = []
# prob_ratio_tracker = []


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

        # CHANGE!!!
        ex_win_rate = 1 / self.nb_player
        min_bet = valid_actions[2]['amount']['min']
        max_bet = valid_actions[2]['amount']['max']
        if win_rate / ex_win_rate >= 1.8:
            action = valid_actions[2]  # fetch raise action info
            try:
                bet = random.randrange(min_bet, max_bet)
            except:
                bet = -1
        elif win_rate / ex_win_rate > 1.18:
            action = valid_actions[1]  # fetch CALL action info
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

        # CHANGE!!!
        ex_win_rate = 1 / self.nb_player
        min_bet = valid_actions[2]['amount']['min']
        max_bet = valid_actions[2]['amount']['max']
        if win_rate / ex_win_rate >= 1.3:
            action = valid_actions[2]  # fetch raise action info
            try:
                bet = random.randrange(min_bet, max_bet)
            except:
                bet = -1
        elif win_rate / ex_win_rate > 1.18:
            action = valid_actions[1]  # fetch CALL action info
            bet = action['amount']
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


# TODO: Add action history

class LooseAggressive(BasePokerPlayer):
    def declare_action(self, valid_actions, hole_card, round_state):
        community_card = round_state['community_card']
        win_rate = estimate_hole_card_win_rate(
            nb_simulation=NB_SIMULATION,
            nb_player=self.nb_player,
            hole_card=gen_cards(hole_card),
            community_card=gen_cards(community_card)
        )

        # CHANGE!!!
        ex_win_rate = 1 / self.nb_player
        min_bet = valid_actions[2]['amount']['min']
        max_bet = valid_actions[2]['amount']['max']
        if win_rate / ex_win_rate >= 1.3:
            action = valid_actions[2]  # fetch raise action info
            try:
                bet = random.randrange(min_bet, max_bet)
            except:
                bet = -1
        elif win_rate / ex_win_rate > 1.0:
            action = valid_actions[1]  # fetch CALL action info
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

        # CHANGE!!!
        ex_win_rate = 1 / self.nb_player
        min_bet = valid_actions[2]['amount']['min']
        max_bet = valid_actions[2]['amount']['max']
        if win_rate / ex_win_rate >= 1.8:
            action = valid_actions[2]  # fetch raise action info
            try:
                bet = random.randrange(min_bet, max_bet)
            except:
                bet = -1
        elif win_rate / ex_win_rate > 1.0:
            action = valid_actions[1]  # fetch CALL action info
            bet = action['amount']
        else:
            action = valid_actions[0]  # fetch FOLD action info
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


opp_model = []


class our_bot(BasePokerPlayer):
    def __init__(self, aggressiveness_raise_prob_factor=1, frequency_call_factor=1, raise_percent=1, name='ourbot'):
        self.aggressiveness_raise_prob_factor = aggressiveness_raise_prob_factor
        self.frequency_call_factor = frequency_call_factor
        self.raise_percent = raise_percent
        self.name = name

    def mean_confidence_interval(data, confidence=0.95):
        a = 1.0 * np.array(data)
        n = len(a)
        m, se = np.mean(a), scipy.stats.sem(a)
        h = se * sp.stats.t._ppf((1 + confidence) / 2., n - 1)
        return m, m - h, m + h

    def model_dict(self, round_state, hole_card):  # CHANGE!!! Added 'hole_card'
        self.this_round_length = 0
        action_histories = round_state['action_histories']
        for x in self.opponent_model.keys():
            self.opponent_model[x]['fold_this_round'] = 0
            self.opponent_model[x]['raise_this_round'] = 0
            self.opponent_model[x]['call_this_round'] = 0
        for game_round in action_histories.keys():
            for x in range(len(action_histories[str(game_round)])):
                if len(action_histories[str(game_round)]) != 0:
                    self.this_round_length += 1

                    # CHANGE !!! Simple method for adding priors. Probably not the best option.
                    self.opponent_model[action_histories[str(game_round)][x]['uuid']]['fold'] = 2.16 # or 4.32 (or any multiple of 2.16)
                    self.opponent_model[action_histories[str(game_round)][x]['uuid']]['call'] = .42 # or .84 (or any multiple of .42)
                    self.opponent_model[action_histories[str(game_round)][x]['uuid']]['raise'] = .42 # or .84 (or any multiple of .42)
                if action_histories[str(game_round)][x]['action'] == 'FOLD':
                    self.opponent_model[action_histories[str(game_round)][x]['uuid']]['fold'] += 1
                    self.opponent_model[action_histories[str(game_round)][x]['uuid']]['fold_this_round'] += 1
                elif action_histories[str(game_round)][x]['action'] == 'CALL':
                    self.opponent_model[action_histories[str(game_round)][x]['uuid']]['call'] += 1
                    self.opponent_model[action_histories[str(game_round)][x]['uuid']]['call_this_round'] += 1
                elif action_histories[str(game_round)][x]['action'] == 'RAISE':
                    self.opponent_model[action_histories[str(game_round)][x]['uuid']]['raise'] += 1
                    self.opponent_model[action_histories[str(game_round)][x]['uuid']]['raise_this_round'] += 1
                    amt = action_histories[str(game_round)][x]['amount']
                    self.opponent_model[action_histories[str(game_round)][x]['uuid']]['raise_shares'] += (
                        amt / self.opponent_model[action_histories[str(game_round)][x]['uuid']]['stack'])
        output = {}
        probability_list = []
        output['probability_list'] = probability_list
        for x in self.opponent_model.keys():
            try:

                n = (self.opponent_model[x]['fold'] + self.opponent_model[x]['raise'] + self.opponent_model[x]['call'])
                fold_freq = self.opponent_model[x]['fold'] / (self.opponent_model[x]['fold'] + self.opponent_model[x]['raise'] + self.opponent_model[x]['call'])   # p_hat
                conf_int = binom.interval(.05, n, fold_freq)
                print(conf_int)

                self.opponent_model[x]['fold_freq'] = self.opponent_model[x]['fold'] / (self.opponent_model[x]['fold'] +        # CHANGE!!!
                                                                                        self.opponent_model[x]['raise'] +
                                                                                        self.opponent_model[x]['call'])
            except:
                self.opponent_model[x]['fold_freq'] = .72
            try:
                self.opponent_model[x]['raises:calls'] = self.opponent_model[x]['raise'] / self.opponent_model[x]['call']
            except:
                self.opponent_model[x]['raises:calls'] = 1
            community_card = round_state['community_card']
            win_rate = estimate_hole_card_win_rate(
                nb_simulation=NB_SIMULATION,
                nb_player=self.nb_player,
                hole_card=gen_cards(hole_card),
                community_card=gen_cards(community_card)
            )
            self.opponent_model[x]['probability'] = (1 - win_rate) / self.nb_player

            if self.opponent_model[x]['raise_this_round'] > 0:
                self.opponent_model[x]['probability'] += (1 - self.opponent_model[x][
                    'aggressiveness'] * self.aggressiveness_raise_prob_factor) * self.opponent_model[x]['probability']
            if self.opponent_model[x]['call_this_round'] > 0:
                self.opponent_model[x]['probability'] += ((1 - self.opponent_model[x]['frequency']) * \
                                                          self.opponent_model[x][
                                                              'probability']) * self.frequency_call_factor
            if self.opponent_model[x]['fold_this_round'] > 0:
                self.opponent_model[x]['probability'] = 0

            # I'm skeptical that opponent model dictionary is tracking properly. I think it only tracks while we're playing a hand.
            # print(self.opponent_model[x])
            if self.opponent_model[x]['name'] != self.name:
                output['probability_list'].append(self.opponent_model[x]['probability'])
            else:
                output['stack'] = self.opponent_model[x]['stack']
        return (output)

    def declare_action(self, valid_actions, hole_card, round_state):
        output = self.model_dict(round_state, hole_card)
        prob_list = output['probability_list']
        stack = output['stack']  # how to access this?
        max_of_list = max(prob_list)
        print('Our Bot Estimated max_prob', max_of_list)
        community_card = round_state['community_card']
        win_rate = estimate_hole_card_win_rate(
            nb_simulation=NB_SIMULATION,
            nb_player=self.nb_player,
            hole_card=gen_cards(hole_card),
            community_card=gen_cards(community_card)
        )
        if win_rate >= max_of_list:
            action = valid_actions[2]  # fetch raise action info
            bet = stack * ((random.randint(40, 60) / 100) * self.raise_percent)
        elif win_rate >= (max_of_list * 0.75):
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
        if round_count == 1:
            self.opponent_model = {}
            for x in range(len(seats)):
                self.opponent_model[seats[x]['uuid']] = {}
                self.opponent_model[seats[x]['uuid']]['name'] = seats[x]['name']
                self.opponent_model[seats[x]['uuid']]['fold'] = 0
                self.opponent_model[seats[x]['uuid']]['call'] = 0
                self.opponent_model[seats[x]['uuid']]['raise'] = 0
                self.opponent_model[seats[x]['uuid']]['fold_this_round'] = 0
                self.opponent_model[seats[x]['uuid']]['call_this_round'] = 0
                self.opponent_model[seats[x]['uuid']]['raise_this_round'] = 0
                self.opponent_model[seats[x]['uuid']]['total'] = 0
                self.opponent_model[seats[x]['uuid']]['raise_shares'] = 0
                self.opponent_model[seats[x]['uuid']]['frequency'] = 0.5
                self.opponent_model[seats[x]['uuid']]['aggressiveness'] = 0
        for x in range(len(seats)):
            self.opponent_model[seats[x]['uuid']]['stack'] = seats[x]['stack']
        opp_model.append(self.opponent_model)

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass


config = setup_config(max_round=50, initial_stack=50000, small_blind_amount=20)
config.register_player(name="TightConservative", algorithm=TightConservative())
config.register_player(name="LooseAgggressive", algorithm=LooseAggressive())
config.register_player(name="TightAggressive", algorithm=TightAggressive())
config.register_player(name="LooseConservative", algorithm=LooseConservative())
config.register_player(name="ourbot", algorithm=our_bot())
game_result = start_poker(config, verbose=1)

# prob_d = np.array(prob_dif_tracker)
# prob_r = np.array(prob_ratio_tracker)
#
# print("Prob Dif Mean: ", prob_d.mean(), "; Prob Dif StD: ", prob_d.std())
# print("Prob Rat Mean: ", prob_r.mean(), "; Prob Rat StD: ", prob_r.std())
