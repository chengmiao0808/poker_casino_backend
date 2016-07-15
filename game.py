''' 
Author: Miao Cheng
Email: chengmiao0808@gmail.com
Description: this file implements the interactions of the game.
'''

from table import table
import random
from flask import Flask, request, jsonify


app = Flask(__name__)


# Defines fixed number of tables and seats.
TABLES, SEATS = 4, 6
# Mark the current maximum number of players.
# New player's id starts from PLAYER_IDX.
PLAYER_IDX = TABLES * SEATS
# Store the current list of table objects.
tables_list = {}
# Store the current players' funds at each table.
show_list = {}
# "player0" is the default id for the human player.
# Mark the current table id where player0 is seated.
player0_seated_table = 'table0'
# Mark whether the tables have been initialized.
has_created = False


# Initialize the tables and players if they are not created.
# Return the current list of players with funds at each table.
@app.route('/tables')
def show_tables():
	global has_created
	if not has_created:
		has_created = True		
		t_idx = 0
		tables_list.clear()
		show_list.clear()
		while t_idx < TABLES:
			t_id = 'table%i' % t_idx
			new_table = table(t_id)
			tables_list[t_id] = new_table
			show_list[t_id] = new_table.get_funds()
			t_idx += 1
	return jsonify(show_list)


# Trigger a hand at a table, and bet when player0 is seated at the current table.
@app.route('/play', methods=['POST', 'PUT'])
def play_one_hand():
	global has_created, player0_seated_table
	if not has_created:
		return "The tables are not created yet!\n"

	# Trigger a hand at a table (with its table id specified).
	# e.g. curl http://127.0.0.1:5000/play -d "table=table0" -X POST
	if request.method == 'POST':
		# Get the table id.
		t_id = request.form['table']
		# First make sure that the specified table id exists.
		if not tables_list.get(t_id):
			return "%s is not found in the table list!\n" % t_id
		# Then make sure that the specified table is not already in a game.
		if tables_list[t_id].is_playing:
			return "%s is playing right now, you cannot trigger a hand again!\n" % t_id
		i = 0
		# Check each player at the table and remove the ones whose funds are not enough.
		while i < tables_list[t_id].player_count:
			if tables_list[t_id].players_list[i].fund < 5*(i+1):
				if tables_list[t_id].players_list[i].id == 'player0':
					has_created = False
					return "You've quitted the game for running out of money!\n"
				del tables_list[t_id].players_list[i]
			else:
				i += 1
		# Make sure there are at least three players at the table who can play the game.
		if tables_list[t_id].player_count < 3:
			return "The number of players at %s is not enough!\n" % t_id
		# Clean the current players' last hands info.
		tables_list[t_id].players_last_hands.clear()
		# Mark the current table is in a game.
		tables_list[t_id].is_playing = True
		# Deal cards for each player at the table.
		tables_list[t_id].deal()
		# Let every computer player randomly bet an amount, and stop by the human player
		# if the human player (player0) is seated at this table.
		p_idx = tables_list[t_id].bet()
		# If the human player happens to be at the current table.
		if p_idx < tables_list[t_id].player_count:
			# Return the current hand of the human player.
			current_play = "Your hand: "
			for c in tables_list[t_id].players_list[p_idx].current_hand:
				current_play += c + ", "
			# Return the current bet amounts by other players before.
			current_play += "other players bet: \n"
			for i in xrange(0, p_idx):
				current_play += (str(tables_list[t_id].players_list[i].id) + ": "
							+ str(tables_list[t_id].players_list[i].bet_amount) + "\n")
			# Return the bet requirements here.
			current_play += ("Waiting for you to bet (you have to bet $ 0~5 " +
							"more than your predecessor's bet, \nor if you are the "
							+ "first player, you have to bet $ 1~5)...\n")
			# Return the whole message.
			return current_play
		else:
			# If there is no human player, all the computer players will randomly bet
			# according to the rules, update the funds and return the results. 
			tables_list[t_id].update_funds_and_reset()
			show_list[t_id] = tables_list[t_id].get_funds()
			return jsonify(tables_list[t_id].players_last_hands)

	# After a hand is triggered at a table where human player is seated, the human player
	# should bet an amount according to current situation.
	if request.method == 'PUT':
		# Get the bet amount of human player.
		# e.g. curl http://127.0.0.1:5000/play -d "amount=<bet amount: Int>" -X PUT
		amount = request.form['amount']
		p_id = 'player0'
		t_id = player0_seated_table
		# If you haven't trigger a hand at the table where human player is seated.
		if not tables_list[t_id].is_playing:
			return "You have not triggered a hand at %s!\n" % t_id
		try:
			amount = int(amount)
			c_bet_idx = tables_list[t_id].bet_idx
			# If the human player is seated at the first place of the table, check 
			# whether the bet amount is proper or not.
			if c_bet_idx == 0:
				if 1 <= amount <= 5:
					tables_list[t_id].players_list[0].bet_amount = amount
					tables_list[t_id].players_list[0].fund -= amount
					tables_list[t_id].bet_idx += 1
					tables_list[t_id].bet()
					tables_list[t_id].update_funds_and_reset()
					show_list[t_id] = tables_list[t_id].get_funds()
					return jsonify(tables_list[t_id].players_last_hands)
				else:
					return "You have to bet $ 1~5 since you are the first player!\n"
			# If the human player is seated in the middle/end of the table, refer to the
			# former players' bets and check whether the human player has bet properly.
			else:
				last_amount = tables_list[t_id].players_list[c_bet_idx-1].bet_amount
				if last_amount <= amount <= last_amount + 5:
					tables_list[t_id].players_list[c_bet_idx].bet_amount = amount
					tables_list[t_id].players_list[c_bet_idx].fund -= amount
					tables_list[t_id].bet_idx += 1
					tables_list[t_id].bet()
					tables_list[t_id].update_funds_and_reset()
					show_list[t_id] = tables_list[t_id].get_funds()
					return jsonify(tables_list[t_id].players_last_hands)
				else:
					return "You have to bet $ 0~5 more than your predecessor's bet!\n"
		# Return an error notification if the input amount is illegal.
		except ValueError:
			return "Your input amount is illegal, please input an integer!\n"


