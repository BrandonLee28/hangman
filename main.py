from flask import Flask, render_template, request,redirect
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
randomwordpresent = " ".join(s)


hiddenword = []
wordlength = len(str(randomword.json()[0])) 
for x in range(wordlength):
    hiddenword.append("_")
hiddenwordstring = " ".join(hiddenword)


lettersleft = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
lettersguessed =[]

def letterappear(letter,count):
    global randomwordpresent
    global randomword
    global hiddenwordstring

    randomword1 = randomwordpresent
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
    #remove from lettersleft
    letterupper = letter.upper()
    x = lettersleft.index(str(letterupper))
    lettersleft.pop(x)
    #add to lettersgueesed
    lettersguessed.append(letterupper)
    if image != 0:
        image = image -1

@app.route("/",methods=["GET", "POST"])
def index():
    global image
    global randomword
    global lettersleft
    global lettersguessed
    global hiddenword
    global hiddenwordstring
    global randomwordpresent

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
                return render_template("index.html", randomword=randomword, lettersleft=lettersleft, hiddenwordstring=hiddenwordstring,image=str(image),lettersguessed=lettersguessed)
        else:
            return render_template("index.html", randomword=randomword, lettersleft=lettersleft, hiddenwordstring=hiddenwordstring,image=str(image),lettersguessed=lettersguessed)



    return render_template("index.html", randomword=randomword, lettersleft=lettersleft, hiddenwordstring=hiddenwordstring,image=str(image),lettersguessed=lettersguessed)




if __name__ == "__main__":
    app.run(debug=True)