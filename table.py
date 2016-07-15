''' 
Author: Miao Cheng
Email: chengmiao0808@gmail.com
Description: this file defines and implements the class of table.
'''

from player import player
from poker import poker
import random


SEATS = 6


class table(object):
	def __init__(self, t_id, seats = SEATS):
		# Mark the table id, and the format of table id is like: 
		# "table0", "table1", "table2", ...
		self.id = t_id
		# Mark the number of seats.
		self.seats = seats
		# Create a poker class.
		self.t_poker = poker()
		# Mark whether the table is in a game.
		self.is_playing = False
		# Mark the index of players who have bet.
		self.bet_idx = 0
		# Store the current list players seated here.
		self.players_list = []
		# Store the last hands of players who have played.
		self.players_last_hands = {}
		# Randomly assign the number of players.
		self.player_count = int(random.uniform(1, seats))
		# Initialize the list of players seated here.
		for i in xrange(self.player_count):
			p_id = int(t_id.lstrip('table'))*seats + i
			p_id = 'player%i' % p_id
			new_player = player(p_id)
			self.players_list.append(new_player)


	# Get the current funds of players seated at the table.
	def get_funds(self):
		players_funds = ""
		for player in self.players_list:
			players_funds += str(player.id) + ": " + str(player.fund) + ", "
		return players_funds.strip(", ")


	# Look for a player seated at the table (with player id specified).
	# Return the index of the specified player or -1 if not found.
	def find_player(self, p_id):
		p_idx = -1
		for i in xrange(self.player_count):
			if self.players_list[i].id == p_id:
				p_idx = i
				break
		return p_idx


	# Delete a player who is seated here (with player id specified).
	def delete_player(self, p_id):
		del self.players_list[self.find_player(p_id)]
		self.player_count -= 1


	# Add a new player to the table.
	def add_player(self, p_id):
		new_player = player(p_id)
		self.players_list.append(new_player)
		self.player_count += 1


	# Deal cards to the current players seated at the table.
	def deal(self):
		t_cards = self.t_poker.deal_cards(self.player_count)
		for i in xrange(0, len(t_cards)):
			self.players_list[i % self.player_count].current_hand.append(t_cards[i])


	# Bet amounts for all the computer players seated at the table.
	def bet(self):
		p_idx = self.bet_idx
		while p_idx < self.player_count:
			# For the player who is seated at the first place of the table,
			# bet $ 1~5.
			if p_idx == 0:
				# Check if the human player is seated here.
				if self.players_list[p_idx].id != 'player0':
					self.players_list[p_idx].bet_amount = int(random.uniform(1, 5))
					self.players_list[p_idx].fund -= self.players_list[p_idx].bet_amount
					p_idx += 1
				else:
					break
			# For the non-first player seated at the table, bet $ 0~5 more than its predecessor.
			else:
				# Check if the human player is seated here.
				if self.players_list[p_idx].id != 'player0':
					self.players_list[p_idx].bet_amount = (self.players_list[p_idx-1].bet_amount 
														+ int(random.uniform(1, 5)))
					self.players_list[p_idx].fund -= self.players_list[p_idx].bet_amount
					p_idx += 1
				else:
					break
		# Mark the number of players who have bet and return.
		self.bet_idx = p_idx
		return p_idx


	# Update the funds of players after one hand of game according to the rules.
	# And reset the states of the table and the players.
	def update_funds_and_reset(self):
		amount_sum, winner_idx = 0, 0
		# Look for the winner and compute the sum of bet amounts.
		for i in xrange(0, self.player_count):
			amount_sum += self.players_list[i].bet_amount
			hand = ""
			for c in self.players_list[i].current_hand:
				hand += c + ", "
			self.players_last_hands[self.players_list[i].id] = hand.strip(", ")
			if self.t_poker.compare_hand(self.players_list[winner_idx].current_hand, 
				self.players_list[i].current_hand) == '<':
				winner_idx = i
		# Update the fund of the winner.
		self.players_list[winner_idx].fund += amount_sum
		self.players_last_hands["winner"] = self.players_list[winner_idx].id
		self.players_last_hands["current_funds"] = self.get_funds()
		# Reset the states of the table and the players.
		for i in xrange(0, self.player_count):
			del self.players_list[i].current_hand[:]
		self.bet_idx = 0
		self.is_playing = False
