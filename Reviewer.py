import ast	# This module allows us to convert text into dictionaries
import random
import os

# loads the text file which contains the items
def readFile():
	try:
		with open('items.txt', 'r') as file:
			if len(file.read()) == 0:
				return False

			file.seek(0)
			return file.readlines()

	except:
		with open('items.txt', 'w') as file:
			return False

# this function is called whenever the program intends to add an item
def addItem(item, description):
	item = '{' + f'\'{item}\': \'{description}\'' + '}'
	
	with open('items.txt', 'a') as file:
		file.write(f'{item}\n')

# this function converts a file list, which is a list that is returned by 
# calling readFile(), into a dictionary
def convertItems(fileList):
	convertedList = {}

	if fileList == False:
		clearScreen()
		print('Currently there are no items saved.\n')
		printDismiss('Press enter to continue.')
		return False, False

	random.shuffle(fileList)

	for line in fileList:
		dictt = ast.literal_eval(line)
		for k, v in dictt.items():
			convertedList[k] = v

	return convertedList, len(fileList)

# this function initiates the Review Mode feature of the program
def reviewMode(fileList):
	userInput = ''
	items, itemQuantity = convertItems(fileList)

	if items == False:
		return

	i = 0

	for k, v in items.items():
		i += 1
		print('\n' + v + '\n\n')
		printDismiss(f'[Items left: {itemQuantity - i}]\nPress enter to show answer.')
		print('\n' + k + '\n\n')
		userInput = printDismiss('Press enter to continue. Enter 0 to exit Review Mode.')

		if userInput == '0':
			break

# this function shows the user the list of all the items that are in the text file
def listAllItems(fileList):
	items, _ = convertItems(fileList)


	if items == False:
		return

	for k, v in items.items():
		print(k)
		print(v + '\n')

	printDismiss('Press enter to continue.')

# clears the terminal
def clearScreen():
	os.system('cls')

# shows a message, then clears the terminal after the user pressed Enter
def printDismiss(cmd):
	userInput = input(cmd)
	os.system('cls')
	return userInput

# allows the user to edit an item using the program
def editItem(fileList):
	userInput = '0'
	found = False

	check, _ = convertItems(fileList)

	if check == False:
		return

	itemName = input('Enter item name that you want to edit: ')
	clearScreen()

	with open('items.txt', 'r') as file:
		for line in file.readlines():
			if itemName in line:
				found = True
				break

	if not found:
		print('Item not found.')
		printDismiss('Press enter to continue.')
		return

	while userInput not in ['1', '2']: # repeats the loop whenever the user enters undesired inputs
		userInput = input('What do you want to edit: \n\n[1] Item name\n[2] Item description\n\n')
		dictItems, _ = convertItems(fileList)
		itemDescription = dictItems[itemName]

		dictItems.pop(itemName)

		clearScreen()

		if userInput == '1':
			newName = input('Enter new name: ')
			dictItems[newName] = itemDescription

		elif userInput == '2':
			dictItems[itemName] = input('Enter new description: ')

		open('items.txt', 'w')
		with open('items.txt', 'a') as file:
			for k, v in dictItems.items():
				addItem(k, v)

		clearScreen()
		print('Item modified.\n')
		printDismiss('Press enter to continue.')

# this function initiates the Exam Mode feature of the program
def examMode(fileList):
	clearScreen()
	score = 0
	itemCounter = 1
	dictItems, itemQuantity = convertItems(fileList)

	if dictItems == False:
		return

	question = ''
	answer = ''
	userAnswer = 0
	possibleChoices = []
	choices = []

	# this feature requires 4 or more items
	if itemQuantity < 4:
		print('Number of items must be greater than 3')
		printDismiss('Press enter to continue.')
		return

	for k, v in dictItems.items():
		possibleChoices.append(v)

	for k, v in dictItems.items():
		question = k
		answer = v

		choices.append(answer)
		random.shuffle(possibleChoices)

		counter = 0

		# this loop adds 3 random wrong choices
		for _ in possibleChoices:
			if len(choices) == 4:
				break
			if not possibleChoices[counter] == answer:
				choices.append(possibleChoices[counter])
			counter += 1
		random.shuffle(choices)


		userAnswer = 0

		# this loop repeats whenever the user enters undesired input
		while userAnswer > 4 or userAnswer < 1:
			clearScreen()
			print(f'Item {itemCounter} / {itemQuantity}			Score: {score}\n')
			print(question + '\n')

			choiceNum = 1
			for choice in choices:
				print(f'[{choiceNum}] {choice}')
				choiceNum += 1

			userAnswer = input('\nYour answer: ')
			if userAnswer == '':
				userAnswer = 0
			else:
				userAnswer = int(userAnswer)

		if choices[userAnswer - 1] == answer:
			input('\nCorrect.')
			score += 1
		else:
			input('\nWrong.')

		choices.clear()
		itemCounter += 1

	clearScreen()
	input('Your score: ' + str(score))


# this function allows the user to delete an item using the program
def deleteItem(fileList):
	clearScreen()
	dictItems, _ = convertItems(fileList)

	if dictItems == False:
		return

	found = False

	itemName = input('Enter the name of the item that you want to delete: ')
	clearScreen()

	with open('items.txt', 'r') as file:
		for line in file.readlines():
			if itemName in line:
				found = True
				break

	if not found:
		print('Item not found.')
		printDismiss('Press enter to continue.')
		return

	dictItems.pop(itemName)

	open('items.txt', 'w')
	with open('items.txt', 'a') as file:
		for k, v in dictItems.items():
			addItem(k, v)

	print('Item deleted.')
	printDismiss('Press enter to continue.')

# this function shows the user the Main Menu
def showMenu():
	menu = '''
CLI Terms Reviewer

[1] Add an item
[2] List all items
[3] Edit item
[4] Delete item
[5] Review mode
[6] Exam mode
[0] Exit
	'''

	print(menu)


# Main loop
userInput = 0
while True:

	clearScreen()
	showMenu()
	userInput = input()
	clearScreen()

	if userInput == '1':
		name = input('Enter item name: ')
		description = input('Enter item description: ')
		addItem(name, description)

		printDismiss(f'Item {name} added.')
	elif userInput == '2':
		listAllItems(readFile())
	elif userInput == '3':
		editItem(readFile())
	elif userInput == '4':
		deleteItem(readFile())
	elif userInput == '5':
		reviewMode(readFile())
	elif userInput == '6':
		examMode(readFile())
	elif userInput == '0':
		break
	else:
		clearScreen()
		printDismiss('Choose only from the given choices.\n\nPress enter to continue.')

