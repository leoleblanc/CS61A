"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100 # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################

# Taking turns

def roll_dice(num_rolls, dice=six_sided):
    """Roll DICE for NUM_ROLLS times.  Return either the sum of the outcomes,
    or 1 if a 1 is rolled (Pig out). This calls DICE exactly NUM_ROLLS times.

    num_rolls:  The number of dice rolls that will be made; at least 1.
    dice:       A zero-argument function that returns an integer outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    "*** YOUR CODE HERE ***"
    score = 0
    sign = 0
    while num_rolls > 0:
        dice_rolls = dice()
        score += dice_rolls
        num_rolls -= 1
        if dice_rolls == 1:
            sign = 1
    if sign == 1:
        return sign
    return score


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    "*** YOUR CODE HERE ***"
    if num_rolls > 0:
        return roll_dice(num_rolls, dice)
    else:
        return max(opponent_score // 10, opponent_score % 10) + 1

# Playing a game

def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """
    "*** YOUR CODE HERE ***"
    if (score + opponent_score) % 7 == 0:
        return four_sided
    else:
        return six_sided

def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who

def play(strategy0, strategy1, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    """
    who = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    score, opponent_score = 0, 0
    "*** YOUR CODE HERE ***"
    while score < goal and opponent_score < goal:
        if score == 0 or opponent_score == 0:
            if who == 0:
                score = score + take_turn(strategy0(score, opponent_score), opponent_score, select_dice(score, opponent_score))
            elif who == 1:
                opponent_score = opponent_score + take_turn(strategy1(opponent_score, score), score, select_dice(opponent_score, score))
            who = other(who)
        elif score != 0 or opponent_score != 0:
            if who == 0:
                if score / opponent_score == 2 or opponent_score / score == 2:
                    score, opponent_score = opponent_score, score
                    score = score + take_turn(strategy0(score, opponent_score), opponent_score, select_dice(score, opponent_score))
                else:
                    score = score + take_turn(strategy0(score, opponent_score), opponent_score, select_dice(score, opponent_score))
            elif who == 1:
                if score / opponent_score == 2 or score / opponent_score == .5:
                    score, opponent_score = opponent_score, score
                    opponent_score = opponent_score + take_turn(strategy1(opponent_score, score), score, select_dice(opponent_score, score))
                else:
                    opponent_score = opponent_score + take_turn(strategy1(opponent_score, score), score, select_dice(opponent_score, score))
            who = other(who)
    return score, opponent_score  # You man=y wish to change this line

#######################
# Phase 2: Strategies #
#######################

# Basic Strategy


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy

# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    6.0

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 1.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 6.0.
    """
    "*** YOUR CODE HERE ***"
    def average(*args):
        n = 0
        total = 0
        while num_samples > n:
            total += fn(*args)
            n += 1
        return total / num_samples
    return average

def max_scoring_num_rolls(dice=six_sided):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE.  Print all averages as in
    the doctest below.  Assume that dice always returns positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    1 dice scores 3.0 on average
    2 dice scores 6.0 on average
    3 dice scores 9.0 on average
    4 dice scores 12.0 on average
    5 dice scores 15.0 on average
    6 dice scores 18.0 on average
    7 dice scores 21.0 on average
    8 dice scores 24.0 on average
    9 dice scores 27.0 on average
    10 dice scores 30.0 on average
    10
    """
    "*** YOUR CODE HERE ***"
    max_num_rolls, max_average_score = 0, 0
    averaged_roll_dice = make_averaged(roll_dice)
    for num_rolls in range(1, 11):
        average_score = averaged_roll_dice(num_rolls, dice)
        print(num_rolls, 'dice scores', average_score, 'on average')
        if average_score > max_average_score:
            max_num_rolls, max_average_score = num_rolls, average_score
    return max_num_rolls

def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1

def average_win_rate(strategy, baseline=always_roll(5)):
    """Return the average win rate (0 to 1) of STRATEGY against BASELINE."""
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)
    return (win_rate_as_player_0 + win_rate_as_player_1) / 2 # Average results

def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True: # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False: # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False: # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False: # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if False: # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"

# Strategies

def free_bacon(opponent_score):
    """This function calculates the score if the free bacon rule was implemented. 
    It returns an integer.
    """
    score = max(opponent_score // 10, opponent_score % 10) + 1
    return score

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    "*** YOUR CODE HERE ***"
    if free_bacon(opponent_score) >= margin:
        return 0
    return num_rolls # Replace this statement

def swap_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice when it would result in a beneficial swap and
    rolls NUM_ROLLS if it would result in a harmful swap. It also rolls
    0 dice if that gives at least MARGIN points and rolls
    NUM_ROLLS otherwise.
    """
    "*** YOUR CODE HERE ***"
    if score == 0 or opponent_score == 0:
        return bacon_strategy
    else:
        if (score + free_bacon(opponent_score)) / opponent_score == .5:
            return 0
        elif (score + free_bacon(opponent_score)) / opponent_score == 2:
            return num_rolls
        elif free_bacon(opponent_score) >= margin:
            return 0
        else:
            return num_rolls # Replace this statement

def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.
    *** YOUR DESCRIPTION HERE ***
    This strategy will incorporate the previous strategy, while also attempting to get the opponent to be stuck with 4 dice most often.  Here's the rundown:
    If a beneficial swine swap can occur, it will roll 0.
    If not, then if it can use free bacon to make the opponent use 4 dice, it will.
    If it is behind, it will take bigger risks (ie. roll more dice).
    If it is ahead, it will take less risks (ie. roll less dice).
    Returns num_rolls, which tries to optimize on the law of averages
    """
    "*** YOUR CODE HERE ***"
    bacon = (max(opponent_score // 10, opponent_score % 10) + 1)
    total = (score + opponent_score)
    if total % 7 != 0:
        if score == 0 or opponent_score == 0:
            return 5
        elif score != 0 and opponent_score < 10:
            if bacon >= 8:
                return 0
            elif (total + bacon) % 7 == 0:
                return 0
            else:
                return 5
        elif score != 0 and opponent_score != 0:
            divided_scores = score / opponent_score
            if score + bacon >= 100 and (score + bacon) / opponent_score != 2:
                return 0
            if (score + bacon) / opponent_score == .5:
                return 0
            elif (score + bacon) / opponent_score == 2:
                return 5
            elif bacon >= 8 and (score + bacon) / opponent_score != 2:
                return 0
            elif (total + bacon) % 7 == 0 and (score + bacon) / opponent_score != 2:
                return 0
            elif divided_scores > 2 and bacon >= 8:
                return 0
            elif divided_scores >= 16:
                return 0
            elif divided_scores > 8:
                return 1
            elif divided_scores > 4:
                return 2
            elif divided_scores > 2:
                return 3
            elif divided_scores > 1:
                return 4
            elif divided_scores < 1:
                return 6
            elif divided_scores < 1 / 2:
                return 7
            elif divided_scores < 1 / 4:
                return 8
            elif divided_scores < 1 / 8:
                return 9
            elif divided_scores <= 1 / 16:
                return 10
            else:
                return 5
    elif opponent_score != 0:
        if (score + bacon) / opponent_score == .5:
            return 0
        elif (score + bacon) / opponent_score == 2:
            return 4
        elif bacon >= 8 and (score + bacon) / opponent_score != 2:
            return 0
        elif (total + bacon ) % 7 == 0 and (score + bacon) / opponent_score != 2:
            return 0
        else:
            return 4
    else:
        return 4 # Replace this statement


##########################
# Command Line Interface #
##########################

# Note: Functions in this section do not need to be changed.  They use features
#       of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')
    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
