import pygame
import sys

#Command Line options
#First argv[1] is game board width in pixels. 300 is default
#tSecond argv[2] is game board height in pixels. 300 is default
#the .py file is consider an arg in len(sys.argv)
#Check if there is a first argument passed in

'''Open with 800 640 after .py script'''

	
if len(sys.argv) > 1:
	if 50 <= int(sys.argv[1]) <= 1200:
		width = int(sys.argv[1])
	else:
		width = 300
else:
	width = 300
print("width:", width)

if len(sys.argv) > 2:
	if 50 <= int(sys.argv[2]) <= 1200:
		height = int(sys.argv[2])
	else:
		height = 300
else:
	height = 300
print("height:", height)

	
# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
CUST_COL = ( 0, 200, 50)
GREY     = ( 200, 200, 200)

#This defines the height and the width of the displayed screen
#width = 300
#height = 300

 

 
# Set row 1, cell 5 to one. (Remember rows and
# column numbers start at zero.)
#grid[1][5] = 1
 
# Initialize pygame
pygame.init()
 
# Set the height and width of the screen
size = [width, height]
screen = pygame.display.set_mode(size)
#screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
 
# Set title of screen
pygame.display.set_caption("Title")
 

 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# This sets the margin between each cell
margin = 5
'''Number of cells per page'''
#This is the number of cells to be displayed (vertically)
cell_num = 5

#Cell height and width calculated by taking total width or height of the screen and subtracting all the margins
#(each side has margin as well as between each cell) and dividing by the number of cells on each axis
#Also store width and height of side bar
bar_width = 100
bar_height = screen.get_height()-2*margin
cell_width  = int((screen.get_width()-(margin*2))) - (bar_width*2)
cell_height = int((screen.get_height()-(margin*(cell_num+1)))/cell_num)

#Height and width of the pop up window. This is th color of the black box that pops up over
#the main screen for settings and currently selected drinks
pop_up_width = int(screen.get_width()*0.9)
pop_up_height = int(screen.get_height()*0.9)

# Create a list with cocktail names
'''Test drink list'''#drinks = ["Jack & Coke", "Rum and Coke", "Long Island Iced Tea", "Coke", "Woo-Woo", "SHOTS!!!!!", "Bloody Mary", "Mimosa", "Beer", "Don't Show"]
##drinks = ["Item 1", "Item Two", "Item-o three-o", "Item 4", "Items 5s", "Item 6", "Item 7"]
font = pygame.font.Font(None, 50) #36 default

#Function that opens a text file in the same directory as the .py file and reads in the data about drinks
#Returns a dictionary where the drinks are the key and the recipe is the value
def build_drink_dict():
	drink_dict_temp = {}
	with open("drink_recipes.txt") as recipes:
		#Iterate though file line by line
		for i in recipes.readlines():
			split = i.split(",")
			#print(split)
			drink_name = split[0]
			split = split[1:]
			#List of tuples that are the [ingredient,percent]
			drink_recipe = []
			#Iterate through list of ingredients and create recipe list of tuples
			for i in split:
				#Ingredients will be in this order:
				#(Percent of drink) (name of ingredient) Example:50 Rum,50 Coke
				#Get percent of drink by splitting at spaces
				percent_temp = i.split(" ")[0]
				#Get length of percent identifier, add one for the space after the number
				#This will be where the name of the ingredient starts
				ingredient_temp = i[len(percent_temp):].replace("\n", "")
				#Add tuple to recipe list
				drink_recipe.append([ingredient_temp,percent_temp])
			#Add entry to dictionary
			drink_dict_temp[drink_name] = drink_recipe
	return drink_dict_temp


#Function to get eligible drinks to make, returns list of lists, where each sublist has cell_num number of items
def get_drink_list(drink_dict):
	drinks = []
	for key in drink_dict:
		drinks.append(key)
	#Reverse list so that it is in original order
	drinks = list(reversed(drinks))
	#List of available drinks
	drinks_avail = []
	done = False
	num_drinks_avail = len(drinks)
	#Keep track of where we are in list
	cur_drink = 0
	while cur_drink < num_drinks_avail:#not done:
		#Try to create sublist of 5
		sublist = []
		for i in range(5):
			try:
				sublist.append(drinks[cur_drink])
				#sublist.append(next(drinks_iter))
			except:
				sublist.append(" ")
				done = True
			cur_drink += 1
		#print(sublist)
		drinks_avail.append(sublist)

	return drinks_avail

#Get dict of drinks
drink_dict = build_drink_dict()
#Get list of drinks from dict
drink_list = get_drink_list(drink_dict)

