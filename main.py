from cheater import Cheater
from gameview import GameView
from menuView import main_menu

filename = "wordlist.txt"
cheater = Cheater(filename)
main_menu(cheater)
GameView(filename).initial_prompt()

