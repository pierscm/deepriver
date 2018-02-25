from pypokerengine.players import BasePokerPlayer
from pypokerengine.api.game import setup_config, start_poker
import random
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate
import pandas as pd
from sqlalchemy import create_engine


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
        if (win_rate >= 2.0 / (self.nb_player)) and (valid_actions[2]['amount']['max'] != -1):
            action = valid_actions[2]  # fetch CALL action info
            bet = action['amount']
            bet = random.uniform(action['amount']['min'], action['amount']['max'])
        elif win_rate >= 1.7 / (self.nb_player):
        	action = valid_actions[1]  # fetch CALL action info
        	bet = action['amount']
        else:
            action = valid_actions[0]  # fetch FOLD action info
            bet = action['amount']
        #print("Tight Conservative: ", hole_card, "; Prob: ", win_rate)
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
        if (win_rate >= 1.5 / self.nb_player) and (valid_actions[2]['amount']['max'] != -1):
            action = valid_actions[2]  # fetch raise action info
            bet = action['amount']['max']*0.75
        elif (win_rate >= 1/self.nb_player):
        	action = valid_actions[1]
        	bet = action['amount']
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
        if (win_rate >= 1.0 / self.nb_player) and (valid_actions[2]['amount']['max'] != -1):
            action = valid_actions[2]  # fetch raise action info
            bet = action['amount']['max']*0.75
        elif win_rate >= 1.0/ (self.nb_player*2):
            action = valid_actions[1]  # fetch CALL action info
            bet = action['amount']
        else:
            action = valid_actions[0]  # fetch FOLD action info
            bet = action['amount']
        #print("Loose Aggressive: ", hole_card, "; Prob: ", win_rate)
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
        if (win_rate >= 1.0 / self.nb_player) and (valid_actions[2]['amount']['max'] != -1):
            action = valid_actions[2]  # fetch raise action info
            bet = action['amount']['min']*1.25
        elif win_rate >= 1.0/ (self.nb_player*2):
            action = valid_actions[1]  # fetch FOLD action info
            bet = action['amount']
        else:
            action = valid_actions[1]  # fetch Call action info
            bet = action['amount']
        #print("Loose Conservative: ", hole_card, "; Prob: ", win_rate)
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

    def __init__(self, aggressiveness_raise_prob_factor=1, frequency_call_factor=1, raise_percent=1, raise_prob=1, name='ourbot'):
        self.aggressiveness_raise_prob_factor = aggressiveness_raise_prob_factor
        self.frequency_call_factor = frequency_call_factor
        self.raise_percent = raise_percent
        self.raise_prob = raise_prob
        #self.call_prob = call_prob
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
        output = {}
        probability_list = []
        output['probability_list'] = probability_list
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
                output['probability_list'].append(self.opponent_model[x]['probability'])
            else:
                output['stack'] = self.opponent_model[x]['stack']
        return(output)

    def declare_action(self, valid_actions, hole_card, round_state):
        output = self.model_dict(round_state)
        prob_list = output['probability_list']
        stack = output['stack'] #how to access this?
        max_of_list = max(prob_list)
        #print('Our Bot Estimated max_prob', max_of_list)
        community_card = round_state['community_card']
        win_rate = estimate_hole_card_win_rate(
                nb_simulation=NB_SIMULATION,
                nb_player=self.nb_player,
                hole_card=gen_cards(hole_card),
                community_card=gen_cards(community_card)
                )


        # Make sure bot is able to raise by valid amount, then select within range
        if (win_rate >= max_of_list*self.raise_prob) and (valid_actions[2]['amount']['max'] != -1):
            action = valid_actions[2]  # fetch raise action info
            bet = random.uniform(action['amount']['min'], action['amount']['min'] * (action['amount']['min'] * self.raise_percent))
            if bet > action['amount']['max']:
            	bet = action['amount']['max']
        elif (win_rate >= (max_of_list*0.8)) and (stack >= valid_actions[1]['amount']):
            action = valid_actions[1]  # fetch call action info
            bet = action['amount']
        else:
            action = valid_actions[0]  # fetch FOLD action info
            bet = action['amount']
        print(self.opponent_model)
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
        opp_model.append(self.opponent_model)

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass


sql_engine = create_engine('sqlite:///playerdata.db', echo=False)
connection = sql_engine.raw_connection()


