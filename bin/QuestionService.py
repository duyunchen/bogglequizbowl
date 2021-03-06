#!/usr/bin/env python

#  This file is part of Boggle Quiz Bowl.
# 
#     Boggle Quiz Bowl is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     Boggle Quiz Bowl is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with Boggle Quiz Bowl.  If not, see <http://www.gnu.org/licenses/>.

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
    #Keep generating till we get a valid question.  Probably not efficient
    #but keeps it simple.
    question = None
    while question is None:
        board = BoardService.generate_board()
        solutions = SolverService.find_words(board)
        dict = FileService.read_dictionary()
        generate = random.choice([generate_is_word_on_board, generate_starts_with_prefix, generate_ends_with_suffix, generate_front_hook, generate_back_hook, generate_double_consonant])
        question = generate(board, solutions, dict)
    return question

def generate_double_consonant(board, solutions, dictionary):
    is_correct = MathService.get_random_boolean()
    answers = ["Yes", "No"]
    prompt = "Is there a word that contains %s?"
    
    common_dc = ["ll", "nn", "ss", "tt", "dd", "mm","ff", "bb","pp"]
    valid_dc = []
    
    for dc in common_dc:
        if board.has_word(dc):
            valid_dc.append(dc)
    
    if len(valid_dc) is 0:
        return None
    
    dc_found = None
    example = None
    for dc in valid_dc:
        for s in solutions:
            if dc in s.word:
                dc_found = dc
                example = s
                break
                
    if dc_found:
        correct = ["Yes"]
        justification = ["Wrong! %s contains double consonant %s!" % (example.word.upper(), dc.upper()), example.path]
        correctExample = ["Correct! e.g. %s contains double consonant %s." % (example.word.upper(), dc.upper()), example.path]
    else:
        correct = ["No"]
        justification = "Wrong! No word here contains %s!" % dc.upper()
        correctExample = []
        
    prompt = prompt % dc.upper()
    
    return Question(board, prompt, answers, correct, justification, correctExample) 

def generate_back_hook(board, solutions, dictionary):
    is_correct = MathService.get_random_boolean()
    answers = ["Yes", "No"]
    prompt = "Does %s have a valid back hook?"
    
    solution = None
    if is_correct:
        correct = ["Yes"]
        backhook = None
        for a in solutions:
            if len(a.word) < 4:
                continue
            for b in solutions:
                if len(b.word) == len(a.word) + 1 and b.word[:-1] == a.word:
                    solution = a
                    backhook = b
                    break
            else:
                continue
            break
        
        if solution is not None:
            justification = ["Wrong! %s can be made from %s!" % (backhook.word.upper(), solution.word.upper()), backhook.path]
            correctExample = ["Correct! e.g. %s can be made from %s" % (backhook.word.upper(), solution.word.upper()), backhook.path]
        else:
            return None
    else:
        correct = ["No"]
        for a in solutions:
            if len(a.word) < 4:
                continue
            for b in solutions:
                if len(b.word) == len(a.word) + 1 and b.word[:-1] == a.word:
                    break
            else:
                solution = a
                break
            
        if solution is not None:
            justification = "Wrong! %s has no back hook here!" % solution.word.upper()
            correctExample = []
        else:
            return None
        
    prompt = prompt % solution.word.upper()
    
    return Question(board, prompt, answers, correct, justification, correctExample) 

def generate_front_hook(board, solutions, dictionary):
    is_correct = MathService.get_random_boolean()
    answers = ["Yes", "No"]
    prompt = "Does %s have a valid front hook?"
    
    solution = None
    if is_correct:
        correct = ["Yes"]
        fronthook = None
        for a in solutions:
            if len(a.word) < 4:
                continue
            for b in solutions:
                if len(b.word) == len(a.word) + 1 and b.word[1:] == a.word:
                    solution = a
                    fronthook = b
                    break
            else:
                continue
            break
        
        if solution is not None:
            justification = ["Wrong! %s can be made from %s!" % (fronthook.word.upper(), solution.word.upper()), fronthook.path]
            correctExample = ["Correct! e.g. %s can be made from %s" % (fronthook.word.upper(), solution.word.upper()), fronthook.path]
        else:
            return None
    else:
        correct = ["No"]
        for a in solutions:
            if len(a.word) < 4:
                continue
            for b in solutions:
                if len(b.word) == len(a.word) + 1 and b.word[1:] == a.word:
                    break
            else:
                solution = a
                break
        
        if solution is not None:
            justification = "Wrong! %s has no front hook here!" % solution.word.upper()
            correctExample = []
        else:
            return None
        
    prompt = prompt % solution.word.upper()
    
    return Question(board, prompt, answers, correct, justification, correctExample) 
        
        
#Generate a "does this end with prefix" question
def generate_ends_with_suffix(board, solutions, dict):
    solution = random.choice(solutions)
    
    is_correct = MathService.get_random_boolean()
    answers = ["Yes", "No"]
    prompt = "Is there a word that ends with -%s?"
    
    if is_correct:
        maxIter = 100
        while maxIter > 0 and (len(solution.word) < 5 or solution.word[-3:] in dict):
            solution = random.choice(solutions)
            maxIter -= 1
            
        if maxIter == 0:
            return None
        
        correct = ["Yes"]
        suffix = solution.word[-3:]
        justification = ["Wrong! %s ends with -%s!" % (solution.word.upper(), suffix.upper()), solution.path]
        correctExample = ["Correct! e.g. " + solution.word.upper() + " ends in " + suffix.upper(), solution.path]
    else:
        suffix = board.get_random_word(3)
        maxIter = 100
        while maxIter > 0 and (not _is_cvc(suffix) or _suffix_in_solutions(solutions, suffix)):
            suffix = board.get_random_word(3)
            maxIter -= 1
            
        if maxIter == 0:
            return None
        
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
        maxIter = 100
        while maxIter > 0 and (len(solution.word) < 5 or solution.word[0:3] in dict):
            solution = random.choice(solutions)
            maxIter -= 1
        if maxIter == 0:
            return None
        correct = ["Yes"]
        prefix = solution.word[0:3]
        justification = ["Wrong! %s starts with %s-!" % (solution.word.upper(), prefix.upper()), solution.path]
        correctExample = ["Correct! e.g. " + solution.word.upper() + " begins with " + prefix.upper() + "-", solution.path]
    else:
        prefix = board.get_random_word(3)
        
        maxIter = 100
        while maxIter > 0 and (not _is_cvc(prefix) or _prefix_in_solutions(solutions, prefix)):
            suffix = board.get_random_word(3)
            maxIter -= 1
        if maxIter == 0:
            return None
            
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
        maxIter = 100
        while maxIter > 0 and len(solution.word) < 5:
            solution = random.choice(solutions)
            maxIter -= 1
        
        if maxIter == 0:
            return None
        
        justification = ["Wrong! \"%s\" is on this board!" % solution.word.upper(), solution.path]
        correctExample = ["Correct!", solution.path]
    else:  # Generate a question with "No" answer
        word = random.choice(dict);
        
        maxIter = 100
        while maxIter > 0 and (len(word) < 5 or StringService.get_similarity(word, board.letters) < 0.4):
            word = random.choice(dict);
            maxIter -= 1
        
        if maxIter == 0:
            return None
            
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

# Determines if a 3-letter word is a vowel sandwiched between consonants
def _is_cvc(word):
    if len(word) != 3:
        return False
    vowels = "aeiou"
    if word[0] not in vowels and word[1] in vowels and word[2] not in vowels:
        return True
    return False
    
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