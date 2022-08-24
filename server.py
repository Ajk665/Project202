import socket
from threading import Thread

import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address, port))
server.listen()

list_of_clients = []
nicknames = []

questions = ['What was Meta Platforms Inc formerly known as? \n a.Whatsapp \n b.Twitter \n c.Facebook \n d.Messenger', 
'Which English city is known as the Steel City? \n a.Manchester \n b.Sheffield \n c.London \n d.Leeds'
]
answers = ['c', 'b']

print("Server has started...")

def clientthread(conn, nickname):
    score = 0
    conn.send("Welcome to this quizgame!".encode('utf-8'))
    conn.send("Now you will receive general knowledge questions!".encode('utf-8'))
    conn.send("And you have to choose the correct answer!".encode('utf-8'))
    index, questions, answers = getRandomQuestions(conn) 
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if(message.split(":")[-1].lower() == answers):
                    score += 1
                    conn.send("Your score is {score}".encode('utf-8'))
                else:
                    conn.send("Incorrect answer, better luck next time".encode('utf-8'))
                removeQuestion(index)
                index, questions, answers = getRandomQuestions(conn)
                print(answers) 
            else:
                remove(conn)
                remove_nickname(nickname)
        except Exception as e:
            print(str(e))
            continue

def getRandomQuestions(conn):
    randomIndex = random.randint(0, len(questions) -1)
    randomQuestion = questions[randomIndex]
    randomAnswer = answers[randomIndex]
    conn.send(randomQuestion.encode('utf-8'))
    return randomIndex, randomQuestion, randomAnswer

def removeQuestion(index):
    questions.pop(index)
    answers.pop(index)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)

while True:
    conn, addr = server.accept()
    conn.send('NICKNAME'.encode('utf-8'))
    nickname = conn.recv(2048).decode('utf-8')
    list_of_clients.append(conn)
    nicknames.append(nickname)
    message = "{} joined!".format(nickname)
    print(message)
    new_thread = Thread(target= clientthread,args=(conn, nickname))
    new_thread.start()
