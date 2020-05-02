import json
import random
from collections import Counter

class Game:
    def __init__(self):
        self.word_file = open('wordlist.json')
        self.word_list = json.load(self.word_file)

        self.result = []
        self.guesses = []
        self.wrong_guesses = []
        self.guess_count = 0

        self.mode = "ai"
        self.word = random.choice(self.word_list)

        self.playing = True
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
            self.guess_count += 1
            self.check_end()

    def user_guess(self):
        # take user input to guess a letter
        validGuess = False
        while(not validGuess):
            validGuess = True

            info = "\nPrevious guesses: "
            for guess in self.wrong_guesses:
                info += guess + " "
            print(info)

            new_guess = input('Guess a Letter: ')[0].lower()

            # check if guess is a letter
            if not new_guess.isalpha():
                validGuess = False
            for g in self.guesses:
                if g == new_guess:
                    validGuess = False

            if not validGuess:
                print("\nInvalid guess, please try again.")

        # validate guess against the secret word
        self.guesses.append(new_guess)

        if new_guess in self.word:
            self.string = ""
            for i in range(len(self.word)):
                if self.word[i] == new_guess:
                    self.result[i] = new_guess
        else:
            self.wrong_guesses.append(new_guess)

    def ai_guess(self):
        checkstring = ""
        for word in self.possibles:
            for char in word:
                if char not in self.guesses:
                    checkstring += char

        all_guesses = Counter(checkstring).most_common()
        new_guess = all_guesses[0][0]
        print(all_guesses)

        self.guesses.append(new_guess)
        if new_guess in self.word:
            self.string = ""
            for i in range(len(self.word)):
                if self.word[i] == new_guess:
                    self.result[i] = new_guess
        else:
            self.wrong_guesses.append(new_guess)

    def check_end(self):
        if len(self.wrong_guesses) > 8:
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
                print("You guessed the word in ", self.guess_count, " tries!")
                print("The word was: ", self.word)
                self.playing = False

g = Game()
g.run()
