#Two Dimensional Array containing the probabilities of each letter being in a given position
#It's an array because it has to be mutable. Indexing can be done with the ord() function
prob = [[140, 304, 306, 162, 63],[ 173, 16, 56, 24, 11],[ 198, 40, 56, 150, 31],[ 111, 20, 75, 69, 118],[ 72, 241, 177, 318, 422],[ 135, 8, 25, 35, 26],[ 115, 11, 67, 76, 41],[ 69, 144, 9, 28, 137],[ 34, 201, 266, 158, 11],[ 20, 2, 3, 2, 0],[ 20, 10, 12, 55, 113],[ 87, 200, 112, 162, 155],[ 107, 38, 61, 68, 42],[ 37, 87, 137, 182, 130],[ 41, 279, 243, 132, 58],[ 141, 61, 57, 50, 56],[ 23, 5, 1, 0, 0],[ 105, 267, 163, 150, 212],[ 365, 16, 80, 171, 36],[ 149, 77, 111, 139, 253],[ 33, 185, 165, 82, 1],[ 43, 15, 49, 45, 0],[ 82, 44, 26, 25, 17],[ 0, 14, 12, 3, 8],[ 6, 22, 29, 3, 364],[ 3, 2, 11, 20, 4]]
#list of all legal guesses in wordle
legalGuesses = []
for line in open("wordlelegalguesses.txt", "r"):
    legalGuesses.append(line.strip())

#Helper method for cleanly accessing probabilities
def getProb(char, index):
    return prob[ord(char.lower())-ord('a')][index]
#debug method
def printProb():
    for i in range(len(prob)):
        print("{}: {}".format(chr(ord('a')+i), prob[i]))
#debug method, used to easily wipe the slate clean after running an algorithm
def resetProb():
    global prob
    prob = [[140, 304, 306, 162, 63],[ 173, 16, 56, 24, 11],[ 198, 40, 56, 150, 31],[ 111, 20, 75, 69, 118],[ 72, 241, 177, 318, 422],[ 135, 8, 25, 35, 26],[ 115, 11, 67, 76, 41],[ 69, 144, 9, 28, 137],[ 34, 201, 266, 158, 11],[ 20, 2, 3, 2, 0],[ 20, 10, 12, 55, 113],[ 87, 200, 112, 162, 155],[ 107, 38, 61, 68, 42],[ 37, 87, 137, 182, 130],[ 41, 279, 243, 132, 58],[ 141, 61, 57, 50, 56],[ 23, 5, 1, 0, 0],[ 105, 267, 163, 150, 212],[ 365, 16, 80, 171, 36],[ 149, 77, 111, 139, 253],[ 33, 185, 165, 82, 1],[ 43, 15, 49, 45, 0],[ 82, 44, 26, 25, 17],[ 0, 14, 12, 3, 8],[ 6, 22, 29, 3, 364],[ 3, 2, 11, 20, 4]]

#Defines value of a word by multiplying the probability of every letter
#Multiplying the values makes it so a 0 probabality is possible
#The value is raised to the power of the number of unique letters in the word
def getValue(word):
    value = 1
    power = 1
    for i in range(len(word)):
        if word.count(word[i]) == 1:
            power += 1
        value *= getProb(word[i], i)
    return pow(value,power)
#Returns the most likely word based on current probabilites
def getBestWord():
    best = "QQQQQ"
    for word in legalGuesses:
        if getValue(word) > getValue(best) :
            best = word
    return best
#Takes a word and a string of 0,1, and 2 corresponding to grey yellow and green
def adjustProb(guess, results):
    for i in range(len(guess)):
        if results[i] == '0':
            #grey
            #different results if the letter is duplicated
            if(guess.count(guess[i]) == 1):
                prob[ord(guess[i].lower())-ord('a')] = [0,0,0,0,0]
            else:
                prob[ord(guess[i].lower())-ord('a')][i] = 0
        elif results[i] == '1':
            #yellow
            for j in range(len(prob[ord(guess[i].lower())-ord('a')])):
                prob[ord(guess[i].lower())-ord('a')][j] *= 10
            prob[ord(guess[i].lower())-ord('a')][i] = 0
        elif results[i] == '2':
            #green
            save = prob[ord(guess[i])-ord('a')][i]
            for array in prob :
                array[i] = 0
            prob[ord(guess[i])-ord('a')][i] = save
#Can't handle double letters yet
def getResult(guess, answer):
    result = ""
    for i in range(len(guess)):
        #Green
        if guess[i] == answer[i]:
            result += '2'
        #Yellow
        elif answer.count(guess[i]) > 0:
            result += '1'
        #Red
        else:
            result += '0'
    return result
def testOneAnswer(answer):
    debugString = ""
    guess = ""
    iterations = 0
    while(guess != answer):
        guess = getBestWord()
        if guess == "QQQQQ":
            printProb()
            break;
        debugString += "Trying {}!\n".format(guess)
        result = getResult(guess,answer)
        debugString += "Result was {}\n".format(result)
        adjustProb(guess,result)
        iterations += 1
    if iterations > 6:
        debugString += "Failed to guess {} in 6 tries, took {} instead. :(\n".format(answer,iterations)
    return debugString
def testAllAnswers():
    allanswers = open("wordleanswersonly.txt","r")
    for answer in allanswers:
        answer = answer.strip()
        resetProb()
        testOneAnswer(answer) 
def testAnswerFromInput():
    answer = input("Enter answer for testing: ")
    return testOneAnswer(answer)
while True:
    resetProb();
    print(testAnswerFromInput())
