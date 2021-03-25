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
