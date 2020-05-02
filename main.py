import json
import random
from collections import Counter

NUM_GUESSES = 100
NUM_ITERATIONS = 10000

class Game:
    def __init__(self):
        self.word_file = open('wordlist.json')
        self.word_list = json.load(self.word_file)

        self.result = []
        self.guesses = []
        self.wrong_guesses = []
        self.correct_guesses = []
        self.possibles = []
        self.guess_count = 0

        self.mode = "ai"
        self.print = False   # set to true to enable print statements. Best for user mode, small # of iterations, and debugging
        self.last_was_correct = False
        self.word = random.choice(self.word_list)

        self.playing = True
        self.firstGuess = True
        self.get_word()

    def get_word(self):
        for x in range(len(self.word)):
            self.result.append("_")

        for word in self.word_list:
            if len(word) == len(self.result):
                self.possibles.append(word)

        if self.mode == "ai":
            if self.print:
                print(len(self.possibles), " words remaining")

    def print(self):
        output = ""
        for c in self.result:
            output += c + " "
        print("\n",output,"\n")

    def run(self):
        while self.playing:
            if self.print:
                self.print()
            if(self.mode == "user"):
                self.user_guess()
            elif(self.mode == "ai"):
                self.ai_guess()
            self.end_guess()
            self.guess_count += 1
            self.check_game_over()

        return self.return_results()

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
            last_correct = self.correct_guesses[len(self.correct_guesses) - 1]  # last correctly guessed letter
            last_correct_positions = []     # lists the positions of the last correctly guessed letter
            for i in range(len(self.result)):
                if self.result[i] == last_correct:
                    last_correct_positions.append(i)

            new_possibles = []
            for word in self.possibles:
                keepWord = True
                for pos in last_correct_positions:
                    if not word[pos] == last_correct:
                        keepWord = False

                if keepWord:
                    if self.print:
                        print("Keeping...", word)
                    new_possibles.append(word)
                else:
                    if self.print:
                        print("Removing...", word)

            self.possibles = new_possibles
            if self.print:
                print(len(self.possibles), " words remaining")
        # if the last guess was incorrect, remove all words which contained that letter
        elif len(self.wrong_guesses) > 0:
            last_wrong = self.wrong_guesses[len(self.wrong_guesses) - 1]  # last correctly guessed letter
            new_possibles = []
            for word in self.possibles:
                keepWord = True
                for char in word:
                    if char == last_wrong:
                        keepWord = False
                if keepWord:
                    if self.print:
                        print("Keeping...", word)
                    new_possibles.append(word)
                else:
                    if self.print:
                        print("Removing...", word)

            self.possibles = new_possibles
            if self.print:
                print(len(self.possibles), " words remaining")

        # find most common letter among remaining possible words
        checkstring = ""
        for word in self.possibles:
            for char in word:
                if char not in self.guesses:
                    checkstring += char

        all_guesses = Counter(checkstring).most_common()
        if self.print:
            print(all_guesses)
        self.new_guess = all_guesses[0][0]
        if self.print:
            print("Guessing:", self.new_guess)

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
            if self.print:
                print("\nGAME OVER: Out of guesses")
                print("The word was: ", self.word)
            self.playing = False
        else:
            done = True
            for x in self.result:
                if x == "_":
                    done = False
            if done:
                if self.print:
                    print("\nGAME OVER: You Win!")
                    print("You guessed the word in ", self.guess_count, " tries with ", len(self.wrong_guesses), " wrong guesses!")
                    print("The word was: ", self.word)
                self.playing = False

    def return_results(self):
        return self.word, self.guesses, self.correct_guesses, self.wrong_guesses


count = 0
all_results = []
while count < NUM_ITERATIONS:
    count += 1
    g = Game()
    result = g.run()
    all_results.append(result)

total_guesses = 0
total_correct = 0
total_incorrect = 0
for result in all_results:
    total_guesses += len(result[1])
    total_correct += len(result[2])
    total_incorrect += len(result[3])

print("Total guesses: ", total_guesses)
print("Total correct: ",  total_correct)
print("Total incorrect:", total_incorrect)
print("Average guesses: ", total_guesses / NUM_ITERATIONS)
print("Average correct: ",  total_correct / NUM_ITERATIONS)
print("Average incorrect:", total_incorrect / NUM_ITERATIONS)