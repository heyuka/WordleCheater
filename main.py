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

# scores = [0] * len(word_array)
# for i in range(len(word_array)):
#     word = word_array[i]
#     for letter in word:
#         scores[i] += counts[ord(letter) - 65]

counts_by_position = np.zeros((26, 5))
for word in word_array:
    for position, letter in enumerate(word):
        counts_by_position[ord(letter) - 65][position] += 1

medians = np.median(counts_by_position, axis=0)

scores_by_pos = np.zeros((26, 5))
for i in range(len(scores_by_pos)):
    for j in range(len(scores_by_pos[i])):
        scores_by_pos[i][j] = counts_by_position[i][j] / medians[j]

scores = np.zeros(len(word_array))
for i in range(len(word_array)):
    word = word_array[i]
    for position, letter in enumerate(word):
        scores[i] += scores_by_pos[ord(letter) - 65][position]


def get_candidates(_words, _scores):
    num_words = 10
    if len(_words) < 10:
        num_words = (len(_words))
    indices = np.argpartition(_scores, (num_words * -1))[(num_words * -1):]
    ew = np.zeros((num_words, 2))
    for index in range(num_words):
        ew[index][0] = indices[index]
        ew[index][1] = _scores[index]
    ew = np.msort(ew)
    for index in range(num_words):
        indices[index] = ew[index][0]
    top5 = _words[indices]
    return top5[::-1]


def get_clean_candidates():
    global word_array
    doomed = []
    for _word in word_array:
        for _letter in _word:
            if _word.count(_letter) > 1:
                doomed.append(np.where(word_array == _word))
                break
    _words = np.delete(word_array, doomed)
    _scores = np.delete(scores, doomed)
    return get_candidates(_words, _scores)


def print_status():
    global scores
    print(str(len(word_array)) + " possible words remain")
    print("Most likely words: " + str(get_candidates(word_array, scores)))
    print("Most likely words without duplicates: " +
          str(get_clean_candidates()))


def rule_out_letter(_letter):
    global word_array, scores
    doomed = []
    for _word in word_array:
        if _word.count(_letter) > 0:
            doomed.append(np.where(word_array == _word))
    word_array = np.delete(word_array, doomed)
    scores = np.delete(scores, doomed)


def require_letter(_letter):
    global word_array, scores
    doomed = []
    for _word in word_array:
        if _word.count(_letter) == 0:
            doomed.append(np.where(word_array == _word))
    word_array = np.delete(word_array, doomed)
    scores = np.delete(scores, doomed)


def rule_out_letter_at_position(_letter, _position):
    global word_array, scores
    doomed = []
    for _word in word_array:
        if _word[_position] == _letter:
            doomed.append(np.where(word_array == _word))
    word_array = np.delete(word_array, doomed)
    scores = np.delete(scores, doomed)


def require_letter_at_position(_letter, _position):
    global word_array, scores
    doomed = []
    for _word in word_array:
        if _word[_position] != _letter:
            doomed.append(np.where(word_array == _word))
    word_array = np.delete(word_array, doomed)
    scores = np.delete(scores, doomed)


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
                  f'  1 - Grey Boxes  \n' \
                  f'  2 - Yellow Boxes  \n' \
                  f'  3 - Green Boxes  \n' \
                  f'>> '
    print_status()
    user_input = input(main_prompt)

    if user_input == "0":
        quit()
    elif user_input == "1":
        menu_grey_boxes()
    elif user_input == "2":
        menu_yellow_boxes()
    elif user_input == "3":
        menu_green_boxes()
    else:
        print("Invalid entry; please try again.")
        main_menu()


def menu_grey_boxes():
    msg = "Enter grey-boxed letter (blank to cancel): "
    user_input = clean_input_letter(msg)

    if user_input > -1:
        rule_out_letter(chr(user_input))
        menu_grey_boxes()

    print("Returning to main menu")
    main_menu()


def menu_green_boxes():
    msg = "Enter green-boxed letter (blank to cancel): "
    user_letter = clean_input_letter(msg)

    if user_letter != -1:
        msg = "Enter position number (1 through 5): "
        user_position = clean_input_number(msg)
    else:
        user_position = -1

    if user_letter > -1 and user_position > -1:
        require_letter_at_position(chr(user_letter),
                                   int(chr(user_position)) - 1)
        menu_green_boxes()

    print("Returning to main menu")
    main_menu()


def menu_yellow_boxes():
    msg = "Enter yellow-boxed letter (blank to cancel): "
    user_letter = clean_input_letter(msg)

    if user_letter != -1:
        msg = "Enter yellow box position (1 through 5): "
        user_position = clean_input_number(msg)
    else:
        user_position = -1

    if user_letter > -1 and user_position > -1:
        require_letter(chr(user_letter))

        rule_out_letter_at_position(chr(user_letter),
                                    int(chr(user_position)) - 1)
        menu_yellow_boxes()

    print("Returning to main menu")
    main_menu()


def clean_input_letter(prompt):
    user_input = input(prompt)

    if len(user_input) > 1:
        print("Please enter only one letter at a time.")
        clean_input_letter(prompt)
    elif len(user_input) < 1:
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
