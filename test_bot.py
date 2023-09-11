from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

global chatbot
chatbot=ChatBot('Rho-09',reply_only=True)
###初始化Rho-09

#trainer = ListTrainer(chatbot)
trainer1=ChatterBotCorpusTrainer(chatbot)
trainer2=ListTrainer(chatbot)
#从words文件夹下读取语料
words=[]
files=['zhdd.txt','LCCC01.txt','LCCC02.txt']
count=0
'''
while count <len(files):
    target="words/"+files[count]
    print(target)
    f=open(target,'r',encoding='utf-8')
    while True:

        # Read current line and put content to line
        line = f.readline()
        line=line.strip('\n')
        #print(line)
        #Print the line
        words.append(line)
        if len(words)>=20000:
            trainer2.train(words[:])
            words.clear()
        #If there is no line exit from loop
        if not line:
            f.close()
            break
    count+=1
trainer1.train("chatterbot.corpus.chinese")
'''

while 1:
    question=input("我:")
    result=chatbot.get_response(question)
    print("Rho_09:",result)