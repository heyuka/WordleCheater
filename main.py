from cheater import Cheater
from gameview import GameView
from menuView import main_menu

filename = "wordlist_old.csv"
cheater = Cheater(filename)
main_menu(cheater)
GameView(filename).initial_prompt()

