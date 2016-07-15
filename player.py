''' 
Author: Miao Cheng
Email: chengmiao0808@gmail.com
Description: this file defines the class of player.
'''

FUND, BET_AMOUNT = 500, 1


class player(object):
	def __init__(self, p_id, fund = FUND, bet_amount = BET_AMOUNT):
		# Mark the player id, and the format of player id is like:
		# "player0", "player1", "player2", ...
		self.id = p_id
		# Mark the current fund of the player.
		self.fund = fund
		# Mark the bet amount during the game.
		self.bet_amount = bet_amount
		# Mark the current hand during the game.
		self.current_hand = []
