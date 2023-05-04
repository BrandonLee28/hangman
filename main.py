from flask import Flask, render_template, request,redirect, flash
import requests

app = Flask(__name__)
#get random word#
url = 'https://random-word-api.herokuapp.com/word'
randomword = requests.get(url)

if randomword.status_code == 200:
    # Print the random word
    print(randomword.json()[0])
else:
    print(f"Request failed with status code {randomword.status_code}")
#got random word#
image = 10


s = str(randomword.json()[0])
b = " ".join(s)
print(b)


hiddenword = []
wordlength = len(str(randomword.json()[0])) 
for x in range(wordlength):
    hiddenword.append("_")
hiddenwordstring = " ".join(hiddenword)
error=None



lettersleft = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
lettersguessed =[]

@app.route("/reload")
def reload():
    global error
    global lettersguessed
    global lettersleft
    global image
    global hiddenword
    global hiddenwordstring

    url = 'https://random-word-api.herokuapp.com/word'
    randomword = requests.get(url)

    if randomword.status_code == 200:
        # Print the random word
        print(randomword.json()[0])
    else:
        print(f"Request failed with status code {randomword.status_code}")
    #got random word#
    image = 10
    error = None
    lettersleft = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    lettersguessed =[]
    hiddenword = []
    wordlength = len(str(randomword.json()[0])) 
    for x in range(wordlength):
        hiddenword.append("_")
    hiddenwordstring = " ".join(hiddenword)
    return render_template("index.html", randomword=randomword, lettersleft=lettersleft, hiddenwordstring=hiddenwordstring,image=str(image),lettersguessed=lettersguessed)


def letterappear(letter,count):
    global randomword
    global hiddenwordstring

    randomword1 = randomword.json()[0]
    randomword1 = list(randomword1)
    randomword1 = " ".join(randomword1)
    randomword1 = list(randomword1)
    for x in range(count):
        placecount = randomword1.index(letter)
        randomword1.pop(placecount)
        randomword1.insert(placecount,"_")
        hiddenwordstring = list(hiddenwordstring)
        hiddenwordstring[placecount] = letter
    hiddenwordstring = "".join(hiddenwordstring) 
    


    

def guessright(letter):
    global lettersleft
    #remove from lettersleft
    letterupper = letter.upper()
    x = lettersleft.index(str(letterupper))
    lettersleft.pop(x)

    #add to lettersgueesed
    lettersguessed.append(letterupper)
    count = randomword.json()[0].count(letter)
    print(count)
    letter = letter.casefold()
    letterappear(letter,count)
        



def guesswrong(letter):
    global image
    global lettersleft
    global error
    #remove from lettersleft
    letterupper = letter.upper()
    x = lettersleft.index(str(letterupper))
    lettersleft.pop(x)
    #add to lettersgueesed
    lettersguessed.append(letterupper)
    if image != 0:
        image = image -1
    if image == 0:
        error = "GAME OVER"

@app.route("/",methods=["GET", "POST"])
def index():
    global image
    global randomword
    global lettersleft
    global lettersguessed
    global hiddenword
    global hiddenwordstring
    wordlength = len(str(randomword.json()[0])) 
    global error

    #create a array where people can guess the word

    if request.method == 'POST':
        guess = request.form['guess']
        print(guess)
        guess = guess.casefold()
        if len(str(guess)) == 1 and guess != "_" and guess != " " and lettersguessed.count(guess.upper()) == 0:
            guesscount = randomword.json()[0].count(guess)
            if guesscount >= 1:
                guessright(guess)
                return render_template("index.html", randomword=randomword, lettersleft=lettersleft, hiddenwordstring=hiddenwordstring,image=str(image),lettersguessed=lettersguessed)
            else:
                guesswrong(guess)
                return render_template("index.html", randomword=randomword, lettersleft=lettersleft, hiddenwordstring=hiddenwordstring,image=str(image),lettersguessed=lettersguessed, error=error)
        else:
            return render_template("index.html", randomword=randomword, lettersleft=lettersleft, hiddenwordstring=hiddenwordstring,image=str(image),lettersguessed=lettersguessed)



    return render_template("index.html", randomword=randomword, lettersleft=lettersleft, hiddenwordstring=hiddenwordstring,image=str(image),lettersguessed=lettersguessed, error=error)




if __name__ == "__main__" :
    app.run(debug=True)