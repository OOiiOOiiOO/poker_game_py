##poker player strategy and i/o

import random, pokerhands

def evaluate(player):
	
	value=player.get_value()
	
def calc_bet(player):

                   
        max_bet=player.stack-player.to_play
        min_bet=player.to_play
        if max_bet<min_bet:
        	min_bet=max_bet
        print ('max bet '+str(max_bet))
        print ('min be  '+str(min_bet))
        
        

        if max_bet<0:
                max_bet=player.stack
				
        bet_amount=random.randrange(min_bet,max_bet+1,5)
        
        
        return bet_amount
	
  class Strategy():
        
        def __init__(self, player):
                
                self.tight=0
                self.aggression=0
                self.cool=0
                self.player=player
                self.name=str(self.__class__.__name__)

        
              
        
        
        def play_style(self):
                
                pass

        def decide_play(self, player, pot):
                
                pass

