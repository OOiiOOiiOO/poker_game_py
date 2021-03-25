created 'position' variable.  

'''
__author__='philip'

import random
import pokerhands
from operator import attrgetter
import time
import pokerstrat


#card class

class Card:

    RANKS=['2','3','4','5','6','7','8','9','10','J', 'Q', 'K', 'A']

    SUITS=['h', 'c', 's', 'd']

    def __init__(self,rank, suit, faceup=True):

        self.rank=rank
        self.suit=suit
        self.values=[]
        self.__value=(Card.RANKS.index(self.rank)+1)
        
        self.faceup=faceup

    def __str__(self):

        if self.faceup:
            
            return str(self.rank)+str(self.suit)
        else:
            return 'XX'

    @property

    def value(self):

        v=self.__value

        return v

#hand class (also used for Player)

class Hand:

    serial=0

    def __init__(self, name, table, strategy='Random'):

        
        self.strategy=[]
        self.stratname=strategy
        strategy_class=getattr(pokerstrat, strategy)
        strat=strategy_class(self)
        self.strategy.append(strat)
               
        
        self.cards=[]
        self.total_cards=(self.cards+table.cards)
        table.players.append(self)
        self.name=name
        
        Hand.serial+=1
        self.position=Hand.serial
        self.small_blind=False
        self.big_blind=False
        self.dealer=False
        self.hand_value=0
        self.rep=''
        self.tie_break=0
        self.raw_data=0
        self.is_folded=False
        self.stack=1000
        
        self.stake=0
        self.in_pot=0
        self.to_play=0
        self.all_in=False
        self.first_all_in=False
        self.raised=0
        self.carry_over=0

        #data points for play analysis:

        self.history=[]

        self.pots_played=0
        self.win=0
        self.raises=0
        self.calls=0
        self.checks=0
    def play_analysis(self):

        pass

    @property

    def get_position(self):

        return self.position%pot.table_size
    
    def __str__(self):


        rep='\n'+str(self.name)+'\t    stack='+str(self.stack)+'\n'
        
        if self.small_blind:
            rep+=' small blind'
        elif self.big_blind:
            rep+=' big blind'
        elif self.dealer:
            rep+=' dealer'
        

        return rep
   
        
    
    def get_value(self):
        
        self.total_cards=(self.cards+table.cards)
        
        rep, hand_value, tie_break, raw_data=pokerhands.evaluate_hand(self.total_cards)
        
        self.rep=str(rep)
        self.hand_value=hand_value
        self.tie_break=tie_break
        self.raw_data=raw_data
        
    
        return hand_value, rep, tie_break, raw_data

   
    def print_cards(self):

        rep=''

        if self.is_folded:
            rep='FF'

        else:

            for card in self.cards:

                rep+=str(card)+'  '
        

        print (rep)
        
        
    def flip(self):
            
        for card in self.cards: card.faceup=not card.faceup

    def fold(self, pot):

        self.is_folded=True
        self.in_pot=0
        self.stake=0
        self.raised=0
        
     
        print (str(self.name)+' folds')

        pot.folded_players.append(self)
        if self in pot.active_players:
        
            pot.active_players.remove(self)
        
                
        if pot.one_remaining:
        	
            pot.stage=5

    def no_play(self, pot):
    	
    	next_player(pot)

    	self.stake=0
    	
   	
    def check_call(self, pot):
    	
        
        
        if self.to_play==0:
            print (str(self.name)+' checks')
        else:
        		if self.to_play>self.stack:
        			self.stake=self.stack
        		else:
        			self.stake=self.to_play
        		print (str(self.name)+' calls '+str(self.stake))
        		if pot.stage==0 and pot.raised==False:
        			pot.limpers+=1

        next_player(pot)
    
    
    def bet(self, pot, stake):
        
        if pot.already_bet:
            print (str(self.name)+' raises '+str(stake-self.to_play))
            self.raised+=1
            pot.limpers=0
            pot.raised=True
        else:
            print (str(self.name)+' bets '+str(stake))
        
            pot.already_bet=True
      
        self.stake=stake
        pots[-1].to_play+=(self.stake-self.to_play)
        
        
        
        
        next_player(pot, True)
        
    def ante(self, pot):
        
        if self.small_blind:
            self.stack-=BLINDS[0]
            pot.total+=BLINDS[0]
            self.in_pot+=BLINDS[0]
            
        if self.big_blind:
            self.stack-=BLINDS[1]
            pot.total+=BLINDS[1]
            pot.to_play=BLINDS[1]
            self.in_pot+=BLINDS[1]
        
                    
    def bust(self):

        print (str(self.name)+' is bust')
        list_index=table.players.index(self)
        for p in table.players[list_index+1:]:
            p.position-=1
            
        table.players.remove(self)
        
        
    def clear(self):

      self.cards=[]
      self.is_folded=False
      self.all_in=False
      self.raised=0
      

    def add(self, cards):

      self.cards.append(cards)

#__________represents the card deck - shuffled each round            
        
class Deck(Hand):

    def __init__(self):

        self.cards=[]

    def populate(self):

        for rank in Card.RANKS:

            for suit in Card.SUITS:

                card=Card(rank, suit)
                self.cards.append(card)

    def shuffle(self):

        random.shuffle(self.cards)

    def print_cards(self):

        rep=''

        for card in self.cards:

            rep+=str(card)+' '

        print (rep)

    def deal_to(self, hand, cards=1, faceup=True):

        if len(self.cards)<cards:
                print ('not enough cards to deal')
                
        elif len(self.cards)==0:
                print ('deck empty')
                
        else:
                dealt=[]
                if not faceup:
                    for card in self.cards:
                         card.faceup=False
                
                for i in range (0,cards):
                        dealt.append(self.cards.pop())
                
                        
                for card in dealt:
                    
                    hand.add(card)

#__________________represents the overall game    

class Table(Hand):

    def __init__(self):

                
        self.cards=[]
        self.players=[]
        self.is_folded=False
        self.button=0
        self.hands=0
        self.blinds_timer=0
        
    def print_cards(self):

        rep='Community cards_______________\n'

        if self.is_folded:
            rep='FF'

        else:

            for card in self.cards:
                card.faceup=True
                rep+=str(card)+' '

        print (rep)

    def print_players(self):
    	
    	for player in self.players:
    		print (player)
    		
    def clear(self):

      self.cards=[]
      
      

#_______________POT represents the pot for each individual round of play

class Pot(object):
    
    stage_dict={0:'pre-flop bet', 1:'dealing the flop', 2:'dealing the turn', 3:'dealing the river'}
    deal_sequence=[0,3,1,1]
    pot_number=0
    
    def __init__(self, table, name):
        
   
        self.players=[]
        self.folded_players=[]
        self.active_players=[]
        self.limpers=0
        self.name=name
        self.blinds=BLINDS
                    
        self.total=0
        
        self.button=table.button
        #the amount each player has to call
        self.to_play=0
        #0=antes+ pre-flop, 1=post-flop, 2=turn, 3=river
        self.stage=0
        #defines turn within each betting stage
        self.turn=0
        #self.no_raise
        self.no_raise=0
        #already bet - works out if the round starts with 0 bet 
        self.already_bet=False
        self.raised=False
        

    @property

    def is_frozen(self):

        if len(self.active_players)<=1:
        	self.active_players=[]
        	return True
        else:
            return False

    @property

    def yet_to_play(self):

        ytp=self.table_size-(self.turn+1)
        if ytp<1: ytp=1

        return ytp

    @property

    def one_remaining(self):

        if len(self.folded_players)==(self.table_size-1):

            return True

        else:

            return False
        
    @property
    
    def table_size(self):
        
        
        return len(self.players)
        
    def __str__(self):

            rep='Pot= '+str(self.total)+'.  to play:'+str(self.to_play)
            return rep
            
    def set_blinds(self):
        
        dealer=(self.button)%self.table_size
        
        small_blind=(self.button+1)%self.table_size

        big_blind=(self.button+2)%self.table_size

        self.players[dealer].dealer=True

        self.players[small_blind].small_blind=True

        self.players[big_blind].big_blind=True

        return
    	

   

    def who_plays(self):

        next_up=0

        if self.stage==0:

            next_up=(self.button+3)%self.table_size

            return next_up

        else:

            next_up=(self.button+1)%self.table_size
            return next_up


class Side_pot(Pot):
    
    serial=0
    
    def __init__(self, parent):
        
        Pot.__init__(self, parent, Pot)
        
        self.button=parent.button
        Side_pot.serial+=1
        self.name='side pot '+str(Side_pot.serial)
        
        self.players=[]
           


