import random
import os

clear = lambda: os.system('clear')


# PLAYER MECHANICS


class Player():
	def __init__(self, game):
		self.game = game
		self.name = "Robo"
		self.turn = int()
		self.sign = ""

class Human(Player):
	
	def set_name(self):
		self.name = input("Your name: ")

	def play(self):

		print("Choose a slot to fill.")

		while self.turn == self.game.turn_manager.current_turn:

			choice = input()

			if choice in self.game.screen.slots and choice != "0" and choice != "X" and choice != "O":
				self.game.screen.slots[int(choice)] = self.sign
				self.game.next_turn()
				self.game.screen.display_screen()

			elif choice == "q" or choice == "Q":
				self.game.screen.down = self.game.screen.msgs["quit"]
				self.game.screen.display_screen()
				de = ""
				while de == "":
					dec = input()
					if dec == "y" or dec == "Y":
						clear()
						print("Good bye!")
						de = 1
						break
					elif dec == "n" or dec == "N":
						print("Alright let's continue! Choose a slot to fill.")
						de = 1
					else:
						print("Please type 'N' or 'Y'")
			else:
				print("Please choose a valid slot.")

class Bot(Player):

	def play(self):
	
		while self.turn == self.game.turn_manager.current_turn:

			choice = random.choice(self.game.screen.slots)

			if choice in self.game.screen.slots and choice != "0" and choice != "X" and choice != "O":
				self.game.screen.slots[int(choice)] = self.sign
				self.game.next_turn()
				self.game.screen.display_screen()
				break
			else:
				continue


# SCREEN AND BOARD


class Screen():
	def __init__(self, game):
		self.game = game
		self.slots = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
		self.msgs = {
			"win": "Congratulations! You beat me!",
			"lose": "I won!!",
			"quit": "Are you sure you want to quit? (Y/N)",
			"tie": "It's a tie! Wanna play again?"}
		self.down = "FILL"
		self.up = "FILL"

	def display_screen(self):
		self.up = "		--- TIC TAC TOE ---		\n"	
		clear()
		self.board = f"""
			 {self.slots[1]} | {self.slots[2]} | {self.slots[3]}
			 ---------
			 {self.slots[4]} | {self.slots[5]} | {self.slots[6]}
			 ---------
			 {self.slots[7]} | {self.slots[8]} | {self.slots[9]}
		\n"""
		display = f"""
{self.up}
{self.board}
{self.down}
		"""
		print(display)


# GAME MECHANICS


class TurnManager():
	def __init__(self, game):
		self.game = game
		self.current_turn = int()
		self.letters = ["x", "O"]
		self.turns = [0, 1]

	def choose_turns(self):
		self.game.pl1.turn = random.choice(self.turns)

		if self.game.pl1.turn == 0:
			self.game.pl1.sign = "X"
			self.game.pl2.sign = "O"
			self.game.pl2.turn = 1

		elif self.game.pl1.turn == 1:
			self.game.pl1.sign = "O"
			self.game.pl2.sign = "X"
			self.game.pl2.turn = 0
		
class Game():
	def __init__(self):
		self.screen = Screen(self)
		self.pl1 = Human(self)
		self.pl2 = Bot(self)
		self.turn_manager = TurnManager(self)
		self.win = False
		self.winner = None
	
	turn = 0

	def next_turn(self):
		if self.turn_manager.current_turn == 0:
			self.turn_manager.current_turn = 1
		elif self.turn_manager.current_turn == 1:
			self.turn_manager.current_turn = 0

	def check_win(self):
		b = self.screen.slots

		win_conditions = [
			[b[1], b[2], b[3]],
			[b[4], b[5], b[6]],
			[b[7], b[8], b[9]],
			[b[1], b[4], b[7]],
			[b[2], b[5], b[8]],
			[b[3], b[6], b[9]],
			[b[1], b[5], b[9]],
			[b[3], b[5], b[7]]
		]

		for condition in win_conditions:
			if condition[0] == condition[1] == condition[2]:
				self.win = True

				if self.turn_manager.current_turn == self.pl1.turn:
					self.winner = self.pl2
				elif self.turn_manager.current_turn == self.pl2.turn:
					self.winner = self.pl1
					
				self.screen.display_screen()

		sl = self.screen.slots
		if "1" not in sl and "2" not in sl and "3" not in sl and "4" not in sl and "5" not in sl and "6" not in sl and "7" not in sl and "8" not in sl and "9" not in sl:
			self.win = True
			self.winner = None

	def greet(self):
		print("Welcome, player! What would you like me to call you?")
		self.pl1.set_name()
		print("Let's start, then {}! (Press enter to continue)".format(self.pl1.name))

	def play(self):
		self.greet()
		input()
		
		self.turn_manager.choose_turns()
		
		turn = Game.turn

		while self.win == False:

			turn += 1

			self.screen.down = f"{self.pl1.name}: {self.pl1.sign} - {self.pl2.name}: {self.pl2.sign}\nRound {int(turn/2)}"

			if self.turn_manager.current_turn == self.pl1.turn:			

				self.screen.display_screen()
				self.pl1.play()

			elif self.turn_manager.current_turn == self.pl2.turn:			

				self.screen.display_screen()
				self.pl2.play()

			self.check_win()

		if self.winner == self.pl1:
			self.screen.down = self.screen.msgs["win"]
			self.screen.display_screen()
		elif self.winner == self.pl2:
			self.screen.down = self.screen.msgs["lose"]
			self.screen.display_screen()
		elif self.winner == None:
			self.screen.down = self.screen.msgs["tie"]			
			self.screen.display_screen()

		
# THE GAME


game = Game()
game.play()