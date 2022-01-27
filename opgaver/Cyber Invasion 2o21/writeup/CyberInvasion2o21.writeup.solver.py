import requests
import base64

api_url = "http://172.16.44.130:3000/"

g_currentSequenceNumber = 1


def SendScore(api_url, increaseScoreBy) :
    global g_currentSequenceNumber

    sendMe1 = str(g_currentSequenceNumber) + ":" + str(increaseScoreBy)

    g_currentSequenceNumber = g_currentSequenceNumber + 1

    sendMe2 = b''
    for c in sendMe1 :
        c = bytes( chr(ord(c) ^ 3), 'ascii')
        sendMe2 += c
    sendMe3 = base64.b64encode(sendMe2).decode('utf-8')

    response = requests.get(api_url + "increase_score/" + sendMe3)
    print(response.content)



response = requests.get(api_url + "clear_current_score")
print(response.content)

for i in range(0, 1002) :
    SendScore(api_url, 1000)
