import requests
import base64
import random

# lines 6-34 are set up, obtaining authorization
client_key = '2dZuQOlHnq0PGmnAhuBc5tayR'
client_secret = 'xsXjfmq9rY0KpAF2j4ERmvrzNxaGdcIm62G6AgdEN1yhblBoRl'
#Reformat the keys and encode them
key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')

# Transform from bytes to bytes that can be printed
b64_encoded_key = base64.b64encode(key_secret)
#Transform from bytes back into Unicode
b64_encoded_key = b64_encoded_key.decode('ascii')

base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)
auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}
auth_data = {
    'grant_type': 'client_credentials'
}
auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)

access_token = auth_resp.json()['access_token']

search_headers = {
    'Authorization': 'Bearer {}'.format(access_token)
}
search_params = {
    'result_type': 'recent',
}

# get user input for which two users they would like to compare
username1 = input("Enter the first twitter username\n")
username2 = input("Enter the second twitter username\n")

# Create the URLs
search_url1 = '{}1.1/statuses/user_timeline.json?screen_name={}&count=3200'.format(base_url, username1)
search_url2 = '{}1.1/statuses/user_timeline.json?screen_name={}&count=3200'.format(base_url, username2)

# Execute the get requests
search_resp_user1 = requests.get(search_url1, headers=search_headers, params=search_params)
search_resp_user2 = requests.get(search_url2, headers=search_headers, params=search_params)
# Get the data from the request
tweet_data_user1 = search_resp_user1.json()
tweet_data_user2 = search_resp_user2.json()

timesPlay = int(input("How many tweets would you like to guess?\n"))

# check if there are tweets for each user that don't include mentions or links
found = False
for i in range(len(tweet_data_user1) - 1):
    if not 'http' in (tweet_data_user1[i])['text'] and not '@' in (tweet_data_user1[i])['text']:
        found = True

if not found:
    timesPlay = 0
    print("Sorry, " + username1 + " doesn't have any recent tweets without mentions or links\n")
    print("Try again with a different user")

found = False
for i in range(len(tweet_data_user2) - 1):
    if not 'http' in (tweet_data_user2[i])['text'] and not '@' in (tweet_data_user2[i])['text']:
        found = True

if not found:
    timesPlay = 0
    print("Sorry, " + username2 + " doesn't have any recent tweets without mentions or links\n")
    print("Try again with a different user\n")


numCorrect = 0
numWrong = 0

for num in range(timesPlay):

    # randomly choose one of two users each round
    which = random.randint(0, 1)
    if which == 0:
        var = (tweet_data_user1[random.randint(0, len(tweet_data_user1)-1)])['text']
        # exclude tweets with user mentions or links
        while 'http' in var or '@' in var:
            var = (tweet_data_user1[random.randint(0, len(tweet_data_user1)-1)])['text']
        print('Next tweet: \n' + var)
        user = username1

    else:
        var = (tweet_data_user2[random.randint(0, len(tweet_data_user2)-1)])['text']
        # exclude tweets with user mentions or links
        while 'http' in var or '@' in var:
            var = (tweet_data_user2[random.randint(0, len(tweet_data_user2)-1)])['text']
        print('Next tweet: \n' + var)
        user = username2

    guess = input("\nWhich user do you think wrote this tweet?\n")
    if guess == user:
        print("Correct!\n")
        numCorrect += 1
    else:
        print("Sorry, that's wrong\n")
        numWrong += 1

print('GAME OVER! YOUR STATS: \nCorrect guesses: ' + str(numCorrect) + '\nWrong guesses: ' + str(numWrong) + '\nTotal guesses: ' + str(numCorrect+numWrong))

