from datetime import datetime
# voice recognition
import speech_recognition as sr
# text to speech
import pyttsx3
# for opening web browser
import webbrowser
# for searching on wikipedia
import wikipedia
import wolframalpha


def speak(text,rate=120):
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()

#speech engine initialization
engine = pyttsx3.init()
#voice selection
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) # 0=man 1=women
activation_word='computer'



appId="YUH6V3-WTVW99XKEK"
wolframalphaClient=wolframalpha.Client(appId)



def parse_commend():
    listener = sr.Recognizer()
    print('listening...')

    with sr.Microphone() as source:
        listener.pause_threshold=2
        input_speech = listener.listen(source)

    try:
        print('recognizing...')
        command = listener.recognize_google(input_speech, language='en_US')
        print(f'the input speech was: {command}\n')
    except Exception as e:
        print('say that again please...')
        speak('say that again please i did not get it')
        print(e)
        return 'None'
    return command


def search_wikipedia(query=""):
    searchResult=wikipedia.search(query)
    if not searchResult:
        print("No result from Wikipedia")
        return "No result from Wikipedia"
    try:
        page=wikipedia.page(searchResult[0])
    except wikipedia.DisambiguationError as err:
        page=wikipedia.page(err.options[0])
    print(page.title)
    summary=str(page.summary)   
    return summary

def listOrDict(var):
    if isinstance(var, list):
        return var[0]['plaintext']
    else:
        return var['plaintext']


def search_wolframAlpha(keyword=''):
    response = wolframalphaClient.query(keyword)
  
    # @success: Wolfram Alpha was able to resolve the query
    # @numpods: Number of results returned
    # pod: List of results. This can also contain subpods

    # Query not resolved
    if response['@success'] == 'false':
        speak('I could not compute')
    # Query resolved
    else: 
        result = ''
        # Question
        pod0 = response['pod'][0]
        # May contain answer (Has highest confidence value) 
        # if it's primary or has the title of result or definition, then it's the official result
        pod1 = response['pod'][1]
        if (('result') in pod1['@title'].lower()) or (pod1.get('@primary', 'false') == 'true') or ('definition' in pod1['@title'].lower()):
            # Get the result
            result = listOrDict(pod1['subpod'])
            # Remove bracketed section
            return result.split('(')[0]
        else:
            # Get the interpretation from pod0
            question = listOrDict(pod0['subpod'])
            # Remove bracketed section
            question = question.split('(')[0]
            # Could search wiki instead here? 
            speak("computing failed, I can search the web for you")
            return search_wikipedia(question)


#Main loop
if __name__=='__main__':
    speak('all systems are ready')
    while True:
        query=parse_commend().lower().split()
        if query[0]==activation_word:
            query.pop(0)
        if query[0]=='say':
            if 'hello' in query:
                speak('hello sir')
            else:
                query.pop(0)
                speak(' '.join(query))
        elif query[0]=='go' and query[1]=='to':
            print('opening...')
            speak('opening...')
            query=' '.join(query[2:])
            webbrowser.open_new(f'https://www.{query}.com')
        elif query[0]=='search':
            print('searching...')
            speak('searching in wikipedia...')
            query=' '.join(query[1:])
            result=search_wikipedia(query)
            print(result)
            speak(result)
        elif query[0]=='calculate':
            query=' '.join(query[1:])
            print('calculating...')
            speak('calculating...')
            try:
                res=search_wolframAlpha(query)
                print(res)
                speak(res)
            except:
                print('Unable to compute')
                speak('Unable to compute')
        elif query[0]=='time':
            print('the time is: ',datetime.now().strftime('%H:%M:%S'))
            speak('the time is: '+datetime.now().strftime('%H:%M:%S'))
        elif query[0]=='date':
            print('the date is: ',datetime.now().strftime('%d/%m/%Y'))
            speak('the date is: '+datetime.now().strftime('%d/%m/%Y'))
        elif query[0]=='note':
            speak("ready for your nots")
            note=parse_commend().lower()
            name=''
            if len(query)>1:
                name=' '.join(query[1:])
            else:
                name='note_'+datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
            with open(f'{name}.txt','a') as f:
                f.write(note)
        elif query[0]=='exit':
            print('exiting...')
            speak('exiting...')
            break