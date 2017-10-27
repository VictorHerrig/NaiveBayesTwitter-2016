from twython import Twython
from twython import TwythonStreamer
import json
import re
import random
import NaiveBayes

TARGET = []#["cbellantoni", "Atrios", "nicopitney", "ggreenwald", "wonkroom", 
          #"stevebenen", "AlanColmes", "nathandaschle", "ewerickson", "mindyfinn", 
          #"dmataconis", "TPCarney", "jbarro", "Heminator", "reihansalam", 
          #"RepublicanStudy"]
with open("accounts.json") as findFile:
    TARGET = (json.loads(findFile.read()))


with open('credentials.json') as authenFile:
    keys = json.load(authenFile)

CONSUMER_KEY = keys['CONSUMER_KEY']
CONSUMER_SECRET = keys['CONSUMER_SECRET']
ACCESS_TOKEN = keys['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = keys['ACCESS_TOKEN_SECRET']
tweets = []
APP_KEY = CONSUMER_KEY
APP_SECRET = CONSUMER_SECRET
stopwords = re.compile('-' '|^the$' '|^to$' '|you' '|^a$' '|^in$' '|^an$' '|^and$' 
                       '|^i$' '|^for$' '|^of$' '|^it$' '|^on$' '|^be$' '|^is$' 
                       '|^was$' '|^by$' '|^at$' '|^have$' '|^that$' '|^from$' 
                       '|^are$' '|^so$' '|&amp' '|^as$' '|^am$' '|^been$' '|^would$' 
                       '|^from$' '|^had$'  '|^but$' '|^it.$' '^isn\'t$' '|^had$' 
                       '|^doesn\'t$' '|^has$' '|^this$' '|^RT$' '|^with$''|^can$' 
                       '|^not$' '|\\\\' '|will' '|^our$' '|^we$' '|^does$' '|^do$' 
                       '|^us$' '|^or$''|^her$' '|^out$' '|^now$' '|http' '|\\n' 
                       '|^she$' '|^if$')

twitter = Twython(APP_KEY, APP_SECRET)
auth = twitter.get_authentication_tokens()
OAUTH_TOKEN = auth['oauth_token']
OAUTH_TOKEN_SECRET = auth['oauth_token_secret']
#print(auth['auth_url'])



class myStreamer(TwythonStreamer):
    def on_success(self, data):
        #if data['lang'] == 'en':
        tweets.append(data)
        print('recieved tweet #', len(tweets))
        if len(tweets) >= 1000:
            self.disconnect()

    def on_error(self, status_code, data):
        print(status_code,data)
        self.disconnect()

def getUsers():
    ids = ""
    users = []
    stream = myStreamer(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    for x in range (0, 10):
        for i in range (0, 100):
            randid = random.randint(1, 2147483647) *100000 + random.randint(1, 2147483647)
            ids += str(randid) + ", "
        try:
            users.append(twitter.lookup_user(user_ids = ids)['id_str'])
        except:
            pass
    print(users)
    #for id in users:
    #    getTweets(id, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    
def getTweets(targetUser, cKey, cSec, aTok, aTokSec):
    #fixed
    #ids = set()#debugging
    #total = []#debugging
    stream = myStreamer(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    wordDict = dict()
    hashtagDict = dict()
    wordSet = set()
    idCount = 0
    #Initialize the tweet ID counter
    user_timeline = twitter.get_user_timeline(screen_name = targetUser,count = 1)
    for aTweet in user_timeline:
        idCount = aTweet['id_str']
    x = 0
    #Get tweets in 16 goes, groups of 200
    for i in range(0,16):
        user_timeline = twitter.get_user_timeline(screen_name = targetUser,count  = 200, 
                                                max_id = idCount, include_rts = False)
        for tweet in user_timeline:
            idCount = tweet['id_str']       #Record the tweet ID
            oneTweet = (str(tweet['text'].encode('utf-8')).split()) #Get all the words in the tweet
            oneTweet[0]  = oneTweet[0][2:]      #Ditch the first 2 characters of the first word
            #Add words pairs
            #pairs = []
            #for i in range(1, len(oneTweet)):
            #    pairs.append(oneTweet[i - 1] + " " + oneTweet[i])
            #for element in pairs:
            #    oneTweet.append(element)
            #print(oneTweet)#debugging
            for words in oneTweet:
                #Generalize words
                words = str.lower(words)
                if re.match('.*\'s$', words):
                    words = words[:-2]
                elif re.match('.*:$', words):
                    words = words[:-1]
                #Check if it's a hashtag
                elif re.match('^#.*', words):
                    if not hashtagDict.get(words):
                        hashtagDict[words] = 1
                        #print('new: ', words)#debugging
                    else:
                        hashtagDict[words] += 1
                        #print('adding: ', words)#debugging
                #Check for stopwords
                elif re.search('http', words) or re.match('^@\S*', words) or re.match('^\"@\S*', words) or re.match('^\"', words) or re.search(stopwords, words):
                    continue
                    #print('skipping :', words)#debugging
                #If not, add it to the normal words dict
                elif not wordDict.get(words):
                    wordDict[words] = 1
                    #print('new :', words)#debugging
                else:
                    wordDict[words] += 1
                    #print('adding: ', words)#debugging
            #ids.add(tweet['id_str'])#debugging
            #total.append(tweet['id_str'])#debugging

    #Get rid of normal words that were only used a few times - fixed
    unimportantWords = []
    for elements in wordDict:
        if wordDict[elements] < 20:
            unimportantWords.append(elements)
    for elements in unimportantWords:
        if wordDict.get(elements):
            del(wordDict[elements])
    unimportantWords = []
    for elements in hashtagDict:
        if hashtagDict[elements] < 5:
            unimportantWords.append(elements)
    for elements in unimportantWords:
        if hashtagDict.get(elements):
            del(hashtagDict[elements])

    for elements in wordDict:
        wordSet.add(elements)
    wordSetList = [word for word in wordSet]
    #Print out to a json
    filename = targetUser + '.json'
    with open(filename, 'w') as outFile:
        #json.dump(wordDict, outFile)
        #json.dump(hashtagDict, outFile)
        json.dump(wordDict, outFile)
    filename = targetUser + 'Hashtags.json'
    with open(filename, 'w') as outFi:
        json.dump(hashtagDict, outFi)
    filename = targetUser + 'Set.json'
    with open(filename, 'w') as outF:
        json.dump(wordSetList, outF)

#****************************************************#
#*******************Program Begins*******************#
#****************************************************#
#getUsers()
for user in TARGET:
    getTweets(user, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
#
