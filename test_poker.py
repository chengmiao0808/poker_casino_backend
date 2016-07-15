''' 
Author: Miao Cheng
Email: chengmiao0808@gmail.com
Description: this file tests the class poker.
'''

from poker import poker

# Test the find_pattern function. If the outcome of the 
# find_pattern function of the poker class is the same as
# the correct outcome, this function returns True, otherwise
# it returns False.
def test_find_pattern(test_poker, hand, result):
	if result == test_poker.find_pattern(hand):
		return True
	else:
		return False

# Test the compare_hand function. If the outcome of the 
# compare_hand function of the poker class is the same as
# the correct outcome, this function returns True, otherwise
# it returns False.
def test_compare_hand(test_poker, hand_a, hand_b, result):
	if result == test_poker.compare_hand(hand_a, hand_b):
		return True
	else:
		return False

# Define the test_poker object of the poker class.
test_poker = poker()

# Test cases for the find_pattern function.
hand_list = [
['5_club', '6_club', '9_club', '7_club', '8_club'],
['5_heart', '4_heart', '3_heart', '2_heart', 'A_heart'],
['A_heart', 'A_club', 'A_spade', 'A_club', '8_club'],
['K_heart', 'K_club', 'K_spade', '10_heart', '10_club'],
['8_club', '6_club', 'Q_club', '4_club', '3_club'],
['2_diamond', '3_club', '4_spade', '6_club', '5_diamond'],
['J_club', 'J_heart', 'J_diamond', '5_club', '8_diamond'],
['10_diamond', '10_club', 'K_diamond', '6_club', '6_spade'],
['A_heart', 'A_club', '6_heart', '2_diamond', '8_club'],
['K_heart', '3_diamond', '10_club', 'J_spade', '6_heart']
]

# Correct result of the test cases for the find_pattern function.
result_list = [
['straight_flush', '9'],
['straight_flush', '5'],
['four_of_a_kind', 'A'],
['full_house', 'K'],
['flush', 'Q', '8', '6', '4', '3'],
['straight', '6'],
['three_of_a_kind', 'J'],
['two_pair', '10', '6', 'K'],
['one_pair', 'A', '8', '6', '2'],
['high_card', 'K', 'J', '10', '6', '3']
]

all_correct = True
# Record the test cases for which find_pattern gives wrong answers.
error_hand = []
for hand, result in zip(hand_list, result_list):
	if not test_find_pattern(test_poker, hand, result):
		all_correct = False
		error_hand.append(hand)

if all_correct:
	print 'All find_pattern tests passed.'
else:
	print 'find_pattern failed. Error occurs in the following hands:'
	print error_hand


# "hand_a" of the test cases of the compare_hand function.
hand_a_list = [
['5_heart', '4_heart', '3_heart', '2_heart', 'A_heart'],
['A_heart', 'A_club', 'A_spade', 'A_club', '8_club'],
['K_heart', 'K_club', 'K_spade', '10_heart', '10_club'],
['8_club', '6_club', 'Q_club', '4_club', '3_club'],
['2_diamond', '3_club', '4_spade', '6_club', '5_diamond'],
['J_club', 'J_heart', 'J_diamond', '5_club', '8_diamond'],
['10_diamond', '10_club', 'K_diamond', '6_club', '6_spade'],
['A_heart', 'A_club', '6_heart', '2_diamond', '8_club'],
['K_heart', '3_diamond', '10_club', 'J_spade', '6_heart'],
['K_heart', '3_diamond', '10_club', 'J_spade', '6_heart'],
['K_heart', 'K_club', 'K_spade', '10_heart', '10_club'],
['5_heart', '4_heart', '3_heart', '2_heart', 'A_heart'],
['A_heart', 'A_club', 'A_spade', 'A_club', '8_club'],
['K_heart', 'K_club', 'K_spade', '10_heart', '10_club'],
['8_club', '6_club', 'Q_club', '4_club', '3_club'],
['2_diamond', '3_club', '4_spade', '6_club', '5_diamond'],
['J_club', 'J_heart', 'J_diamond', '5_club', '8_diamond'],
['10_diamond', '10_club', 'K_diamond', '6_club', '6_spade'],
['A_heart', 'A_club', '6_heart', '2_diamond', '8_club'],
['K_diamond', '5_heart', '4_diamond', 'Q_club', '6_diamond'],
['6_diamond', '7_spade', '6_spade', '2_club', '4_diamond'],
['K_diamond', '9_diamond', 'K_heart', 'J_diamond', '7_club']
]

# "hand_b" of the test cases of the compare_hand function.
hand_b_list = [
['6_heart', '8_heart', '9_heart', '10_heart', '7_heart'],
['10_heart', '10_club', '10_spade', '10_club', 'A_club'],
['5_heart', '5_club', '5_spade', 'A_heart', 'A_club'],
['Q_spade', '4_spade', '5_spade', '3_spade', '2_spade'],
['6_heart', '8_heart', '7_heart', '9_heart', '10_heart'],
['A_club', '2_diamond', '3_club', 'A_diamond', 'A_spade'],
['10_heart', '10_spade', 'K_heart', '7_club', '7_spade'],
['9_club', '9_heart', 'A_spade', 'K_spade', 'J_spade'],
['K_spade', '10_diamond', 'J_club', '7_heart', '8_club'],
['K_diamond', '3_heart', '10_spade', 'J_club', '6_diamond'],
['A_heart', 'A_club', '6_heart', '2_diamond', '8_club'],
['A_heart', 'A_club', 'A_spade', 'A_club', '8_club'],
['K_heart', 'K_club', 'K_spade', '10_heart', '10_club'],
['8_club', '6_club', 'Q_club', '4_club', '3_club'],
['2_diamond', '3_club', '4_spade', '6_club', '5_diamond'],
['J_club', 'J_heart', 'J_diamond', '5_club', '8_diamond'],
['10_diamond', '10_club', 'K_diamond', '6_club', '6_spade'],
['A_heart', 'A_club', '6_heart', '2_diamond', '8_club'],
['K_heart', '3_diamond', '10_club', 'J_spade', '6_heart'],
['8_spade', '3_club', '8_club', '4_heart', 'K_club'],
['2_heart', 'K_spade', '5_spade', 'J_heart', 'J_diamond'],
['4_diamond', 'A_heart', '8_spade', '5_heart', '5_diamond']
]

# Correct results of the test cases of the compare_hand function.
compare_result_list = [
'<', '>', '>', '>', '<', '<', '<', '>', '<', '>', '>',
'>', '>', '>', '>', '>', '>', '>', '>', '<', '<', '>'
]

all_compare_correct = True
# Record the test cases for which compare_hand gives wrong answers.
error_hand_pair = []

for hand_a, hand_b, compare_result in zip(hand_a_list, 
	hand_b_list, compare_result_list):
	if not test_compare_hand(test_poker, hand_a, hand_b, compare_result):
		all_compare_correct = False
		error_hand_pair.append([hand_a, hand_b])

if all_compare_correct:
	print 'All compare_hand tests passed.'
else:
	print 'compare_hand failed. Error occurs in the following hand pairs:'
	print error_hand_pair
