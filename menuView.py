def main_menu(ch):
    main_prompt = f'Enter a number below to make a selection from ' \
                  f'the following options:  \n' \
                  f'  0 - Quit  \n' \
                  f'  1 - Grey Boxes  \n' \
                  f'  2 - Yellow Boxes  \n' \
                  f'  3 - Green Boxes  \n' \
                  f'>> '
    ch.print_status()
    user_input = input(main_prompt)

    if user_input == "0":
        quit()
    elif user_input == "1":
        menu_grey_boxes(ch)
    elif user_input == "2":
        menu_yellow_boxes(ch)
    elif user_input == "3":
        menu_green_boxes(ch)
    else:
        print("Invalid entry; please try again.")
        main_menu(ch)


def menu_grey_boxes(ch):
    msg = "Enter grey-boxed letter (blank to cancel): "
    user_input = clean_input_letter(msg)

    if user_input > -1:
        ch.rule_out_letter(chr(user_input))
        menu_grey_boxes(ch)

    print("Returning to main menu")
    main_menu(ch)


def menu_green_boxes(ch):
    msg = "Enter green-boxed letter (blank to cancel): "
    user_letter = clean_input_letter(msg)

    if user_letter != -1:
        msg = "Enter position number (1 through 5): "
        user_position = clean_input_number(msg)
    else:
        user_position = -1

    if user_letter > -1 and user_position > -1:
        ch.require_letter_at_position(chr(user_letter),
                                      int(chr(user_position)) - 1)
        menu_green_boxes(ch)

    print("Returning to main menu")
    main_menu(ch)


def menu_yellow_boxes(ch):
    msg = "Enter yellow-boxed letter (blank to cancel): "
    user_letter = clean_input_letter(msg)

    if user_letter != -1:
        msg = "Enter yellow box position (1 through 5): "
        user_position = clean_input_number(msg)
    else:
        user_position = -1

    if user_letter > -1 and user_position > -1:
        ch.require_letter(chr(user_letter))

        ch.rule_out_letter_at_position(chr(user_letter),
                                       int(chr(user_position)) - 1)
        menu_yellow_boxes(ch)

    print("Returning to main menu")
    main_menu(ch)


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
