from flask import Flask, render_template, request, flash
import random
import re
import kmeans

app = Flask(__name__)
app.secret_key = 'some_secret_key'  # Required for flashing messages

YOUTUBE_LINK_PATTERN = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'

@app.route('/', methods=['GET', 'POST'])
def index():
    wordsList=None
    quesList=None
    if request.method=='POST':
        wordsOutput=open("kmeansOutput.txt")
        questionsOut= open('questionsOutput.txt')

        tempList=[]
        wordsList=[]
        for line in wordsOutput:
            if(line=="][\n"):
                wordsList.append(tempList)
                tempList=[]
                continue
            if(line=="[\n"):
                continue
            else:
                tempList.append(line)
        wordsList.append(tempList)
        
        tempList=[]
        quesList=[]

        for line in questionsOut:
            if(line=="][\n"):
                quesList.append(tempList)
                tempList=[]
                continue
            if(line=="[\n"):
                continue
            else:
                tempList.append(line)
        quesList.append(tempList)
        wordsOutput.close()
        questionsOut.close()
    return render_template('content.html', text=wordsList, ques=quesList)
    
    
    number = None
    energy_message = None
    
    if request.method == 'POST':
        youtube_link = request.form.get('youtube_link')
        
        if not re.match(YOUTUBE_LINK_PATTERN, youtube_link):
            flash('Please enter a valid YouTube link.', 'error')
        else:
            number = random.randint(1, 99)
            
            if number <= 33:
                energy_message = "This video has less number of questions."
            elif number <= 66:
                energy_message = "This video has a moderate level ofs questions"
            else:
                energy_message = "This video has a lot of Questions"
                
    return render_template('index.html', number=number, energy_message=energy_message)

if __name__ == '__main__':
    app.run(debug=True)

