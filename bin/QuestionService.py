#!/usr/bin/env python

#  This file is part of Boggle Quiz Bowl.
# 
#     Boggle Quiz Bowl is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     Foobar is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

from Question import Question
from Solution import Solution
import BoardService
import SolverService
import MathService
import FileService
import StringService
import random

# Generates a question
def generate_question():
    board = BoardService.generate_board()
    solutions = SolverService.find_words(board)
    dict = FileService.read_dictionary()
    generate = random.choice([generate_is_word_on_board, generate_starts_with_prefix, generate_ends_with_suffix])
    
    question = generate(board, solutions, dict)
    
    return question

#Generate a "does this end with prefix" question
def generate_ends_with_suffix(board, solutions, dict):
    solution = random.choice(solutions)
    
    is_correct = MathService.get_random_boolean()
    answers = ["Yes", "No"]
    prompt = "Is there a word that ends with -%s?"
    
    if is_correct:
        while len(solution.word) < 3 or solution.word[-3:] in dict:
            solution = random.choice(solutions)
        correct = ["Yes"]
        suffix = solution.word[-3:]
        justification = ["Wrong! %s ends with -%s!" % (solution.word.upper(), suffix.upper()), solution.path]
        correctExample = ["Correct! E.g. " + solution.word + " ends in " + suffix.upper(), solution.path]
    else:
        suffix = board.get_random_word(3)
        
        while not _contains_vowel(suffix) or _suffix_in_solutions(solutions, suffix):
            suffix = board.get_random_word(3)
            
        correct = ["No"]
        justification = "Wrong! No word here ends with -%s!" % suffix.upper()
        correctExample = []
        
    prompt = prompt % suffix.upper()
    
    return Question(board, prompt, answers, correct, justification, correctExample)

#Generate a "does this start with prefix" question
def generate_starts_with_prefix(board, solutions, dict):
    solution = random.choice(solutions)
    
    is_correct = MathService.get_random_boolean()
    answers = ["Yes", "No"]
    prompt = "Is there a word that starts with %s-?"
    
    if is_correct:
        while len(solution.word) < 3 or solution.word[0:3] in dict:
            solution = random.choice(solutions)
        correct = ["Yes"]
        prefix = solution.word[0:3]
        justification = ["Wrong! %s starts with %s-!" % (solution.word.upper(), prefix.upper()), solution.path]
        correctExample = ["Correct! E.g. " + solution.word + " begins with " + prefix.upper() + "-", solution.path]
    else:
        prefix = board.get_random_word(3)
        
        while not _contains_vowel(prefix) or _prefix_in_solutions(solutions, prefix):
            prefix = board.get_random_word(3)
            
        correct = ["No"]
        justification = "Wrong! No word here starts with %s-!" % prefix.upper()
        correctExample = []

    prompt = prompt % prefix.upper()
    
    return Question(board, prompt, answers, correct, justification, correctExample)
    
def generate_is_word_on_board(board, solutions, dict):
    prompt = "Is %s on this board?"
    answers = ["Yes", "No"]
    
    is_correct = MathService.get_random_boolean()
    
    if is_correct:  # Generate a question with "Yes" answer (easy)
        correct = ["Yes"]
        solution = random.choice(solutions)
        justification = ["Wrong! \"%s\" is on this board!" % solution.word.upper(), solution.path]
        correctExample = ["Correct!", solution.path]
    else:  # Generate a question with "No" answer
        word = random.choice(dict);
        
        while StringService.get_similarity(word, board.letters) < 0.4:
            word = random.choice(dict);
            
        solution = Solution(word)
        
        s = _word_in_solutions(solutions, word)
        if s is not None:
            correct = ["Yes"]
            justification = ["Wrong! \"%s\" is on this board!" % word.upper(), s.path]
            correctExample = ["Correct!", s.path]
        else:
            correct = ["No"]
            justification = "Wrong! \"%s\" is not on this board!" % word.upper()
            correctExample=[]
    
    prompt = prompt % solution.word.upper()
         
    return Question(board, prompt, answers, correct, justification, correctExample)

def _contains_vowel(word):
    vowels = "aeiou"
    return len(set(word).intersection(vowels)) > 0

def _suffix_in_solutions(solutions, suffix):
    for s in solutions:
        if len(s.word) >= len(suffix) and s.word[-len(suffix):] == suffix:
            return True
    return False
 
def _prefix_in_solutions(solutions, prefix):
    for s in solutions:
        if len(s.word) >= len(prefix) and s.word[0:len(prefix)] == prefix:
            return True
    return False
    
def _word_in_solutions(solutions, word):
    for s in solutions:
        if s.word == word:
            return s
    return None