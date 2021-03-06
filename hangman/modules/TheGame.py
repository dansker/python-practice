from hangman.modules import methods
import pymysql

conn = pymysql.connect(db='python-hangman', user='python', passwd='python', host='localhost')
cur = conn.cursor()

def hangmanTheGame(name):
    Syntax = ""
    ar = []

    while True:
        if not cur.execute("SELECT word FROM dictionary {} ORDER BY RAND() LIMIT 1".format(Syntax)):
            print("Congratulations! to " + name + " You have beaten the game!")
            break

        randomString = cur.fetchone()[0]
        ar.append(randomString)
        guessedCharacters = []
        characters = methods.character_guess(randomString, guessedCharacters)

        #number of tries
        tries_left = 10

        while tries_left > 0 and "_" in characters:
            print("You have %d live(s) left" % tries_left)
            print(characters)
            i = methods.checkCharacter(input("Guess a character "), guessedCharacters)

            if i == False:
                print("This character is not legal, try another one")
            else:
                if i not in randomString: #if user guess is not in word decrement tries_left by one
                    tries_left -= 1
                    guessedCharacters.append(i)
                    print("you have already guessed %s" % guessedCharacters)
                else:
                    guessedCharacters.append(i)
                    characters = methods.character_guess(randomString, guessedCharacters)

                if not i: #If no input is received, stop the game
                    cur.close()
                    conn.close()
                    return

        print("the word has been guessed")
        Syntax = 'WHERE NOT word IN({})'.format(methods.MySQLWords(ar))


