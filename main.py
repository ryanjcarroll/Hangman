import json
import random
from collections import Counter

NUM_GUESSES = 100

class Game:
    def __init__(self):
        self.word_file = open('wordlist.json')
        self.word_list = json.load(self.word_file)

        self.result = []
        self.guesses = []
        self.wrong_guesses = []
        self.correct_guesses = []
        self.guess_count = 0

        self.mode = "ai"
        self.last_was_correct = False
        self.word = random.choice(self.word_list)

        self.playing = True
        self.firstGuess = True
        self.get_word()

    def get_word(self):
        for x in range(len(self.word)):
            self.result.append("_")

        if self.mode == "ai":
            self.possibles = []  # array of possible words

        for word in self.word_list:
            if len(word) == len(self.result):
                self.possibles.append(word)
        print(self.possibles)

    def print(self):
        output = ""
        for c in self.result:
            output += c + " "
        print(output)

    def run(self):
        while(self.playing):
            self.print()
            if(self.mode == "user"):
                self.user_guess()
            elif(self.mode == "ai"):
                self.ai_guess()
            self.end_guess()
            self.guess_count += 1
            self.check_game_over()

    def user_guess(self):
        # take user input to guess a letter
        validGuess = False
        while(not validGuess):
            validGuess = True

            info = "\nPrevious guesses: "
            for guess in self.wrong_guesses:
                info += guess + " "
            print(info)

            self.new_guess = input('Guess a Letter: ')[0].lower()

            # check if guess is a letter
            if not self.new_guess.isalpha():
                validGuess = False
            for g in self.guesses:
                if g == self.new_guess:
                    validGuess = False

            if not validGuess:
                print("\nInvalid guess, please try again.")

    def ai_guess(self):
        # eliminate words that were made invalid by the last letter guessed, if the last guess was correct
        if self.last_was_correct:
            last_correct = self.correct_guesses[len(self.correct_guesses) - 1]  #last correctly guessed letter
            last_correct_positions = []     # lists the positions of the last correctly guessed letter
            for i in range(len(self.result)):
                if self.result[i] == last_correct:
                    last_correct_positions.append(i)

            print(last_correct)
            print(last_correct_positions)

            new_possibles = self.possibles.copy()
            for word in self.possibles:
                for pos in last_correct_positions:
                    if not word[pos] == last_correct:
                        print("Removing...", word)
                        new_possibles.remove(word)
                        break
                    print("Keeping...", word)

            self.possibles = new_possibles

        # find most common letter among remaining possible words
        checkstring = ""
        for word in self.possibles:
            for char in word:
                if char not in self.guesses:
                    checkstring += char

        all_guesses = Counter(checkstring).most_common()
        print(all_guesses)
        self.new_guess = all_guesses[0][0]
        print(self.new_guess)

    def end_guess(self):
        self.guesses.append(self.new_guess)
        if self.new_guess in self.word:
            self.correct_guesses.append(self.new_guess)
            self.last_was_correct = True
            for i in range(len(self.word)):
                if self.word[i] == self.new_guess:
                    self.result[i] = self.new_guess
        else:
            self.last_was_correct = False
            self.wrong_guesses.append(self.new_guess)
    
    def check_game_over(self):
        global NUM_GUESSES
        if len(self.wrong_guesses) > NUM_GUESSES:
            print("GAME OVER: Out of guesses")
            print("The word was: ", self.word)
            self.playing = False
        else:
            done = True
            for x in self.result:
                if x == "_":
                    done = False
            if done:
                print("GAME OVER: You Win!")
                print("You guessed the word in ", self.guess_count, " tries with ", len(self.wrong_guesses), " wrong guesses!")
                print("The word was: ", self.word)
                self.playing = False

g = Game()
g.run()
