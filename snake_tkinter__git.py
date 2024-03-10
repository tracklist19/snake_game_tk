## Python Snake Game : from the Bro Code tutorial at https://www.youtube.com/watch?v=bfRwxS5d0SI


from tkinter import * 
import random 


### CONSTANTS ##########################################################

GAME_WIDTH = 720
GAME_HEIGHT = 560
SPEED = 90
SPACE_SIZE = 40
BODY_PARTS = 3
SNAKE_COLOR = "#006600"
FOOD_COLOR = "#ff6666"
BACKGROUND_COLOR = "#310225"


### CLASSES and FUNCTIONS ##############################################

class Snake:
	
	def __init__(self): 
		self.body_size = BODY_PARTS
		self.coordinates = [] 											# list of square coordinates
		self.squares = [] 												# list of square graphics on canvas
		
		# Creating a List of Coordinates 
		for i in range(0, BODY_PARTS):
			self.coordinates.append([0, 0])
	
		# Creating Squares 
		for x, y in self.coordinates: 
			square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
			self.squares.append(square)

		print('SNAKE')


class Food:
	
	def __init__(self):
		
		# Placing Food-object randomly 
			# Picking a random position[x,y] within the game-canvas-measures			# randint() chooses randomly from the total number of possible SPACE_SIZEs (times the SPACE_SIZE to get a WIDTH/HEIGHT that is a multiple of the Food-size)
		x = random.randint(0, (GAME_WIDTH/SPACE_SIZE)-1) * SPACE_SIZE
		y = random.randint(0, (GAME_HEIGHT/SPACE_SIZE)-1) * SPACE_SIZE
		
			# Setting the coordinates
		self.coordinates = [x, y] 

			# Drawing the Food-object on the canvas 
		canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

		print('FOOD')


def next_turn(snake, food):
	
	# Unpacking the head of the snake 
	x, y = snake.coordinates[0]
	
	# Updating the set of coordinates for the head of the snake (new/next location)
	if direction == 'up': 
		y = y - SPACE_SIZE
	elif direction == 'down': 
		y = y + SPACE_SIZE
	elif direction == 'left': 
		x = x - SPACE_SIZE
	elif direction == 'right': 
		x = x + SPACE_SIZE
	
	# Inserting the updated coordinates for the new head of the snake 
	snake.coordinates.insert(0, (x, y))
	
	# New Graphic for the head of the snake 
	square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR) 
	
	# Update Snake's List of squares
	snake.squares.insert(0, square)

	# Eating the Apple
	if x == food.coordinates[0] and y == food.coordinates[1]:
		global score
		score += 1
		label.config(text="Score:{}".format(score))
		canvas.delete("food")											# Delete the food-Object from the GameCanvas (per "food"-tag)
		food = Food()													# Create a new food-Object
	else:																# Only Delete the last body part of our snake if it didn't eat a food object
	# Delete last BodyPart of our Snake									# Simulates the movement of the snake (part2)
		del snake.coordinates[-1]
		canvas.delete(snake.squares[-1])
		del snake.squares[-1]
	
	# Check for collisions
	if check_collisions(snake):
		game_over()
	else:
	# Moving on to the next turn 
		window.after(SPEED, next_turn, snake, food) 					# Updating the game-window (after the time SPEED) and Calling next_turn(), passing on its arguments 
	
	
def change_direction(new_direction):
	
	global direction													# accessing the old direction
	
	if new_direction == 'left':
		if direction != 'right':										# old direction must not be 180° of the new (rules of the game)
			direction = new_direction
	if new_direction == 'right':	
		if direction != 'left': 
			direction = new_direction 
	if new_direction == 'up':	
		if direction != 'down': 
			direction = new_direction 
	if new_direction == 'down':	
		if direction != 'up': 
			direction = new_direction 
			

def check_collisions(snake):
	
	x, y = snake.coordinates[0]											# unpack the head of the snake
	
	# Check if left/right/top/bottom border of the game is crossed
	if x < 0 or x >= GAME_WIDTH:
		print('GAME OVER')
		return True
	elif y < 0 or y >= GAME_HEIGHT:
		print('GAME OVER')
		return True
	# Check if snake is crossing itself
	for body_part in snake.coordinates[1:]:								# anything after the head of the snake (because it cant run into itself)
		if x == body_part[0] and y == body_part[1]:						# Are head- and snake-coordinates overlapping?
			print('GAME OVER')
			return True
			
	return False
	
	
def game_over():
	canvas.create_text(canvas.winfo_width()/4, canvas.winfo_height()/4,
						font=('consolas', 25), text="GAME OVER", fill='red', tag="gameover")


### GAME WINDOW ########################################################

window = Tk() 
window.title("Snake")
window.resizable(False, False)					 						# window not resizable 


score = 0 
direction = 'down'														# starting-direction of the snake

label = Label(window, text="Score:{}".format(score), font=('consolas', 13))
label.pack()					 										# wraps up the label 

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack() 															# wraps up the canvas 

## Centering the game window on the screen
window.update()															# updating the window so that it renders

	# window dimensions
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

	# Check for how much to adjust the window position 					# centering the outlines of the windows through subtraction of half lengths
x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

	# Setting the geometry / Moving the window  
window.geometry(f"{window_width}x{window_height}+{x}+{y}")				# x,y : starting point of the window


## Binding Keys : Controls
window.bind('<Left>', lambda event: change_direction('left'))			# argument is an event : calling change_direction(), passing in'left' for the variable new_direction
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))


## Snake object & Food object
snake = Snake()
food = Food()


## Calling the next_turn()-Function										# initial call at the start of the game (to get the Snake()-class-object moving)
next_turn(snake, food) 


window.mainloop()														# enters the Tkinter-eventLoop

