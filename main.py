import numpy as np

from CSVToList import CSVToList

# bring in the wordlist for us to play with. I'm re-using the CSVToList file
# which returns the csv as a list of strings, so I'll immediately turn it into a
# numpy array to make some of the later calculations easier
word_list_file = "wordlist.csv"
word_list = CSVToList(word_list_file).list
word_array = np.array(word_list)

# counts holds the number of times each letter is used in the whole of the
# master data set, and scores holds the sum of the scores for each of the five
# letters in the word. We create these arrays once and leave them be, because
# the overall probability shouldn't change throughout the process
counts = [0] * 26
for word in word_array:
    for letter in word:
        counts[ord(letter) - 65] += 1

scores = [0] * len(word_array)
for i in range(len(word_array)):
    word = word_array[i]
    for letter in word:
        scores[i] += counts[ord(letter) - 65]


def find_top5(_words, _scores):
    global word_array
    num_to_return = -5
    if len(_words) < 5:
        num_to_return = (len(_words)) * -1
    indices = np.argpartition(_scores, num_to_return)[num_to_return:]
    top5 = _words[indices]
    return top5


def find_top5_without_duplicates():
    global word_array
    doomed = []
    for _word in word_array:
        for _letter in _word:
            if _word.count(_letter) > 1:
                doomed.append(np.where(word_array == _word))
                break
    _words = np.delete(word_array, doomed)
    _scores = np.delete(scores, doomed)
    ret = find_top5(_words, _scores)
    return ret


def print_status():
    global scores
    print(str(len(word_array)) + " possible words remain")
    print("Most likely words: " + str(find_top5(word_array, scores)))
    print("Most likely words without duplicates: " +
          str(find_top5_without_duplicates()))


def rule_out_letter(_letter):
    print(f"Ruling out letter {_letter}...")
    global word_array, scores
    doomed = []
    for _word in word_array:
        if _word.count(_letter) > 0:
            doomed.append(np.where(word_array == _word))
    word_array = np.delete(word_array, doomed)
    scores = np.delete(scores, doomed)
    print_status()


def require_letter(_letter):
    print(f"Require letter {_letter}...")
    global word_array, scores
    doomed = []
    for _word in word_array:
        if _word.count(_letter) == 0:
            doomed.append(np.where(word_array == _word))
    word_array = np.delete(word_array, doomed)
    scores = np.delete(scores, doomed)
    print_status()


def rule_out_letter_at_position(_letter, _position):
    print(f"Rule out letter {_letter} at position {_position}...")
    global word_array, scores
    doomed = []
    for _word in word_array:
        if _word[_position] == _letter:
            doomed.append(np.where(word_array == _word))
    word_array = np.delete(word_array, doomed)
    scores = np.delete(scores, doomed)
    print_status()


def require_letter_at_position(_letter, _position):
    print(f"Require letter {_letter} at position {_position}...")
    global word_array, scores
    doomed = []
    for _word in word_array:
        if _word[_position] != _letter:
            doomed.append(np.where(word_array == _word))
    word_array = np.delete(word_array, doomed)
    scores = np.delete(scores, doomed)
    print_status()


def main_menu():
    """Take the user's input and direct them to the appropriate submenu.

    The main menu for the user interface. Takes the user's input and throws them
    to the appropriate submenu. If the user makes an unrecognizable entry, ask
    them to try again. When the user's done, terminate the program.

    :return: None
    """
    main_prompt = f'Enter a number below to make a selection from ' \
                  f'the following options:  \n' \
                  f'  0 - Quit  \n' \
                  f'  1 - Rule out letter  \n' \
                  f'  2 - Require letter  \n' \
                  f'  3 - Rule out letter at position  \n' \
                  f'  4 - Require letter at position  \n' \
                  f'>> '
    print_status()
    user_input = input(main_prompt)

    if user_input == "0":
        quit()
    elif user_input == "1":
        menu_rule_out_letter()
    elif user_input == "2":
        menu_require_letter()
    elif user_input == "3":
        menu_rule_out_letter_at_position()
    elif user_input == "4":
        menu_require_letter_at_position()
    else:
        print("Invalid entry; please try again.")
        main_menu()


def menu_rule_out_letter():
    print("Rule out letter sub-menu")
    msg = "Enter letter to rule out (blank to cancel): "
    user_input = clean_input_letter(msg)

    if user_input > -1:
        rule_out_letter(chr(user_input))
        menu_rule_out_letter()

    print("Returning to main menu")
    main_menu()


def menu_require_letter():
    print("Require letter sub-menu")
    msg = "Enter letter to require (blank to cancel): "
    user_input = clean_input_letter(msg)

    if user_input > -1:
        require_letter(chr(user_input))
        menu_require_letter()

    print("Returning to main menu")
    main_menu()


def menu_require_letter_at_position():
    print("Require letter at position sub-menu")

    msg = "Enter letter to require (blank to cancel): "
    user_letter = clean_input_letter(msg)

    msg = "Enter position number (1 through 5): "
    user_position = clean_input_number(msg)

    if user_letter > -1 and user_position > -1:
        require_letter_at_position(chr(user_letter), int(chr(user_position)) - 1)
        menu_require_letter_at_position()

    print("Returning to main menu")
    main_menu()


def menu_rule_out_letter_at_position():
    print("Rule out letter at position sub-menu")

    msg = "Enter letter to rule (blank to cancel): "
    user_letter = clean_input_letter(msg)

    msg = "Enter position number (1 through 5): "
    user_position = clean_input_number(msg)

    if user_letter > -1 and user_position > -1:
        rule_out_letter_at_position(chr(user_letter), int(chr(user_position)) - 1)
        menu_rule_out_letter_at_position()

    print("Returning to main menu")
    main_menu()


def clean_input_letter(prompt):
    user_input = input(prompt)

    if len(user_input) > 1:
        print("Please enter only one letter at a time.")
        clean_input_letter(prompt)
    elif len(user_input) < 1:
        print("Returning to parent menu.")
        return -1

    user_input = user_input.upper()
    user_input = ord(user_input)

    if 64 < user_input < 91:
        return user_input
    else:
        print("Invalid entry. Please try again.")
        clean_input_letter(prompt)


def clean_input_number(prompt):
    user_input = input(prompt)

    if len(user_input) > 1:
        print("Please enter only one number at a time.")
        clean_input_letter(prompt)
    elif len(user_input) < 1:
        print("Returning to parent menu.")
        return -1

    user_input = user_input.upper()
    user_input = ord(user_input)

    if 48 < user_input < 54:
        return user_input
    else:
        print("Invalid entry. Please try again.")
        clean_input_letter(prompt)


# print_status()
# rule_out_letter("E")
# require_letter("V")
# require_letter_at_position("V", 3)
# require_letter_at_position("A", 2)

main_menu()
