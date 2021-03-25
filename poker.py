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
