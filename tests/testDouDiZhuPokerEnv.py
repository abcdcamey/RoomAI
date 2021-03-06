#!/bin/python
#coding:utf-8
import sys
import unittest
import copy
from roomai.doudizhupoker   import *


class DouDiZhuPokerEnvTester(unittest.TestCase):
    """
    """
    def testSmokeTest(self):
        '''
        
        :return: 
        '''
        env = DouDiZhuPokerEnv()
        infos, public_state, person_states, private_state = env.init()
        while public_state.is_terminal == False:
            available_actions = list(infos[public_state.turn].person_state.available_actions.values())
            action = available_actions[int(random.random() * len(available_actions))]
            env.forward(action)


        env = DouDiZhuPokerEnv()
        infos, public_state, person_states, private_state  = env.init()
        num_card = private_state.__unused_cards__.num_cards
        for i in range(17 * 3):
            available_actions = list(infos[public_state.turn].person_state.available_actions.values())
            action = available_actions[int(random.random() * len(available_actions))]
            print(action.key)
            env.forward(action)
        env = env
        self.assertTrue((env.public_state.turn in [0,1,2]))
        x = 0



    def testFoward(self):
        """

        """
        env = DouDiZhuPokerEnv()
        p = [0,0,0]
        infos,public_state, person_states, private_state = env.init({"param_start_turn":0})

        while isinstance(list(person_states[public_state.turn].available_actions.values())[0],DouDiZhuPokerActionChance) == True:
            env.forward(list(person_states[public_state.turn].available_actions.values())[0])


        ### init
        for i in range(3):
            env.person_states[i].__hand_cards__ = DouDiZhuPokerHandCards.lookup("")
            for j in range(4*i,4*(i+1)):
                for count in range(4):
                    env.person_states[i].__hand_cards__ = env.person_states[i].hand_cards.add_cards(DouDiZhuPokerUtil.rank_to_str[j])
            env.person_states[i].__hand_cards__ = env.person_states[i].hand_cards.add_cards(DouDiZhuPokerUtil.rank_to_str[12])
        env.private_state.__unused_cards__ = DouDiZhuPokerHandCards.lookup("")
        env.private_state.__unused_cards__  = env.private_state.__unused_cards__.add_cards("".join([DouDiZhuPokerUtil.rank_to_str[12], DouDiZhuPokerUtil.rank_to_str[13], DouDiZhuPokerUtil.rank_to_str[14]]))



        print ("_______________________________________________________________")
        #print (env.private_state.__unused_cards__.key)
        print (env.person_states[0].hand_cards.key)
        print (env.person_states[0].hand_cards.num_cards)
        print (env.person_states[1].hand_cards.key)
        print (env.person_states[2].hand_cards.key)
        env.public_state.__turn__ = 0
        
        # landlord 0:4,1:4,2:4,3:4      12:1 
        # peasant1 4:4,5:4,6:4,7:4      12:1
        # peasant2 8:4,9:4,10:4,11:4    12:1
        # remaining 12:1 13:1 14:1

        action = DouDiZhuPokerAction([13], [])
        self.assertFalse(env.is_action_valid(action, env.public_state,env.person_states[env.public_state.turn]))

        action = DouDiZhuPokerAction([1, 2, 3, 4, 5], [12, 2, 3])
        self.assertFalse(env.is_action_valid(action, env.public_state,env.person_states[env.public_state.turn]))

        ##0 turn = 0
        action = DouDiZhuPokerAction([DouDiZhuPokerUtil.str_to_rank["b"]], [])
        infos, public_state, person_states, private_state = env.forward(action)

        ##1 turn = 1
        action = DouDiZhuPokerAction([DouDiZhuPokerUtil.str_to_rank["b"]], [])
        infos, public_state, person_states, private_state = env.forward(action)
        
        ##2 turn = 2
        self.assertEqual(env.public_state.turn,2)
        action = DouDiZhuPokerAction([DouDiZhuPokerUtil.str_to_rank["b"]], [])
        infos, public_state, person_states, private_state = env.forward(action)
        self.assertEqual(public_state.landlord_id,2)
        self.assertEqual(public_state.phase, 1)
        # peasant   0:4, 1:4, 2:4,  3:4  12:1 
        # peasant   4:4, 5:4, 6:4,  7:4  12:1
        # landlord  8:4, 9:4, 10:4, 11:4 12:2 13:1 14:1     
      
        #landlord = 2 
        #########################play phase#################
        ##3 turn = 2 license_id = 2
        self.assertEqual(env.public_state.turn,2)
        self.assertEqual(env.public_state.license_playerid,2)
        action = DouDiZhuPokerAction([8], [])
        infos, public_state, person_states, private_state = env.forward(action) ######################################################### 8
        # landlord 4:4, 1:4, 2:4,  3:4  12:1
        # peasant1 4:4, 5:4, 6:4,  7:4  12:1
        # peasant2 8:3, 9:4, 10:4, 11:4 12:2
        print ("1111111_______________________________________________________________")
        print (env.public_state.turn)
        print (env.private_state.__unused_cards__)
        print (env.person_states[0].hand_cards.key)
        print (env.person_states[0].hand_cards.num_cards)
        print (env.person_states[1].hand_cards.key)
        print (env.person_states[2].hand_cards.key)
        print (type(infos[0].person_state))
        print (infos[0].person_state.hand_cards.key)

        ## 4 turn = 0 license_id = 2
        self.assertEqual(env.public_state.turn,0)
        action = DouDiZhuPokerAction([0], [])
        self.assertFalse(env.is_action_valid(action,public_state,person_states[public_state.turn]), False)
        action = DouDiZhuPokerAction([DouDiZhuPokerUtil.str_to_rank['x']], [])
        infos, public_state, person_states, private_state = env.forward(action) ############################################# cheat
        self.assertEqual(public_state.license_playerid,2)
        self.assertEqual(public_state.turn,1)
        action = DouDiZhuPokerAction([8, 8, 8, 8], [9, 10])
        self.assertFalse(env.is_action_valid(action,public_state,person_states[public_state.turn]),False)
        # landlord 0:4, 1:4, 2:4,  3:4  12:1
        # peasant1 4:4, 5:4, 6:4,  7:4  12:1
        # peasant2 8:3, 9:4, 10:4, 11:4 12:2 13:1 14:1
        # peasant2 8:3, 9:4, 10:4, 11:4 12:2
        print ("1111_______________________________________________________________ cheat")
        print (env.private_state.__unused_cards__.key)
        print (env.person_states[0].hand_cards.key)
        print (env.person_states[0].hand_cards.num_cards)
        print (env.person_states[1].hand_cards.key)
        print (env.person_states[2].hand_cards.key)

        ## 5 turn == 1 license_id =0
        self.assertEqual(env.public_state.epoch,51 + 5)
        action = DouDiZhuPokerAction([DouDiZhuPokerUtil.str_to_rank['x']], [])
        self.assertTrue(env.public_state.continuous_cheat_num,1)
        infos, public_state, person_states, private_state= env.forward(action) ########################################## cheat
        # landlord 0:4, 1:4, 2:4,  3:4  12:1
        # peasant1 4:4, 5:4, 6:4,  7:4  12:1
        # peasant2 8:3, 9:4, 10:4, 11:4 12:2 13:1 14:1
        print ("111111111111_______________________________________________________________ cheat")
        print (env.private_state.__unused_cards__.key)
        print (env.person_states[0].hand_cards.key)
        print (env.person_states[0].hand_cards.num_cards)
        print (env.person_states[1].hand_cards.key)
        print (env.person_states[2].hand_cards.key)

        ########################################################################## 2 round ############################################
        ## 6 turn == 2 license_id =0
        self.assertEqual(env.public_state.license_playerid, 2)
        self.assertEqual(env.public_state.is_response, False)
        self.assertEqual(env.public_state.turn, 2)
        action = DouDiZhuPokerAction([8], [])
        infos,public_state,person_states,private_state= env.forward(action)
        # landlord 0:4, 1:4, 2:4,  3:4  12:1
        # peasant1 4:4, 5:4, 6:4,  7:4  12:1
        # peasant2 8:2, 9:4, 10:4, 11:4 12:2 13:1 14:1
        print ("22222_______________________________________________________________ start")
        print (env.private_state.__unused_cards__.key)
        print (env.person_states[0].hand_cards.key)
        print (env.person_states[0].hand_cards.num_cards)
        print (env.person_states[1].hand_cards.key)
        print (env.person_states[2].hand_cards.key)

        
        ## 7 turn == 0 license_id = 0
        self.assertEqual(env.public_state.license_playerid, 2)
        self.assertEqual(env.public_state.turn, 0)
        self.assertEqual(env.public_state.is_response, True)
        action = DouDiZhuPokerAction([DouDiZhuPokerUtil.str_to_rank['x']], [])
        self.assertTrue(env.is_action_valid(action,public_state,person_states[public_state.turn]))
        action = DouDiZhuPokerAction([0, 0, 0, 0],[])
        infos, public_state, person_states, private_state= env.forward(action) #################
        print ("22222_______________________________________________________________ 0 boom")
        print (env.private_state.__unused_cards__.key)
        print (env.person_states[0].hand_cards.key)
        print (env.person_states[0].hand_cards.num_cards)
        print (env.person_states[1].hand_cards.key)
        print (env.person_states[2].hand_cards.key)
        self.assertEqual(person_states[0].hand_cards.card_pointrank_count[0], 0)
        self.assertEqual(person_states[0].hand_cards.card_pointrank_count[1], 4)
        self.assertEqual(person_states[0].hand_cards.card_pointrank_count[12], 1)
        # landlord 0:0, 1:4, 2:4,  3:4  12:1
        # peasant1 4:3, 5:4, 6:4,  7:4  12:1
        # peasant2 8:2, 9:4, 10:4, 11:4 12:2 13:1 14:1

        ## 8 turn == 1 license_id =0
        action = DouDiZhuPokerAction([DouDiZhuPokerUtil.str_to_rank['x']], [])
        env.forward(action)
        ## 9 turn = 2  license_id = 0
        action = DouDiZhuPokerAction([DouDiZhuPokerUtil.str_to_rank['x']], [])
        env.forward(action)
        # landlord 0:0, 1:4, 2:4,  3:4  12:0 
        # peasant1 4:3, 5:4, 6:4,  7:4  12:1
        # peasant2 8:2, 9:4, 10:4, 11:4 12:2 13:1 14:1
        self.assertEqual(env.public_state.is_response, False)
        self.assertEqual(env.public_state.license_playerid, 0)


        ########################################## round 3 ########################
        #10 turn = 0 license_id = 0
        action = DouDiZhuPokerAction([2,2,2,2], [])
        env.forward(action)
        print ("3333333 _______________________________________________________________0 2222")
        print (env.private_state.__unused_cards__.key)
        print (env.person_states[0].hand_cards.key)
        print (env.person_states[0].hand_cards.num_cards)
        print (env.person_states[1].hand_cards.key)
        print (env.person_states[2].hand_cards.key)


        ## 11 turn == 1 license_id =0
        action = DouDiZhuPokerAction([DouDiZhuPokerUtil.str_to_rank['x']], [])
        env.forward(action)
        ## 12 turn = 2  license_id = 0
        action = DouDiZhuPokerAction([DouDiZhuPokerUtil.str_to_rank['x']], [])
        env.forward(action)
        # landlord 0:0, 1:4, 2:4,  3:4  12:0 
        # peasant1 4:3, 5:4, 6:4,  7:4  12:1
        # peasant2 8:4, 9:4, 10:4, 11:4 12:2  
        
        # 13 turn =0 license_id = 0
        action = DouDiZhuPokerAction([1,1,1,1], [])
        self.assertTrue(env.is_action_valid(action, public_state, person_states[public_state.turn]))
        env.forward(action)
        print ("3333333 _______________________________________________________________0 1111")
        print (env.private_state.__unused_cards__.key)
        print (env.person_states[0].hand_cards.key)
        print (env.person_states[0].hand_cards.num_cards)
        print (env.person_states[1].hand_cards.key)
        print (env.person_states[2].hand_cards.key)


        ## 14 turn == 1 license_id =0
        action = DouDiZhuPokerAction([DouDiZhuPokerUtil.str_to_rank['x']], [])
        env.forward(action)
        ## 15 turn = 2  license_id = 0
        action = DouDiZhuPokerAction([DouDiZhuPokerUtil.str_to_rank['x']], [])
        env.forward(action)
        # landlord 0:0, 1:2, 2:2,  3:2  12:0 
        # peasant1 4:3, 5:4, 6:4,  7:4  12:1
        # peasant2 8:4, 9:4, 10:4, 11:4 12:2


        # 16 turn =0 license_id = 0
        action = DouDiZhuPokerAction([3,3,3,3],[])
        print (action.key)
        self.assertEqual(env.public_state.is_response,False)
        self.assertTrue(env.is_action_valid(action,public_state,person_states[public_state.turn ]))
        infos, public_state, person_states, private_state = env.forward(action)
        print ("3333333 _______________________________________________________________0 3333")
        print (env.private_state.__unused_cards__.key)
        print (env.person_states[0].hand_cards.key)
        print (env.person_states[0].hand_cards.num_cards)
        print (env.person_states[1].hand_cards.key)
        print (env.person_states[2].hand_cards.key)

        ## 14 turn == 1 license_id =0
        action = DouDiZhuPokerAction([DouDiZhuPokerUtil.str_to_rank['x']], [])
        env.forward(action)
        ## 15 turn = 2  license_id = 0
        action = DouDiZhuPokerAction([DouDiZhuPokerUtil.str_to_rank['x']], [])
        env.forward(action)
        # landlord 0:0, 1:2, 2:2,  3:2  12:0
        # peasant1 4:3, 5:4, 6:4,  7:4  12:1
        # peasant2 8:4, 9:4, 10:4, 11:4 12:2

        action = DouDiZhuPokerAction([12],[])
        print (action.key)
        self.assertEqual(env.public_state.is_response,False)
        self.assertTrue(env.is_action_valid(action,public_state,person_states[public_state.turn ]))
        infos, public_state, person_states, private_state = env.forward(action)
        print ("3333333 _______________________________________________________________0 12")
        print (env.private_state.__unused_cards__.key)
        print (env.person_states[0].hand_cards.key)
        print (env.person_states[0].hand_cards.num_cards)
        print (env.person_states[1].hand_cards.key)
        print (env.person_states[2].hand_cards.key)

        print (env.person_states[0].hand_cards.num_cards)
        expected_scores = [1,1,-2]
        scores = public_state.scores
        print (public_state.scores)
        print (public_state.is_terminal)
        for i in range(len(scores)):
            self.assertEqual(scores[i], expected_scores[i])
        