def open_drink(surface, drink):
	pop_up_x = surface.get_width()*0.05
	pop_up_y = surface.get_height()*0.05
	#Draw black box over screen
	pygame.draw.rect(surface, BLACK,
		[pop_up_x,
		pop_up_y,
		pop_up_width,
		pop_up_height])
	#Draw white box to display info
	pygame.draw.rect(surface, WHITE,
					[pop_up_x+margin,
					pop_up_y+margin,
					pop_up_width*0.7-margin,
					pop_up_height*0.7-margin])
	#Draw Pour button
	pygame.draw.rect(surface, WHITE,
					[pop_up_x+margin+(pop_up_width*0.7),
					pop_up_y+margin,
					pop_up_width*0.3-(margin*2),
					pop_up_height*0.6-margin])
	#Draw Done button
	pygame.draw.rect(surface, WHITE,
					[pop_up_x+margin+(pop_up_width*0.7),
					pop_up_y+margin+(pop_up_height*0.6),
					pop_up_width*0.3-(margin*2),
					pop_up_height*0.4-(margin*2)])

	'''Draw size buttons'''
	#Whichever size button is currently selected will have a different background
	#Color of the buttons for size selection
	global size_buttons
	size_buttons = [WHITE, CUST_COL, WHITE]
	'''
	#Background color of 1.5 oz button
	button_15_color = WHITE
	#Background color of 3 oz button
	button_30_color = CUST_COL
	#Background color of 4.5 oz button
	button_45_color = WHITE
	'''
	#Draw 1.5 oz button
	pygame.draw.rect(surface, size_buttons[0],
					[pop_up_x+margin,
					pop_up_y+margin+(pop_up_height*0.7),
					pop_up_width*(0.7/3)-margin,
					pop_up_height*0.3-(margin*2)])
	#Draw 3.0 oz button
	pygame.draw.rect(surface, size_buttons[1],
						[pop_up_x+margin+(pop_up_width*(0.7/3)),
						pop_up_y+margin+(pop_up_height*0.7),
						pop_up_width*(0.7/3)-margin,
						pop_up_height*0.3-(margin*2)])
	#Draw 4.5 oz button (Use rest of width to the sise button for width on this button)
	pygame.draw.rect(surface, size_buttons[2],
					[pop_up_x+margin+(pop_up_width*(0.7/3*2)),
					pop_up_y+margin+(pop_up_height*0.7),
					(pop_up_width*(0.7)-margin)-(pop_up_width*(0.7/3*2)),
					pop_up_height*0.3-(margin*2)])
	'''Draw text'''
	text = font.render(drink, True, BLACK)
	#Length of text, height of text (in pixels)
	text_size = font.size(drink)
	#Center text horizontally
	text_x = pop_up_x + margin + (pop_up_width*0.01)
	#Center text vertically
	#Calculate height of cells * row, account for margin, then center in cell. -2 to account for text starting after 2 pixels
	##text_y = (cell_height*row) + (margin*(row+1)) + ((cell_height-text_size[1])/2) - 2
	text_y = pop_up_y + margin + (pop_up_height*0.01)
	#Coordinates are top left of text box, text is actually 2 pixels down and right from coordinates
	#text, [dist from left edge, dist from top edge]
	screen.blit(text, [text_x, text_y])

#Handle clicks for drink pop up menu
##def open_drink_click()

