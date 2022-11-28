# Monopoly main game file (Sorry for license, github stuff)
# License: This version of monopoly is given out as a school project, however future versions may/will be licensed separately.
#          Being a school project means my teacher and school are given permission to view and modify this project as a way to help with grading this project.
#          The only condition being that I remain as the author of this project and in a position where I may continue to work on this project outside of school and be able to license any future versions of this project as i wish.
#          For al non school personel this project is private however you may use the code as insipiration as long as I (Simon Kalmi Claesson) gets credited and you link back to the github page: https://github.com/simonkalmiclaesson/Monopoly, note that you are not allowed to copy or claim this code or any assets from this project as your own.
#
# Other files:
#    utils.py - Utility file for keyboard and other
#    playsound.py - Work in progress sound player (Does not work)
#

# ======================================[ Setup ]====================================

# Imports
import os
import re
import time
import yaml
import random
import webcolors
from datetime import datetime
from utils import *
from playsound import * # Not done

# Enviroment Setup
setConSize(148,35)
setConTitle("Monopoly")
os.system("") # Enable ANSI

# Import name list
monopol = ['Gå' , 'Västra långgatan', 'Allmänning', 'Hornsgsgatan', 'Inkomstskatt', 'Södra station', 'Folkungagatan', 'Chans', 'Götgatan', 'Ringvägen', 'Besök fängelse', 'St Eriksgatan', 'Elverket', 'Odengatan', 'Valhallavägen', 'Östra station', 'Sturegatan', 'Allmänning', 'Karlavägen', 'Narvavägen', 'Fri parkering', 'Strandvägen', 'Chans', 'Kungsträdsgårdsgatan', 'Hamngatan', 'Centralstation', 'Vasagatan', 'Kungsgatan', 'Vattenledningsverket', 'Stureplan', 'Gå i fängelse', 'Gustav Adolfs Torg', 'Drottninggatan', 'Allmänning', 'Diplomatstaden', 'Norra station', 'Chans', 'Centrum', 'Betala lyxskatt', 'Norrmalmstorg']
gw_names = monopol

# =============================[ Define Render Functions ]===========================

# Debug function
def debug(msg):
	# Get globals
	global debug_enabled
	global debug_logging
	# Log message to file
	if debug_logging == True:
		# Get date and time from datetime
		now = datetime.now()
		hh = "[" + str(now.strftime("%d/%m/%Y %H:%M:%S")) + "] "
		logfile = ".//debug.log"
		# Write to file
		lf = open(logfile, "a")
		lf.write(str(hh) + str(msg) + "\n")
		lf.close()
	# Debug to game if enabled in settings
	if debug_enabled == True:
		# Get cords
		startCord = settings["debug"]["printCord"]
		# Print
		render_texture(0,int(startCord),["                                                         "],"light_gray")
		render_texture(0,int(startCord),[str(msg)],"light_gray")

# De tokenising function
def deTokenize(string):
	# Get tokens
	prepLine = str(string)
	tokens = re.findall(r'%.*?%',prepLine)
	# Get variable from token name and replace the token with the variables value
	for token in tokens:
		token = str(token)
		var = token.replace('%','')
		value = str(globals()[var])
		string = string.replace(token,value)
	# Return de-tokenised string
	return string

# Load texture
def load_texture (filepath):
	# Get content from file
	rawContent = open(filepath, 'r', encoding="utf-8").read()
	splitContent = rawContent.split("\n")
	# Fix empty last-line issue
	if splitContent[-1] == "":
		splitContent.pop(-1)
	# Return content as a list
	return splitContent

# Asset loader
def load_asset (filepath):
	# Get content from file
	rawContent = open(filepath, 'r', encoding="utf-8").read()
	splitContent = rawContent.split("\n") # Line splitter
	# Get asset configuration from file
	configLine = (splitContent[0]).split("#")[0]
	configLine_split = configLine.split(";")
	posX = configLine_split[0]
	posY = configLine_split[1]
	color = configLine_split[2]
	splitContent.pop(0)
	# Get texture
	texture = splitContent
	# Return config and texture
	return int(posX), int(posY), list(texture), str(color)

# Print sprite
def render_texture (posX,posY,texture,color):
	print("\033[s") # Save cursorPos
	# Get color code
	colorcode = getANSI(color)
	# Print texture
	c = 0
	OposY = int(posY)
	for line in texture:
		posY = OposY + c
		# Replace tokens in line
		line = deTokenize(line)
		# Set ansi prefix and print it
		ANSIprefix = "\033[" + str(apply_vertOffset(posY)) + ";" + str(posX) + "H" + "\033[" + str(colorcode) + "m"
		print(ANSIprefix, str(line), "\033[0m")
		c += 1
	print("\033[u\033[2A") # Load cursorPos