total_stack = 10000*8
world_results = []
for world in range(3):
    GameNumber = 0
    print("W BEGIN")
    config = setup_config(max_round=20, initial_stack=10000, small_blind_amount=20)
    config.register_player(name="TightConservative", algorithm=TightConservative())
    config.register_player(name="LooseAgggressive", algorithm=LooseAggressive())
    config.register_player(name="TightAggressive", algorithm=TightAggressive())
    config.register_player(name="LooseConservative", algorithm=LooseConservative())

    agg = [(random.randint(5,300)/100), (random.randint(5,300)/100), (random.randint(5,300)/100), (random.randint(5,300)/100)]
    freq = [(random.randint(5,300)/100), (random.randint(5,300)/100), (random.randint(5,300)/100), (random.randint(5,300)/100)]
    rand_raise = [(random.randint(5,300)/100), (random.randint(5,300)/100), (random.randint(5,300)/100), (random.randint(5,300)/100)]
    raise_prob = [(random.randint(80,150)/100),(random.randint(80,150)/100),(random.randint(80,150)/100),(random.randint(80,150)/100)]
    #call_prob = [(random.randint(5,80)/100),(random.randint(5,80)/100),(random.randint(5,80)/100),(random.randint(5,80)/100), ]


    config.register_player(name="ourbot1", algorithm=our_bot(aggressiveness_raise_prob_factor=agg[0], frequency_call_factor=freq[0], raise_percent=rand_raise[0], raise_prob=raise_prob[0], name="ourbot1"))
    config.register_player(name="ourbot2", algorithm=our_bot(aggressiveness_raise_prob_factor=agg[1], frequency_call_factor=freq[1], raise_percent=rand_raise[1], raise_prob=raise_prob[1], name="ourbot2"))
    config.register_player(name="ourbot3", algorithm=our_bot(aggressiveness_raise_prob_factor=agg[2], frequency_call_factor=freq[2], raise_percent=rand_raise[2], raise_prob=raise_prob[2], name="ourbot3"))
    config.register_player(name="ourbot4", algorithm=our_bot(aggressiveness_raise_prob_factor=agg[3], frequency_call_factor=freq[3], raise_percent=rand_raise[3], raise_prob=raise_prob[3], name="ourbot4"))
    game_resulta = start_poker(config, verbose=1)
    game_resulta = pd.DataFrame.from_dict(game_resulta['players'])
    game_resulta['aggressiveness_raise_prob_factor'] = pd.Series([0,0,0,0,agg[0],agg[1],agg[2],agg[3]])
    game_resulta['frequency_call_factor'] = pd.Series([0,0,0,0,freq[0],freq[1],freq[2],freq[3]])
    game_resulta['raise_percent'] = pd.Series([0,0,0,0,rand_raise[0],rand_raise[1],rand_raise[2],rand_raise[3]])
    game_resulta['raise_prob'] = pd.Series([0, 0, 0, 0, raise_prob[0],raise_prob[1],raise_prob[2],raise_prob[3]] )
    #game_resulta['call_prob'] = pd.Series([0, 0, 0, 0, call_prob[0],call_prob[1],call_prob[2],call_prob[3]])

    our_bot_stack_total = game_resulta.ix[4:7]['stack'].sum()
    game_resulta['win_factor'] = game_resulta['stack']/our_bot_stack_total
    game_resulta['aggressiveness_raise_prob_factor'] = game_resulta['aggressiveness_raise_prob_factor'] * game_resulta['win_factor']
    game_resulta['frequency_call_factor'] = game_resulta['frequency_call_factor'] * game_resulta['win_factor']
    game_resulta['raise_percent'] = game_resulta['raise_percent'] * game_resulta['win_factor']
    game_resulta['raise_prob'] = game_resulta['raise_prob'] * game_resulta['win_factor']
    #game_resulta['call_prob'] = game_resulta['call_prob'] * game_resulta['win_factor']
    game_resulta['game'] = GameNumber
    print(game_resulta)

    try:
        game_result = game_result.append(game_resulta)
    except:
        game_result = game_resulta


    agg_factor = {}
    freq_factor = {}
    raise_percent = {}
    #call_prob = {}
    raise_prob = {}

    for evolution in range(15):
        GameNumber+=1

        print("BEGINNING EVOLUTION")
        try:
            agg_factor[1] =  game_resultb['aggressiveness_raise_prob_factor'].sum()
            freq_factor[1] = game_resultb['frequency_call_factor'].sum()
            raise_percent[1] = game_resultb['raise_percent'].sum()
            raise_prob[1] = game_resultb['raise_prob'].sum()
            #call_prob[1] = game_resultb['call_prob'].sum()
        except:
            agg_factor[1] =  game_resulta['aggressiveness_raise_prob_factor'].sum()
            freq_factor[1] = game_resulta['frequency_call_factor'].sum()
            raise_percent[1] = game_resulta['raise_percent'].sum()
            raise_prob[1] = game_resulta['raise_prob'].sum()
            #call_prob[1] = game_resulta['call_prob'].sum()
        if agg_factor[1] is None:
            agg_factor[1] = 0.1
            freq_factor[1] = 0.1
            raise_percent[1] = 0.1
            raise_prob[1] = 1
            #call_prob[1] = 0.8
        for i in range(2,5):
            agg_factor[i] = agg_factor[1] * (random.randint(75,125)/100)
            freq_factor[i] = freq_factor[1] * (random.randint(75,125) / 100)
            raise_percent[i] = raise_percent[1] * (random.randint(75,125) / 100)
            raise_prob[i] = freq_factor[1] * (random.randint(75,125) / 100)
            #call_prob[i] = raise_percent[1] * (random.randint(75,125) / 100)
        config = setup_config(max_round=20, initial_stack=10000, small_blind_amount=20)
        config.register_player(name="TightConservative", algorithm=TightConservative())
        config.register_player(name="LooseAgggressive", algorithm=LooseAggressive())
        config.register_player(name="TightAggressive", algorithm=TightAggressive())
        config.register_player(name="LooseConservative", algorithm=LooseConservative())

        config.register_player(name="ourbot1",
                               algorithm=our_bot(aggressiveness_raise_prob_factor=agg_factor[1], frequency_call_factor=freq_factor[1],
                                                 raise_percent=raise_percent[1], raise_prob=raise_prob[1],
                                                 name="ourbot1"))
        config.register_player(name="ourbot2",
                               algorithm=our_bot(aggressiveness_raise_prob_factor=agg_factor[2], frequency_call_factor=freq_factor[2],
                                                 raise_percent=raise_percent[2], raise_prob=raise_prob[2],
                                                 name="ourbot2"))
        config.register_player(name="ourbot3",
                               algorithm=our_bot(aggressiveness_raise_prob_factor=agg_factor[3], frequency_call_factor=freq_factor[3],
                                                 raise_percent=raise_percent[3], raise_prob=raise_prob[3],
                                                 name="ourbot3"))
        config.register_player(name="ourbot4",
                               algorithm=our_bot(aggressiveness_raise_prob_factor=agg_factor[4], frequency_call_factor=freq_factor[4],
                                                 raise_percent=raise_percent[4], raise_prob=raise_prob[4],
                                                 name="ourbot4"))
        game_resultb = start_poker(config, verbose=1)
        game_resultb = pd.DataFrame.from_dict(game_resultb['players'])
        game_resultb['aggressiveness_raise_prob_factor'] = pd.Series([0, 0, 0, 0, agg_factor[1], agg_factor[2], agg_factor[3], agg_factor[4]])
        game_resultb['frequency_call_factor'] = pd.Series([0, 0, 0, 0, freq_factor[1], freq_factor[2], freq_factor[3], freq_factor[4]])
        game_resultb['raise_percent'] = pd.Series(
            [0, 0, 0, 0, raise_percent[1], raise_percent[2], raise_percent[3], raise_percent[4]])
        game_resultb['raise_prob'] = pd.Series([0, 0, 0, 0, raise_prob[1], raise_prob[2], raise_prob[3], raise_prob[4]])
        #game_resultb['call_prob'] = pd.Series([0, 0, 0, 0, call_prob[1], call_prob[2], call_prob[3], call_prob[4] ])
        print(game_resultb)
        our_bot_stack_total = game_resultb.ix[4:7]['stack'].sum()
        game_resultb['win_factor'] = game_resultb['stack'] / our_bot_stack_total
        game_resultb['aggressiveness_raise_prob_factor'] = game_resultb['aggressiveness_raise_prob_factor'] * game_resultb['win_factor']
        game_resultb['frequency_call_factor'] = game_resultb['frequency_call_factor'] * game_resultb['win_factor']
        game_resultb['raise_percent'] = game_resultb['raise_percent'] * game_resultb['win_factor']
        game_resultb['raise_prob'] = game_resultb['raise_prob'] * game_resultb['win_factor']
        #game_resultb['call_prob'] = game_resultb['call_prob'] * game_resultb['win_factor']
        game_resultb['game'] = GameNumber
        print("finished game.")
        game_result = game_result.append(game_resultb)
        #game_result.to_sql('data', connection,index=False, if_exists='replace')

    world_results.append(game_result)
    #import getplayerstats