#Loop until the user clicks the close button.
done = False
#Which page of the drink menu the user is on
drink_page = 0
#Determines if a drink menu is open
drink_menu_open = False
#Keeps track of currently open drink
cur_drink = ""
# -------- Main Program Loop -----------
while done == False:

	for event in pygame.event.get(): # User did something
		if event.type == pygame.QUIT: # If user clicked close
			done = True # Flag that we are done so we exit this loop
		elif event.type == pygame.MOUSEBUTTONDOWN:
			# User clicks the mouse. Get the position
			click_pos = pygame.mouse.get_pos()
			#Check if click is in the left sidebar
			##print(click_pos)
			if click_pos[0] <= (bar_width+margin):
				##print("Left sidebar clicked")
				#Check if button clicked

				#Check if menu can page left, if it can, decrement drink_page
				if drink_page > 0:
					drink_page -= 1
				'''
				#Else loop to end of drink pages
				else:
					drink_page = len(drink_list)-1
				'''

			#Check if click is in the right sidebar
			elif click_pos[0] >= (screen.get_width()-(bar_width+margin)):
				##print("Right sidebar clicked")
				#Check if button clicked

				#Check if menu can page right, if it can, increment drink_page
				if drink_page < (len(drink_list)-1):
					drink_page += 1
				'''
				#Else at end of list and loop back to beginning
				else:
					drink_page = 0
				'''

			#Else, click is in the middle section (list)
			else:
				##print("Menu click")
				#Gets which cell is clicked, margin counts as part of cell above it
				drink_click = int((click_pos[1]-margin)/(cell_height+margin))
				print(drink_list[drink_page][drink_click])
				drink_menu_open = True
				cur_drink = drink_list[drink_page][drink_click]
			
	# Set the screen background
	screen.fill(BLACK)
	'''
	if game_over:
	# If game over is true, draw game over
		if winner == 1:
			text = font.render("Green Wins", True, WHITE)
		if winner == 2:
			text = font.render("Blue Wins", True, WHITE)
		text_rect = text.get_rect()
		text_x = screen.get_width() / 2 - text_rect.width / 2
		text_y = screen.get_height() / 2 - text_rect.height / 2
		screen.blit(text, [text_x, text_y])
		pygame.display.flip()
		pygame.time.delay(1000)
		
	else:	
		'''
	'''Draw the side bars'''
	'''color = WHITE'''
	color = GREY
	#Left side bar
	pygame.draw.rect(screen, color,
					[margin,
					margin,
					bar_width-margin,
					screen.get_height()-(2*margin)])
	#Right side bar
	pygame.draw.rect(screen, color,
					[(margin*2)+cell_width+bar_width,
					margin,
					bar_width-margin, 
					screen.get_height()-(2*margin)])

	'''Draw the arrows in the side bar'''
	'''Old triangle arrows
	#Point lists of filled polygons for right and left arrows
	##points_left = [(50,260), (20, 310), (50, 360)]
	##points_right = [(750, 260), (780, 310), (750, 360)]
	#Create filled triangle on left side
	##pygame.draw.polygon(screen, CUST_COL, points_left, 0)
	#Create filled triangle on right side
	##pygame.draw.polygon(screen, BLACK, points_right, 0)
	'''
	#Point list of > shape, use percent of side bar width and height to set points
	arrow_right = [(margin+cell_width+bar_width + bar_width*0.3, margin+(bar_height*0.4)),#260),
					(margin+cell_width+bar_width + bar_width*0.5, margin+(bar_height*0.4)),
					(margin+cell_width+bar_width + bar_width*0.7, margin+(bar_height*0.5)),
					(margin+cell_width+bar_width + bar_width*0.5, margin+(bar_height*0.6)),
					(margin+cell_width+bar_width + bar_width*0.3, margin+(bar_height*0.6)),
					(margin+cell_width+bar_width + bar_width*0.5, margin+(bar_height*0.5))]
	#Create filled > shape on right side
	pygame.draw.polygon(screen, CUST_COL, arrow_right, 0) 
	#Point list of < shape, use percent of side bar width and height to set points
	arrow_left = [(margin+(bar_width*0.7), margin+(bar_height*0.4)),
				(margin+(bar_width*0.5), margin+(bar_height*0.4)),
				(margin+(bar_width*0.3), margin+(bar_height*0.5)),
				(margin+(bar_width*0.5), margin+(bar_height*0.6)),
				(margin+(bar_width*0.7), margin+(bar_height*0.6)),
				(margin+(bar_width*0.5), margin+(bar_height*0.5))]
	#Create filled < shape on left side
	pygame.draw.polygon(screen, CUST_COL, arrow_left, 0)
	
	'''Draw the grid'''
	iterat = 0
	for row in range(cell_num):
		'''color = WHITE'''
		color = GREY
		'''Draw the cells for the drinks'''
		#screen, color, [dist from left edge, dist from top edge], width of rectangle, height of rectangle
		pygame.draw.rect(screen,
						color,
						[(margin+bar_width),
						(margin+cell_height)*row+margin,
						cell_width,
						cell_height])


		text = font.render(drink_list[drink_page][iterat], True, BLACK)
		#Length of text, height of text (in pixels)
		text_size = font.size(drink_list[drink_page][iterat])
		#Center text vertically
		#Calculate height of cells * row, account for margin, then center in cell. -2 to account for text starting after 2 pixels
		text_y = (cell_height*row) + (margin*(row+1)) + ((cell_height-text_size[1])/2) - 2
		#Center text horizontally
		text_x = ((screen.get_width() - text_size[0])/2) - 2
		#Coordinates are top left of text box, text is actually 2 pixels down and right from coordinates
		#text, [dist from left edge, dist from top edge]
		screen.blit(text, [text_x, text_y])
		iterat += 1
 
	'''Check if drink menu is open'''
	if drink_menu_open:
		open_drink(screen, cur_drink)


	# Limit to 60 frames per second
	clock.tick(60)
 
	# Go ahead and update the screen with what we've drawn.
	pygame.display.flip()
	
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()