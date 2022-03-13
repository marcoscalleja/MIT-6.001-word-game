# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>
import os
import math
import random
import string
import numpy as np
from numpy import load
from sklearn.metrics import SCORERS

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    SCRABBLE_LETTER_VALUES['*'] = 0
    word = word.lower()
    word_list = list(word)

    wordlen = len(word_list)

    values = []
    for letter in word_list:
        values.append(SCRABBLE_LETTER_VALUES[letter])
    
    points = sum(values)

    return points * max(7*wordlen - 3*(n-wordlen), 1)


#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    wo = ''
    for letter in hand.keys():
        for j in range(hand[letter]):
             #print(letter, end=' ')      # print all on the same line
             wo = wo + letter + ' '       #saving the letters in a str
    #print()                              # print an empty line
    return wo                             

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))
    num_vowels = num_vowels - 1 #Adding a wild card substituting a vowel

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    hand['*'] = 1
    
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    hand_2 = hand.copy()
    word = word.lower()

    #dic = get_frequency_dict(word)
    list_1 = list(word)

    new_hand = dict()

    for key in list_1:
        if key in hand:
            hand_2[key] = hand_2[key] - 1

    delete = []
    for key in hand_2:
        if hand_2[key] > 0: #we remove letters with 0 or negative count
            new_hand[key] = hand_2[key] 
    
    return new_hand

#test
#update_hand({'h': 1, 'e': 1, 'l': 2, 'o': 1}, 'hello')

#
# Problem #3: Test word validity
#

##My own function to match words with * special char:
def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    verification = []
    for index in range(len(my_word)): #We check for each character whether, when there is a letter, it has the same position in the word
      if len(my_word) == len(other_word):
        if my_word[index] == '*':
            if other_word[index] in ['a', 'e', 'e', 'o', 'u']: #We want to force * to be only a vowel!!
                verification.append(True)
            else:
                verification.append(False)
        elif my_word[index] == other_word[index]:
          verification.append(True)
        else:
          verification.append(False)
      else:
        verification.append(False)

    if False in verification:
      output = False
    else:
      output = True

    return output

def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    hand_2 = hand.copy()
    state = []
    out = False

    word = word.lower()
    
    for w in word_list:
        if match_with_gaps(word, w):
            state.append(True)
            
    if True in state: #If my word is not in wordlist then, state = []
        #dic = get_frequency_dict(list(word))

        for key in list(word):
            if key in hand_2:
                if hand_2[key] > 0: #If we still have chances
                    hand_2[key] = hand_2[key] - 1
                else:
                    state.append(False) #If we have used all the chances
            else:
                state.append(False)
        
        if False in state:
            out = False
        else:
            out = True

    return out

 #Testing   
#is_valid_word('EVIL', {'e': 1, 'v': 2, 'n': 1, 'i': 1, 'l': 2}, load_words())

#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    return sum(list(hand.values()))

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    # hand= {'a':1, 'q':1, 'l':2, 'm':1, 'u':1, 'i':1}
    # word_list = load_words()

    # BEGIN PSEUDOCODE <-- Remove this comment when you implement this function
    # Keep track of the total score
    n = calculate_handlen(hand)
    score = 0 #initialize
    finished = False

    # if n == hand_size:
    #     score1 = 0 
    # else:
    #     score1 = score1 #update score

    # As long as there are still letters left in the hand:
    
    while finished == False:
        # Display the hand
        print('Current Hand:', display_hand(hand))

            # Ask user for input
        word = input('Enter word, or "!!" to indicate that you are finished: ')
            
                
            # Otherwise (the input is not two exclamation points):
        attempts = 3
        while attempts > 0 and sum(hand.values()) > 0:         

            if word ==  '!!':
                # End the game (break out of the loop)
                finished = True
                break

            # If the word is valid:

            elif is_valid_word(word, hand, word_list) == True:
                # Tell the user how many points the word earned,
                print(F'"{word}" earned {get_word_score(word, n)} points')
                score = score + get_word_score(word, n)
                # and the updated total score
                print(f'Total: {score} points')
                
                #Now we update the hand
                hand = update_hand(hand, word)
                
                if sum(hand.values()) == 0:
                    break
                #Display updated hand
                print('Current Hand:', display_hand(hand))
                #get user input again
                
                word = input('Enter word, or "!!" to indicate that you are finished: ')

                # if word ==  '!!':
                # # End the game (break out of the loop)
                #     finished = True
                #     break
                
            # Otherwise (the word is not valid):
                # Reject invalid word (print a message)
            else:
                print('That is not a valid word. Please choose another word.')
                attempts = attempts - 1
                print(f'{attempts} attempts remaining')

                if attempts == 0:
                    break

                print('Current Hand:', display_hand(hand))
                
                #get user input again
                if sum(hand.values()) == 0:
                    break
                else:
                    word = input('Enter word, or "!!" to indicate that you are finished: ')



                # # update the user's hand by removing the letters of their inputted word
                # update_hand(hand, word)

        # Game is over (user entered '!!' or ran out of letters),
        # so tell user the total score

        if attempts == 0 or sum(hand.values()) == 0:
            finished = True
            print(f'Ran out of letters. Total score for this hand: {score} points')
        elif word == '!!':
            print(f'Total score for this hand: {score} points')
            finished = True
        else:
            print(word)
            print(hand)
            print(is_valid_word(word, hand, word_list))
            print('something weird happened')
    

        # Return the total score as result of function
        return score

#testing
play_hand({'a': 0, 'c': 0, 'f': 1, 'i': 1, '*': 1, 't':1, 'x':1}, load_words())


#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    keys_dic = list(hand.keys())
    alphabet = list(string.ascii_lowercase)
    for let in keys_dic:
        try:
            alphabet.remove(let)
        except:
            continue

    index_alpha = np.random.randint(1,len(alphabet))
    new_let = alphabet[index_alpha]
    try:
        hand[new_let] = hand.pop(letter)
    except:
        pass
           
    return hand

    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """

    #load words
    #load_words()

    HAND_SIZE = 7    #Size of the hand
    final_score = [] #List with final score

    #Entering total number of hands in an int format:
    check = False
    while check == False:
        nb_hands = input(f'Enter total number of hands: ')
        try:
            nb_hands = int(nb_hands)
        except:
            pass
        if type(nb_hands) == int:
            check = True
    
    
    #Loop nb_hands N times:
    for i in range(nb_hands):
        #Start with first hand:
        hand = deal_hand(HAND_SIZE)
        print(f'Current hand: {display_hand(hand)}')


        substitution = input('Would you like to substitute a letter?: ')

        while True:
            if substitution in ('Yes', 'yes', 'YES', 'y', 'Y'):
                print('before ', hand)
                letter = input('Which letter would you like to replace: ')
                hand = substitute_hand(hand, letter)
                print('after ',hand)
                break

            elif substitution in ('No', 'no', 'NO', 'n', 'N'):
                break

            else:
                print('You have to choose Yes or No')
                substitution = input('Would you like to substitute a letter?: ')

        # substitution = input('Would you like to substitute a letter?: ')

        # if substitution in ('Yes', 'yes', 'YES', 'y', 'Y'):
        #     sub = False
        #     while sub == False:
        #         letter = input('Which letter would you like to replace: ')
        #         print(letter)
        #         substitute_hand(hand, letter)

        #         try:
        #             hand = substitute_hand(hand, letter)
        #             sub=True
        #         except:
        #             continue


        final_score.append(play_hand(hand, word_list)) 
        print()
        print('------------------------')
    print('------------------------')
    final = f'Total score over all hands: {sum(final_score)}'

    return final


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)