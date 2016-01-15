from random import shuffle

answer_dic = {"Josh" : 1, "mall" : 2, "tricycle" : 3, "hot" : 4, "forty-two" : 5,
"cactus" : 6, "living room" : 7, "dogs" : 8, "aunt" : 9, "crestfallen" : 10, "baseball players" : 11}

problem = """(1) and I went shopping at the mall in a (2). We drove a (3) so we could get there fast! It was a (4) day to go shopping. We got (5) bargains! We bought a (6) to decorate the (7) with and (8) as a present for my (9). We also got some (10) (11) for the yard."""

options = answer_dic.keys()

def print_options():
    print_line(options, "")

def print_line(line, border):
    print border*len(line)
    print line
    print border*len(line)

def play_game():
    prompt = "Choose a word from the options to go in to the blank."
    print_line(prompt, "=")
    answer = problem
    while True:
        print_options()
        print answer
        print ""
        user_input = raw_input("Choose the number of blank to solve (to quit, type in 0): ")
        if user_input == "0" or int(user_input) >= len(answer_dic):
            break
        answer_input = raw_input("Type in the word for ("+user_input+"): ")
        if answer_input in answer_dic:
            if answer_dic[answer_input] == int(user_input):
                print_line("***** Correct! ******", "")
                # Replace question number in text with the answer
                answer = answer.replace("("+user_input+")", answer_input)
                # Remove answer from options
                options.remove(answer_input)
                # Go back to the beginning of the loop for another question
                continue
        print_line("** Incorrect answer.. Better luck next time.. **", "")
        
play_game()