# Get ANSI code from name
def getANSI (name):
	# Get hex value
	hex = palette[name]
	hex = hex.replace("#",'')
	# Get RGB value
	lv = len(hex)
	rgb = tuple(int(hex[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
	rgbstr = str(rgb)
	rgbstr = rgbstr.replace(' ','')
	rgbstr = rgbstr.replace('(','')
	rgbstr = rgbstr.replace(')','')
	rgbdta = rgbstr.split(',')
	# Create ansi code string
	background=False
	ansi = '{};2;{};{};{}'.format(48 if background else 38, rgbdta[0], rgbdta[1], rgbdta[2])
	# Return ansi code string
	return ansi


# Apply global offset
def apply_vertOffset (posY):
	offset = settings["window"]["ui_offset"]
	y = int(posY) + int(offset)
	return y

# Cords choice
def cordsChoice (posX, posY, text=None, color=None):
	# get args
	baseColor = settings["theme"]["ui"]["text"]
	if color == None:
		color = ""
	if text == None:
		text = ""
	if color != "":
		color = baseColor
	# Save cursorPos
	print("\033[s")
	# Get color code
	colorcode = getANSI(color)
	# Print texture
	# Replace tokens in line
	text = deTokenize(text)
	# Set ansi prefix
	ANSIprefix = "\033[" + str(apply_vertOffset(posY)) + ";" + str(posX) + "H" + "\033[" + str(colorcode) + "m"
	input(str(ANSIprefix + str(text + "\033[0m")))
	# Load cursorPos
	print("\033[u\033[2A")

# Selector view function
def selector(state):
	# Get globals
	global ui_selector_state
	global ui_selector_pos
	global theme_selector
	# Switch state
	if state == None:
		state = ""
	if state == "":
		if ui_selector_state != True:
			ui_selector_state = False
	else:
		ui_selector_state = state
	# Rended correct selector texture depending on state
	if ui_selector_state == True:
		render_texture(ui_selector_pos[0],ui_selector_pos[1],texture_ui_selector,theme_selector)
	elif ui_selector_state == False:
		render_texture(ui_selector_pos[0],ui_selector_pos[1],texture_ui_selector_reset,theme_ui_list)

# Anim If enabled (If animations are enabled wait for a given time)
def animIfEnabled(animationsEnabled,timei):
	delay = float(timei)
	if animationsEnabled == True:
		time.sleep(delay)

# ============================[ Define Game Functions ]============================

# Handle tile tags
def handleTileTag(tag):
	global game_prison_maxtries
	global game_balance
	animationsEnabled = settings["animations"]["enabled"]
	debug(f"Event.HandleTileTag: {tag}")
	# Prison tag
	if tag == "prison":
		# Render prison Animation
		render_texture(0,0,texture_ui_effect_prison_bar_vertical,"blue")
		animIfEnabled(animationsEnabled,animation_delay_prison)
		render_texture(19,0,texture_ui_effect_prison_bar_vertical,"blue")
		animIfEnabled(animationsEnabled,animation_delay_prison)
		render_texture(37,0,texture_ui_effect_prison_bar_vertical,"blue")
		animIfEnabled(animationsEnabled,animation_delay_prison)
		render_texture(56,0,texture_ui_effect_prison_bar_vertical,"blue")
		animIfEnabled(animationsEnabled,animation_delay_prison)
		render_texture(73,0,texture_ui_effect_prison_bar_vertical,"blue")
		animIfEnabled(animationsEnabled,animation_delay_prison)
		render_texture(92,0,texture_ui_effect_prison_bar_vertical,"blue")
		animIfEnabled(animationsEnabled,animation_delay_prison)
		render_texture(110,0,texture_ui_effect_prison_bar_vertical,"blue")
		animIfEnabled(animationsEnabled,animation_delay_prison)
		render_texture(129,0,texture_ui_effect_prison_bar_vertical,"blue")
		animIfEnabled(animationsEnabled,animation_delay_prison)
		render_texture(145,0,texture_ui_effect_prison_bar_vertical,"blue")
		animIfEnabled(animationsEnabled,animation_delay_prison)
		render_texture(0,5,texture_ui_effect_prison_bar_horizontal,"blue")
		animIfEnabled(animationsEnabled,animation_delay_prison)
		render_texture(0,16,texture_ui_effect_prison_bar_horizontal,"blue")
		animIfEnabled(animationsEnabled,animation_delay_prison)
		render_texture(0,27,texture_ui_effect_prison_bar_horizontal,"blue")
		animIfEnabled(animationsEnabled,animation_delay_prison)
		# Render box
		render_texture(*object_ui_prisonMain)
		# Info msg
		render_texture(*object_ui_prisonInfo)
		# loop of dices
		tries = 0
		while tries <= int(game_prison_maxtries):
			showDices("reset","reset",theme_dice_selected)
			dice1, dice2 = 0,0
			showDices(dice1,dice2,theme_dice_selected,"id.2cords")
			render_texture(*object_ui_pressRtoRoll)
			res = waitKey(keymapping_roll)
			render_texture(*object_ui_prisonInfo_reset)
			if res == True:
				dice1, dice2 = rollDices()
				if int(dice1) == int(dice2):
					break
				else:
					tries += 1
		else:
			# Failed
			render_texture(*object_ui_prisonBuyOut)
			res = waitchoice(keymapping_yes,keymapping_no)
			render_texture(*object_ui_prisonBuyOut_reset)
			if res == keymapping_yes:
				if game_canAfford == False:
					if game_balance > game_prison_buyPrice:
						game_balance -= game_prison_buyPrice
					else:
						showGameLost()
				else:
					game_balance -= game_prison_buyPrice
			else:
				showGameLost()

		# Reset
		clear()
		renderBackground()
		renderTiles()
		renderBalance()
		render_texture(*object_ui_pressToSell)
		render_texture(*object_ownedTiles)
		renderOwnedTiles()
		render_texture(*object_ui_pressESCtoexit)
		setTile (board,game_current_tile,True,theme_tile_selected)
		posX, posY, texture, color = object_currentTile
		game_current_tile_name = board[game_current_tile]["name"]
		text_currentTile = lang["text_currentTile"]
		render_texture(posX, posY, resetTexture_currentTiles, color)
		render_texture(posX, posY, texture, color)

# Game won
def showGameWon():
	debug("Event.GameWon")
	render_texture(*object_ui_gameWon)
	pause()
	clear()
	exit()
# Game lost
def showGameLost():
	debug("Event.GameLost")
	render_texture(*object_ui_gameLost)
	pause()
	clear()
	exit()

# Show welcomme
def showWelcomme():
	render_texture(0, 0, texture_ui_welcome, theme_ui_background)
	render_texture(*object_ui_welcome_title)
	render_texture(*object_ui_welcome_text)
	render_texture(*object_ui_welcome_starttext)
	render_texture(*object_ui_welcome_dependencies)
	pause()

# Show exit dialog
def showExitDialog():
	render_texture(*object_ui_exitDialog)
	res = waitchoice(keymapping_enter,keymapping_esc)
	if res == keymapping_esc:
		return False
	if res == keymapping_enter:
		return True

# Get cords of tile
def getCords_ofTile (config,name):
	cords = config[name]["cords"]
	return cords

# Toggle tile
def setTile (config,name,state,color):
	cords = config[name]["cords"]
	selectedColor = color
	gotColor = board[name]["color"]
	if gotColor != "":
		selectedColor = gotColor
	if state == True:
		texture = texture_tile_selected
	elif state == False:
		texture = texture_tile_normal
	else:
		return "\033[31mError:State is boolean!\033[0m"
	render_texture(cords[0],cords[1],texture,selectedColor)

# Roll dices
def showDices(dice_one_face,dice_two_face,theme,overwriteID=None):
	if (overwriteID == "id.2cords"):
		first_dice = board["dice.1"]["2cords"]
		second_dice = board["dice.2"]["2cords"]
	else:
		first_dice = board["dice.1"]["cords"]
		second_dice = board["dice.2"]["cords"]
	first_dice_file = location_dice + "dice_" + str(dice_one_face) + ".ta"
	second_dice_file = location_dice + "dice_" + str(dice_two_face) + ".ta"
	first_dice_texture = load_texture(first_dice_file)
	second_dice_texture = load_texture(second_dice_file)
	render_texture(first_dice[0],first_dice[1],first_dice_texture, theme)
	render_texture(second_dice[0],second_dice[1],second_dice_texture, theme)

# Roll dices
def rollDices():
	# Load config
	diceRange = settings["gameStuff"]["diceRange"].split('-')
	animationsEnabled = settings["animations"]["enabled"]
	# Clear last roles
	render_texture(*object_ui_pressRtoRoll_reset)
	showDices("reset","reset",theme_dice_selected,"id.2cords")
	# Animate roll
	if animationsEnabled == True:
		animationFrames = 20
		shownFrames = 0
		while shownFrames < animationFrames:
			dice1 = random.randint(int(diceRange[0]),int(diceRange[1]))
			dice2 = random.randint(int(diceRange[0]),int(diceRange[1]))
			showDices(dice1,dice2,theme_dice)
			time.sleep(float(animation_delay_diceroll))
			shownFrames = shownFrames + 1
	# Roll result
	dice1 = random.randint(int(diceRange[0]),int(diceRange[1]))
	dice2 = random.randint(int(diceRange[0]),int(diceRange[1]))
	# Animate winning roll
	if animationsEnabled == True:
		animationFrames = 8
		shownFrames = 0
		isYellow = False
		while shownFrames < animationFrames:
			if isYellow == True:
				# show yellow
				isYellow = False
				showDices(dice1,dice2,theme_dice)
			else:
				# show green
				isYellow = True
				showDices(dice1,dice2,theme_dice_selected)
			time.sleep(float(animation_delay_diceroll_win))
			shownFrames = shownFrames + 1
	# Show result
	showDices(dice1,dice2,theme_dice_selected)
	debug(f"Event.rollDices: [1: {dice1}, 2: {dice2}]") # Debug
	return (dice1,dice2)

# Update owned tiles
def renderOwnedTiles():
	newList = list()
	items = game_ownedTiles
	renderLines = int(settings["window"]["height"]) - 5
	for item in items:
		string = "- " + str(item)
		newList.append(string)
	if len(newList) > int(renderLines):
		newList = newList[0:int(renderLines)]
	posX, posY, texture, color = object_ownedTilesList
	texture = newList
	render_texture(posX, posY, texture, color)

# Render background
def renderBackground():
	render_texture(0, 0, texture_ui_background, theme_ui_background)

# Render tiles
def renderTiles():
	for i in board:
		# Only render tile
		if "tile" in str(i):
			# Set color
			selectedColor = theme_tile
			gotColor = board[str(i)]["color"]
			gotTag = board[str(i)]["tag"]
			otexture = texture_tile_normal
			#if gotTag == "tax":
			#	otexture = texture_tile_tag_tax
			#elif gotTag == "prison":
			#	otexture = texture_tile_tag_prison
			#elif gotTag == "prison_visit":
			#	otexture = texture_tile_tag_prison_visit
			#else:
			#	otexture = texture_tile_normal
			if gotColor != "":
				selectedColor = gotColor
			cords = getCords_ofTile(board,i)
			render_texture(cords[0], cords[1], otexture, selectedColor)

# Render balance
def renderBalance():
	global game_balance
	render_texture(*object_balance_reset)
	posX, posY, texture, color = object_balance
	# Negative balance
	if int(game_balance) < 0:
		color = "red"
		ngame_balance = int(str(game_balance).replace('-',''))
		newBalanceTexture = str(texture[0]).replace('%currency_symbol%%game_balance%',f"-{currency_symbol}{ngame_balance}")
		texture = [newBalanceTexture]
	# Render
	render_texture(posX, posY, texture, color)

# Walk through tiles
def walkTiles(game_current_tile,steps):
	debug(f"Event.walkTiles: {game_current_tile} +> {steps}") # Debug
	# Globals
	global game_ownedTiles
	global game_rounds
	global game_balance
	# Get config
	animationsEnabled = settings["animations"]["enabled"]
	oldTile = game_current_tile
	tileNum = int(str(game_current_tile).split('.')[1])
	newTileNum = tileNum + steps
	# Handle rounds
	if newTileNum > 40:
		org_game_rounds = game_rounds
		game_rounds += 1
		debug(f"Event.walkTiles.goRound: {org_game_rounds} --> {game_rounds}") # Debug
		# Payment if enabled
		if game_roundIncome == True:
			for tilename in game_ownedTiles:
				selectedItem_id = ""
				for tile in board:
					if "tile." in str(tile):
						if str(board[tile]["name"]) == tilename:
							selectedItem_id = str(tile)
				income = board[selectedItem_id]["payEventIncome"]
				if str(income) != "":
					game_balance += int(income)
	if animationsEnabled == True:
		posX, posY, texture, color = object_currentTileIsWalking
		render_texture(posX, posY, resetTexture_currentTiles, color)
		render_texture(posX, posY, texture, color)
		stepsTaken = 0
		while stepsTaken <= steps:
			gotoTile = tileNum + stepsTaken
			# Handle round
			if gotoTile > 40:
				gotoTile = gotoTile - 40
			if gotoTile == 0:
				gotoTile = 1
			# Walk
			setTile (board,game_current_tile,False,theme_tile)
			game_current_tile = "tile." + str(gotoTile)
			setTile (board,game_current_tile,True,theme_tile_selected)
			time.sleep(float(animation_delay_walk))
			stepsTaken += 1
	else:
		# Handle round
		if newTileNum >= 40:
			newTileNum = newTileNum - 40
		if newTileNum == 0:
			newTileNum = 1
		# Walk
		setTile (board,oldTile,False,theme_tile)
		game_current_tile = "tile." + str(newTileNum)
		setTile (board,game_current_tile,True,theme_tile_selected)
	return game_current_tile

# Owned tile
def ownedTile(action,tile):
	global game_ownedTiles
	tilename = board[tile]["name"]
	#add
	if action == "add":
		game_ownedTiles.append(tilename)
	#Remove
	if action == "remove":
		game_ownedTiles.remove(tilename)

# Buy tile
def buyTile(tile,price,local_game_balance):
	price = int(price)
	if game_canAfford == True:
		local_game_balance -= price
	else:
		if local_game_balance >= price:
			local_game_balance -= price
	renderBalance()
	ownedTile("add",tile)
	renderOwnedTiles()
	debug(f"Event.BuyTile: {tile}")
	return local_game_balance

# Sell tile
def sellTile():
	global ui_selector_pos
	global game_balance
	# Fix no owned tiles
	if len(game_ownedTiles) < 1:
		debug("Event.SellTile.Exeption.NoTilesOwned")
		return "\033[31mError: NoOwnedTiles\033[0m"
	# First position
	selectorX, posY, texture, color = object_ownedTilesList
	startItemPos = posY
	# Selector
	items = game_ownedTiles
	endItemPos = int(startItemPos) + int(len(items)) - 1
	# pop selector to first pos
	ui_selector_pos = [selectorX,startItemPos]
	selector(True)
	# Loop for rendering and choosing
	ShallExit = False
	IsSelecting = True
	while IsSelecting == True:
		# Get selected item
		indexVal = int(ui_selector_pos[1]) - int(startItemPos)
		selectedItem = items[indexVal]
		# Move if pressed
		res = waitchoice4(keymapping_up,keymapping_down,keymapping_enter,keymapping_esc)
		if res == keymapping_up:
			# Move selector up
			if ui_selector_pos[1] != startItemPos:
				selector(False)
				ui_selector_pos = [int(ui_selector_pos[0]),int(int(ui_selector_pos[1]) - 1)]
				selector(True)
			res = ""
		elif res == keymapping_down:
			# Move selector down
			if ui_selector_pos[1] != endItemPos:
				selector(False)
				ui_selector_pos = [int(ui_selector_pos[0]),int(int(ui_selector_pos[1]) + 1)]
				selector(True)
			res = ""
		elif res == keymapping_enter:
			# Select tile
			IsSelecting = False
			selector(False)
			break
		elif res == keymapping_esc:
			ShallExit = True
			IsSelecting = False
			selector(False)
			break
		else:
			res = ""
	# Remove tile from ownedTiles and rerender the tiles
	if ShallExit == False:
		selectedItem_id = ""
		for tile in board:
			if "tile." in str(tile):
				if str(board[tile]["name"]) == selectedItem:
					selectedItem_id = str(tile)
		if selectedItem_id != "":
			ownedTile("remove",selectedItem_id)
			price = int(board[selectedItem_id]["price"])
			returnMoney = int(round(float(price) * float(game_sellModifier)))
			game_balance += returnMoney
			renderBalance()
		render_texture(*object_ui_ownedTiles_reset)
		renderOwnedTiles()
		debug(f"Event.SellTile: {selectedItem}")
	else:
		debug("Event.SellTile.Canceled")

# Handle Tile Event
def handleTileEvent(game_current_tile):
	global game_ownedTiles
	global game_currenttile_passover
	global text_payedPassover
	# Get game balance
	game_balance = globals()["game_balance"]
	# Get tile properties
	passover = board[game_current_tile]["passover"]
	price = board[game_current_tile]["price"]
	game_current_tile_name = board[game_current_tile]["name"]
	tag = board[game_current_tile]["tag"]
	# Handle passover
	if passover != "":
		# Set global value
		game_currenttile_passover = passover
		# Apply to balance
		org_game_balance = game_balance
		passoverType = str(passover)[0]
		passoverNum = int(str(passover).replace(passoverType,""))
		if passoverType == "-":
			# SubtractivePassoverEvent
			debug(f"Event.tileEvent.subtractiveAction: {passover}")
			# Show text
			text_payedPassover = text_payedPassover_sub
			game_currenttile_passover_bac = game_currenttile_passover
			game_currenttile_passover = str(game_currenttile_passover).replace('-',"").replace('+',"")
			render_texture(*object_ui_hasPayedPassover_reset)
			render_texture(*object_ui_hasPayedPassover)
			game_currenttile_passover = game_currenttile_passover_bac
			# Apply to balance
			game_balance -= passoverNum
		elif passoverType == "+":
			# AddativePassoverEvent
			debug(f"Event.tileEvent.addativeAction: {passover}")
			# Show text
			text_payedPassover = text_payedPassover_add
			render_texture(*object_ui_hasPayedPassover_reset)
			render_texture(*object_ui_hasPayedPassover)
			# Apply to balance
			game_balance += passoverNum
		else:
			debug("Event.tileEvent.Exeption.NoPassoverEventType")
			return "\033[31mNoPassoverEventType\033[0m"
	# Handle tags
	handleTileTag(tag)
	# Handle price
	if price != "":
		if str(game_current_tile_name) in str(game_ownedTiles):
			owned = True
		else:
			owned = False
		if owned == False:
			render_texture(*object_ui_hasPayedPassover_reset)
			# Ask if wanna buy?
			render_texture(*object_ui_doYouWanaBuy)
			global game_currenttile_price
			game_currenttile_price = price
			posX, posY, texture, color = object_ui_price
			if game_canAfford == False:
				if price >= game_balance:
					color == "red"
			render_texture(posX, posY, texture, color)
			res = waitchoice(keymapping_yes,keymapping_no)
			render_texture(*object_ui_price_reset)
			render_texture(*object_ui_doYouWanaBuy_reset)
			if res == keymapping_yes:
				game_balance = buyTile(game_current_tile,price,game_balance)
	# Return possibly changed values
	return game_balance


# =================================[ Config game ]=================================

# Globla variables
none = ""

# Load config
config_path = "."
boardFile = config_path + "//board.yaml"
settingsFile = config_path + "//settings.yaml"
boardRaw = open(boardFile, 'r').read()
settingsRaw = open(settingsFile, 'r', encoding="utf-8").read()
board = yaml.load(boardRaw, Loader=yaml.Loader)
settings = yaml.load(settingsRaw, Loader=yaml.Loader)
palette = settings["theme"]["palette"]
lang = settings["lang"]

# Apply window properties from settings
setConSize(settings["window"]["width"],settings["window"]["height"])
setConTitle(settings["window"]["title"])

# Apply names from gw_names
c = 0
for o in board:
	if "tile." in str(o):
		settings["lang"][str(o)] = gw_names[c]
		c = c + 1

# Apply names to board tiles
c = 0
for o in board:
	if "tile." in str(o):
		board[str(o)]["name"] = settings["lang"][str(o)]
		c = c + 1

# Load theme
theme = settings["theme"]
theme_dice = theme["dice"]["normal"]
theme_dice_selected = theme["dice"]["selected"]
theme_tile = theme["tile"]["normal"]
theme_tile_selected = theme["tile"]["selected"]
theme_ui_background = theme["ui"]["background"]
theme_ui_text = theme["ui"]["text"]
theme_ui_list = theme["ui"]["list"]
theme_selector = theme["ui"]["selector"]

# Debug
debug_enabled = settings["debug"]["enabled"]
debug_length = settings["debug"]["length"]
debug_logging = settings["debug"]["logging"]
if debug_enabled == True:
	debug_title  = str(settings["window"]["title"]) + " -DEBUG"
	debug_height = int(settings["window"]["height"]) + int(debug_length)
	setConSize(settings["window"]["width"],debug_height)
	setConTitle(debug_title)

# Prep load textures into variables
texture_ui_background = load_texture(".//assets//ui_max.ta")
texture_tile_normal = load_texture(".//assets//tile.ta")
texture_tile_selected = load_texture(".//assets//tile_selected.ta")
texture_ui_selector = load_texture(".//assets//ui_selector.ta")
texture_ui_selector_reset = load_texture(".//assets//ui_selector_reset.ta")
texture_ui_welcome = load_texture(".//assets//ui_welcome.ta")
texture_ui_effect_prison_bar_vertical = load_texture(".//assets//effects//prison//ui_prison_bar_vertical.ta")
texture_ui_effect_prison_bar_horizontal = load_texture(".//assets//effects//prison//ui_prison_bar_horizontal.ta")
texture_ui_effect_prison_bar_horizontal_filled = load_texture(".//assets//effects//prison//ui_prison_bar_horizontal_filled.ta")
#texture_tile_tag_prison = load_texture(".//assets//tile_prison.ta")
#texture_tile_tag_tax = load_texture(".//assets//tile_tax.ta")
object_balance = load_asset(".//assets//balance.asset")
object_balance_reset = load_asset(".//assets//balance_reset.asset")
object_currentTile = load_asset(".//assets//currentTile.asset")
object_ownedTiles = load_asset(".//assets//ownedTiles.asset")
object_ownedTilesList = load_asset(".//assets//ownedTilesList.asset")
object_currentTileIsWalking = load_asset(".//assets//currentTile_isWalking.asset")
object_ui_welcome_title = load_asset(".//assets//ui_welcome_title.asset")
object_ui_welcome_text = load_asset(".//assets//ui_welcome_text.asset")
object_ui_welcome_starttext = load_asset(".//assets//ui_welcome_starttext.asset")
object_ui_pressRtoRoll = load_asset(".//assets//text_pressRtoRoll.asset")
object_ui_pressRtoRoll_reset = load_asset(".//assets//text_pressRtoRoll_reset.asset")
object_ui_doYouWanaBuy = load_asset(".//assets//text_doYouWannaBuy.asset")
object_ui_doYouWanaBuy_reset = load_asset(".//assets//text_doYouWannaBuy_reset.asset")
object_ui_price = load_asset(".//assets//price.asset")
object_ui_price_reset = load_asset(".//assets//price_reset.asset")
object_ui_pressToSell = load_asset(".//assets//text_pressToSell.asset")
object_ui_hasPayedPassover = load_asset(".//assets//hasPayedPassover.asset")
object_ui_hasPayedPassover_reset = load_asset(".//assets//hasPayedPassover_reset.asset")
object_ui_ownedTiles_reset = load_asset(".//assets//ownedTilesList_reset.asset")
object_ui_exitDialog = load_asset(".//assets//ui_exitDialog.asset")
object_ui_pressESCtoexit = load_asset(".//assets//ui_pressESCtoexit.asset")
object_ui_welcome_dependencies = load_asset(".//assets//ui_welcome_dependencies.asset")
object_ui_gameWon = load_asset(".//assets//ui_gameWon.asset")
object_ui_gameLost = load_asset(".//assets//ui_gameLost.asset")
object_ui_prisonBuyOut = load_asset(".//assets//text_prisonBuyOut.asset")
object_ui_prisonBuyOut_reset = load_asset(".//assets//text_prisonBuyOut_reset.asset")
object_ui_prisonInfo = load_asset(".//assets//text_prisonInfo.asset")
object_ui_prisonInfo_reset = load_asset(".//assets//text_prisonInfo_reset.asset")
object_ui_prisonMain = load_asset(".//assets//ui_prisonMain.asset")
location_dice = ".//assets//dices//"
# Prep load resets
resetTexture_currentTiles = load_texture(".//assets//currentTile_reset.ta")

# Prep sound file
location_backgroundMusic = ".//assets//tracks//" + settings["sound"]["backgroundTrack"]
soundsEnabled = settings["sound"]["enabled"]

# Load keymappings
keymapping_yes = settings["keymaps"]["_yes"]
keymapping_no = settings["keymaps"]["_no"]
keymapping_roll = settings["keymaps"]["_roll"]
keymapping_sell = settings["keymaps"]["_sell"]
keymapping_up = settings["keymaps"]["_up"]
keymapping_down = settings["keymaps"]["_down"]
keymapping_enter = settings["keymaps"]["_enter"]
keymapping_esc = settings["keymaps"]["_esc"]

# Load animations
animation_delay_diceroll = settings["animations"]["delay"]["diceroll"]
animation_delay_diceroll_win = settings["animations"]["delay"]["diceroll_win"]
animation_delay_walk = settings["animations"]["delay"]["walk"]
animation_delay_prison = settings["animations"]["delay"]["prison"]

# Prep prep of text :)
currency_symbol = lang["currency_symbol"]

# Prep gamestuff
game_starting_cash = settings["gameStuff"]["startingCash"]
game_starting_tile = settings["gameStuff"]["startingTile"]
game_sellModifier = settings["gameStuff"]["sellModifier"]
game_winningRound = settings["gameStuff"]["winningRound"]
game_loosingNoMoney = settings["gameStuff"]["loosingNoMoney"]
game_canAfford = settings["gameStuff"]["canAfford"]
game_prison_maxtries = settings["gameStuff"]["prison_maxTries"]
game_prison_buyPrice = settings["gameStuff"]["prison_buyPrice"]
game_roundIncome = settings["gameStuff"]["roundIncome"]

# Prep texts
text_doYouWannaBuy = deTokenize(lang["text_doYouWannaBuy"])
text_balance = deTokenize(lang["text_balance"])
text_payedPassover_sub = deTokenize(lang["text_payedPassover_sub"])
text_payedPassover_add = deTokenize(lang["text_payedPassover_add"])
text_prisonBuyOut = deTokenize(lang["text_prisonBuyOut"])
text_prisonInfo = deTokenize(lang["text_prisonInfo"])
text_prisonInfo2 = deTokenize(lang["text_prisonInfo2"])

# ==============================[ Main Game Section ]==============================

# Play sound file
if soundsEnabled == True:
	playsound(location_backgroundMusic)

# [Show welcomme screen]
clear()
showWelcomme()

# [Prep render]
game_balance = game_starting_cash
currency_symbol = lang["currency_symbol"]
game_ownedTiles = []
ui_selector_state = False
dice1,dice2 = 0,0
game_currenttile_passover = ""
text_payedPassover = ""

# [Render game]
clear()
renderBackground()
renderTiles()
renderBalance()
render_texture(*object_ui_pressToSell)
render_texture(*object_ownedTiles)
renderOwnedTiles()
render_texture(*object_ui_pressESCtoexit)

# [Render starting tile]
setTile (board,game_starting_tile,True,theme_tile_selected)
posX, posY, texture, color = object_currentTile
game_current_tile = game_starting_tile
game_current_tile_name = board[game_current_tile]["name"]
text_currentTile = lang["text_currentTile"]
render_texture(posX, posY, resetTexture_currentTiles, color)
render_texture(posX, posY, texture, color)

# [Main game loop]
RunGame = True
game_rounds = 0
while (RunGame == True):
	# Handle loosing condition
	if game_loosingNoMoney == True:
		if game_balance <= 0:
			showGameLost()
	# Handle winning condition
	if game_winningRound != False:
		if game_rounds == game_winningRound:
			showGameWon()
	# Roll Dices
	showDices("reset","reset",theme_dice_selected)
	showDices(dice1,dice2,theme_dice_selected,"id.2cords")
	render_texture(*object_ui_pressRtoRoll)
	res = waitchoice3(keymapping_roll,keymapping_sell,keymapping_esc)
	if res == keymapping_roll:
		render_texture(posX, posY, resetTexture_currentTiles, color)
		dice1, dice2 = rollDices()
		game_steps = int(dice1) + int(dice2)
		# Walk to pos
		text_isWalking = lang["text_isWalking"]
		game_current_tile = walkTiles(game_current_tile,game_steps)
		# Update current tile
		posX, posY, texture, color = object_currentTile
		game_current_tile_name = board[game_current_tile]["name"]
		text_currentTile = lang["text_currentTile"]
		render_texture(posX, posY, resetTexture_currentTiles, color)
		render_texture(posX, posY, texture, color)
		# Handle tile event
		game_balance = handleTileEvent(game_current_tile)
		renderBalance()
	elif res == keymapping_sell:
		sellTile()
	elif res == keymapping_esc:
		debug("Event.Keypress.ESC")
		esc = showExitDialog()
		if esc == True:
			clear()
			exit()
		else:
			clear()
			renderBackground()
			renderTiles()
			renderBalance()
			render_texture(*object_ui_pressToSell)
			render_texture(*object_ownedTiles)
			renderOwnedTiles()
			render_texture(*object_ui_pressESCtoexit)
			setTile (board,game_current_tile,True,theme_tile_selected)
			posX, posY, texture, color = object_currentTile
			game_current_tile_name = board[game_current_tile]["name"]
			text_currentTile = lang["text_currentTile"]
			render_texture(posX, posY, resetTexture_currentTiles, color)
			render_texture(posX, posY, texture, color)
