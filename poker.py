''' 
Author: Miao Cheng
Email: chengmiao0808@gmail.com
Description: this file defines the rules and methods of poker cards.
'''

import random

class poker(object):
	def __init__(self):	
		# Define the four suits of cards.
		self.suit = ['spade', 'heart', 'club', 'diamond']
		# Define the 13 numbers of cards, ordered from low to high.
		self.number = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
		# A list of 52 cards.
		self.poker_cards = []
		# Define all the possible patterns of a hand of five cards.
		# Explanation of the patterns and comparison rules: 
		# https://www.pokerstars.com/poker/games/rules/hand-rankings/
		# Patterns are ordered from low to high.
		self.pattern = ['high_card', 'one_pair', 'two_pair', 'three_of_a_kind', 
				'straight', 'flush', 'full_house', 'four_of_a_kind', 'straight_flush']
		# Generate the list of cards. Each card is in the format '<number>_<suit>',
		# e. g., 5_club, A_diamond, etc.
		for s in self.suit:
			for n in self.number:
				self.poker_cards.append(n + '_' + s)

	# Deal five cards to each player by randomly sample the card list.
	def deal_cards(self, player_count):
		return random.sample(self.poker_cards, player_count*5)


	# Given a hand of 5 cards, find the pattern of this hand.
	# The function returns a pattern description list, with the first element
	# being the name of the pattern and the following elements being the 
	# numbers which are relavant. 
	def find_pattern(self, hand):
		# Record the number of appearance of each suit.
		suit_count = {}
		# Record the number of appearance of each number.
		number_count = [0] * 13

		# Split the strings of cards and count the appearance of
		# suits and numbers.
		for h in hand:
			n = h.split('_')[0]
			s = h.split('_')[1]

			if not suit_count.get(s):
				suit_count[s] = 1
			else:
				suit_count[s] += 1

			number_count[self.number.index(n)] += 1

		# Decide whether a hand is straight or not.
		is_straight = False
		flag = 0
		straight_highest = ''
		for i in xrange(13):
			if number_count[i] != 1 and flag > 0:
				break
			if number_count[i] == 1:
				flag += 1
				# If 5 consecutive numbers appear, the hand is straight.
				if flag == 5:
					# Record the highest number of the straight.
					straight_highest = self.number[i]
					is_straight = True

		# A special case: A, 2, 3, 4, 5. Highest number is 5.
		if number_count == [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]:
			straight_highest = '5'
			is_straight = True

		# If all cards have the same suit and the hand is also a straight,
		# then the pattern is straight_flush.
		if len(suit_count) == 1 and is_straight:
			# Return pattern and highest number.
			return ['straight_flush', straight_highest]

		# If all cards have the same suit but the hand is not a straight,
		# then the pattern is flush.
		if len(suit_count) == 1 and not is_straight:
			# Return the pattern and the card numbers in descending order.
			pattern = ['flush']
			for i in xrange(12, -1, -1):
				if number_count[i] == 1:
					pattern.append(self.number[i])
			return pattern

		# If the hand is a straight but not flush, then the pattern is straight.
		if is_straight:
			# Return the pattern and the highest number.
			return ['straight', straight_highest]

		# If four cards in the hand have the same number,
		# then the pattern is four_of_a_kind.
		if number_count.count(4) == 1:
			# Return the pattern and the number which appears four times.
			return ['four_of_a_kind', self.number[number_count.index(4)]]
			
		# If three cards have the same number and the other two also have the same number,
		# then the pattern is full_house.
		if number_count.count(3) == 1 and number_count.count(2) == 1:
			# Return the pattern and the number which appears three times.
			return ['full_house', self.number[number_count.index(3)]]

		# If three cards have the same number and the other two have different numbers,
		# then the patter is three_of_a_kind.
		if number_count.count(3) == 1:
			# Record the pattern and the number which appears three times.
			return ['three_of_a_kind', self.number[number_count.index(3)]]

		# If two pairs exist, then the pattern is two_pair.
		if number_count.count(2) == 2:
			# Return the pattern and the numbers of the two pairs in descending order, 
			# and then add the one number which does not belong to any pair.
			return ['two_pair', self.number[len(number_count)-number_count[::-1].index(2)-1], 
				self.number[number_count.index(2)], self.number[number_count.index(1)]]

		# If only one pairs exists, then the pattern is one_pair.
		if number_count.count(2) == 1:
			pattern = ['one_pair', self.number[number_count.index(2)]]
			for i in xrange(12, -1, -1):
				if number_count[i] == 1:
					pattern.append(self.number[i])
			# Return the pattern, the number of the pair, and three other numbers
			# in descending order.
			return pattern

		# If the hand does not belong to any of the previous patterns, 
		# then the hand has pattern high_card.
		pattern = ['high_card']
		for i in xrange(12, -1, -1):
			if number_count[i] == 1:
				pattern.append(self.number[i])
		# Return the pattern and the numbers in descending order.
		return pattern


	# Compare two hands according to the rules described in: 
	# https://www.pokerstars.com/poker/games/rules/hand-rankings/
	def compare_hand(self, hand_a, hand_b):
		pattern_a = self.find_pattern(hand_a)
		pattern_b = self.find_pattern(hand_b)
		# If the patterns of the two hands are different,
		# then the hand whose pattern ranks higher wins.
		if pattern_a[0] != pattern_b[0]:
			idx_a = self.pattern.index(pattern_a[0])
			idx_b = self.pattern.index(pattern_b[0])
			if idx_a > idx_b:
				return '>'
			else:
				return '<'
		else:
			if pattern_a == pattern_b:
				# If the whole pattern descriptions are the same, then hand_a wins.
				return '>'
			for i in xrange(1, len(pattern_a)):
				# Compare the numbers in the pattern description list in order.
				idx_a = self.number.index(pattern_a[i])
				idx_b = self.number.index(pattern_b[i])
				if idx_a > idx_b:
					return '>'
				if idx_a < idx_b:
					return '<'