# Can add/remove a player at any table as well as change the seat of the human player.
@app.route('/update', methods=['POST', 'PUT', 'DELETE'])
def update():
	global has_created, PLAYER_IDX, player0_seated_table
	if not has_created:
		return "The tables are not created yet!\n"

	# Add a new player to a table (with table id specified) if this table is not full.
	# e.g. curl http://127.0.0.1:5000/update -d "add2=table0" -X POST
	if request.method == 'POST':
		t_id = request.form['add2']
		# First check whether the specified table id is correct.
		if not tables_list.get(t_id):
			return "%s is not found in the table list!\n" % t_id
		else:
			# Cannot add a player when the specified table is playing a game.
			if tables_list[t_id].is_playing:
				return "%s is playing righ now, you cannot add a player!\n" % t_id
			# Check whether the table is full or not, and if not add a new player.
			if tables_list[t_id].player_count < SEATS:
				p_idx = PLAYER_IDX
				# The player's id is like the following format.
				p_id = 'player%i' % p_idx
				PLAYER_IDX += 1
				tables_list[t_id].add_player(p_id)
				show_list[t_id] = tables_list[t_id].get_funds()
				# Return the table list with players after adding.
				return jsonify(show_list)
			else:
				return "%s is already full!\n" % t_id

	# Change the seat of the human player to another table (with table id specified).
	# e.g. curl http://127.0.0.1:5000/update -d "change2=table1" -X PUT
	if request.method == 'PUT':
		n_t_id = request.form['change2']
		# First check whether the specified table id is correct.
		if not tables_list.get(n_t_id):
			return "%s is not found in the table list!\n" % n_t_id
		else:
			t_id = player0_seated_table
			# Cannot change the seat when the current/new table is playing a game.
			if tables_list[t_id].is_playing or tables_list[n_t_id].is_playing:
				return "The table is playing righ now, you cannot change seat!\n"
			# Check whether the new table is full or not, and if not change the seat.
			if tables_list[n_t_id].player_count < SEATS:
				p_id = 'player0'
				t_id = player0_seated_table
				p_idx = tables_list[t_id].find_player(p_id)
				p_fund = tables_list[t_id].players_list[p_idx].fund
				tables_list[t_id].delete_player(p_id)
				show_list[t_id] = tables_list[t_id].get_funds()
				tables_list[n_t_id].add_player(p_id)
				tables_list[n_t_id].players_list[-1].fund = p_fund
				show_list[n_t_id] = tables_list[n_t_id].get_funds()
				# Mark the new table id where the human player is seated.
				player0_seated_table = n_t_id
				# Return the table list with players after changing.
				return jsonify(show_list)
			else:
				return "%s is already full!\n" % n_t_id

	# Remove a player (with player id specified).
	# e.g. curl http://127.0.0.1:5000/update -d "player=player1" -X DELETE
	if request.method == 'DELETE':
		p_id = request.form['player']
		has_deleted = False
		# Look for which table the specified player is seated.
		for t_id in tables_list:
			if tables_list[t_id].find_player(p_id) != -1:
				# Cannot remove a player if its table is playing a game.
				if tables_list[t_id].is_playing:
					return "%s is playing righ now, you cannot remove a player!\n" % t_id
				tables_list[t_id].delete_player(p_id)
				show_list[t_id] = tables_list[t_id].get_funds()
				has_deleted = True
				break
		if has_deleted:
			# If the removed player is the human player (player0), this means you have quitted
			# the current game. You can restart later.
			if p_id == 'player0':
				has_created = False
				return "You've quitted the game!\n"
			else:
				# Return the table list with players after removing.
				return jsonify(show_list)
		else:
			return "%s does not exist in the player list!\n" % p_id


if __name__ == "__main__":
	app.debug = True
	app.run()
