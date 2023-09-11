##python 3.10.4/3.7.9

import itchat,time,threading,os
from winsound import MB_ICONQUESTION,Beep


import text_respond_person as TRP
import text_respon_group as TRG
import public as PB
import others as OT
from text_respond_person import learn_talk,image_nums

######! 风险事项:thread的setdaemon即将弃用 要用attribute代替
#///*import tkinter   tkinter 在线程中不好操作用windows弹窗替代
#* 考虑到兼容性问题和必要性,取消弹窗功能.
##? 用户隔离的实现方法是否需要改进
##? 命名规则有无必要调整
#todo 内存分析
#///todo  
#doing 实现对方可以自定义的自动回复,实现群友可以自定义的自动回复[会话]
#useless #///todo 修复群聊发起签到bug 

'''Rho-09 已弃用
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer



###初始化Rho-09

#trainer = ListTrainer(chatbot)
trainer1=ChatterBotCorpusTrainer(chatbot)
trainer2=ListTrainer(chatbot)


#从words文件夹下读取语料
words=[]
files=['zhdd.txt','LCCC01.txt','LCCC02.txt']
count=0
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

global stop_reply
global myUserName
stop_reply=False
myUserName=""

@itchat.msg_register(itchat.content.TEXT,isGroupChat=False)#普通非群聊信息
def text_reply(msg):#msg是收到的text类消息
    global stop_reply
    global myUserName
    PB.message_record(msg,myUserName)   
    stop_reply=PB.control(msg,stop_reply)#检验是否是控制台相关指令,并做出相应操作
    if stop_reply==False:#杳泽是否要暂停程序
        #msg_output = json.dumps(msg, indent=4,ensure_ascii=False, sort_keys=False,separators=(',', ':'))
        #print(msg_output)
        trigger=1
        trigger2=1
        if msg['ToUserName']!="filehelper":#表明不是自己发给文件传输助手的
            From_name=msg['User']['RemarkName']#发送人备注   
            trigger*=TRP.start_repeat(msg,From_name)
            trigger*=TRP.emergency(msg)
            trigger*=TRP.others(msg)
            trigger*=TRP.do_not_repeat(msg,From_name)
            trigger2=TRP.repeat(msg,From_name)
            trigger*=TRP.wsh(msg,From_name)
            trigger*=TRP.lists_of_maker(msg)
            trigger*=TRP.chatter(msg)
            trigger*=TRP.relieve(msg)
            trigger*=TRP.ambition(msg)
            #trigger*=TRP.love(msg)
            trigger*=TRP.def_own_reply_start(msg)
            trigger*=TRP.def_own_reply(msg)
            trigger*=PB.use_def_reply(msg)
            trigger*=TRP.recite_helper(msg)
            if trigger2==1:
                trigger=TRP.repeat_file(msg,From_name)
            #trigger=TRP.frog_520(msg)
            if trigger==1 and trigger2==1:#触发标准回复
                PB.standard_reply(msg,From_name)
    return



@itchat.msg_register([itchat.content.TEXT,itchat.content.PICTURE, itchat.content.RECORDING, itchat.content.ATTACHMENT, itchat.content.VIDEO,itchat.content.MAP,itchat.content.CARD,itchat.content.SHARING],isGroupChat=True)#群内任意消息
def group_reply(msg):
    global stop_reply
    global myUserName
    trigger=1
    if stop_reply==False:#杳泽是否要暂停程序
        trigger*=TRG.wsh_resume(msg)
        trigger*=TRG.OCR_group_start(msg)
        trigger*=TRG.chatter(msg)
        trigger*=TRG.def_own_reply_start(msg)
        trigger*=TRG.def_own_reply(msg)
        trigger*=TRG.use_def_reply(msg)
        trigger*=TRG.menu(msg)
        trigger*=TRG.exif_start(msg)
        if trigger==True:
            TRG.standard_reply_group(msg)
        ###发起签到模块还存在bug 1、chatroomowner不一定存在 2、不同群的签到信息同步了  3、昵称未和username绑定
        if msg.text=="发起签到":#发起签到目前在维护
            itchat.send_msg("发起签到目前在修复bug中...剩余3个bug",msg['User']['UserName'])
        '''
        if msg['User']['NickName']=='明日派蒙的魔法学院':#如果是mjq的群
            print("mjq的群")
            TRG.signin_start(msg,"氨基酸")
            TRG.signin(msg)
            TRG.signin_end(msg,"氨基酸")
        if msg['User']['NickName']=='test':#kzc群
            print("kzc群")
            TRG.signin_start(msg,"菠萝蜜刺客")
            TRG.signin(msg)
            TRG.signin_end(msg,"菠萝蜜刺客")
        if msg['User']['NickName']=='三林伞兵号':#如果是三林伞兵号这个群
            print("wj群")
            TRG.signin_start(msg,"哈里不是凯恩")
            TRG.signin(msg)
            TRG.signin_end(msg,"哈里不是凯恩")
        '''
        #TRG.auto_reply(msg)
    return


@itchat.msg_register([itchat.content.PICTURE, itchat.content.RECORDING, itchat.content.ATTACHMENT, itchat.content.VIDEO,itchat.content.MAP,itchat.content.CARD,itchat.content.SHARING],isGroupChat=False)
def download_files(msg):
    global learn_talk
    global image_nums
    global stop_reply
    global myUserName
    trigger=True
    if image_nums<51 and msg['FromUserName']!=myUserName:#将对方发的文件下载下来   一次最多下载50个文件
        download_result=msg.download(os.path.split(os.path.realpath(__file__))[0]+'\\downloaded_files\\'+msg.fileName)
        image_nums+=1
    if stop_reply==False:#杳泽是否要暂停程序
        # 'RemarkName' in msg['User']
        From_name=msg['User']['RemarkName']#发送人备注
        if From_name in learn_talk:
            if learn_talk[From_name]==True:#如果开启了 学我说话 功能
                TRP.repeat_file(msg,From_name)
                trigger=False
        if trigger==True:
            PB.standard_reply(msg,From_name)
    return 


@itchat.msg_register(itchat.content.PICTURE,isGroupChat=True)
def group_reply_pic(msg):
    TRG.OCR_group(msg)
    TRG.exif(msg)
    return

itchat.auto_login(hotReload=True)
#登录后
try:
    thread1=threading.Thread(target=PB.keep_online)
    thread1.setDaemon(True)
    thread1.start()
except:
    print('线程启动失败')
myUserName=itchat.search_friends()['UserName']#获取我自己此次登录后的UserName
PB.load_reply()
TRG.list_before=TRG.load_reply_group()
#print(myUserName)
#OT.who_delete_me()  未完工
#print(itchat.search_chatrooms("明日派蒙的魔法学院"))
itchat.run()