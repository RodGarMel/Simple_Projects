import time
import random
import string

alphabet = string.ascii_letters + "ñ" + "Ñ"
symbols = ["$", "%", "&", "#"]

random_number = random.randint(0,100000000) #Random number between 0 and 100 million
print(f"user{random_number}")

password = ""
lenght = 12

while len(password) < lenght: #12 characts
    random_n = random.randint(0,9) #Number
    str_random_n = str(random_n) #Previous number selected converted to string so we can concatenate
    character = random.choice(alphabet) #Random choice on the letters of the alphabet
    charactersS = random.choice(symbols) #Random choice on symbols
    randomchoice = [str_random_n, character, charactersS] #Adding symbols, letters and numbers into a list so we can pick a random object from this list

    pass_characters_randomized = random.choice(randomchoice) #Picking a random character (symbol, number or letter)
    password += pass_characters_randomized #The random choice concatenates on the original empty string

    # Some visuals to 'generate' the password live on the terminal
    glitched_charac = ""

    for i in range (lenght - int(len(password))): #Password lenght - Generated password, to get the number of characters left
        rnd = random.choice(randomchoice) #Picking a random character (symbol, number or letter)
        glitched_charac += rnd #Concatenating x number of random characters into the original empty string
    
    print(password+glitched_charac, end="\r") #Prints the generated password + the number of characters left (randomized characters)
    time.sleep(0.1)


print(password)