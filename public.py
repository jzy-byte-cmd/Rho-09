import time,itchat,threading,os,datetime
import random

import text_respon_group as TRG
global beeping
beeping=True

global replied
global Banned_Friends
global def_reply#所有人的自定义回复内容
global def_reply_num#每个人的自定义回复的第几个


replied=['none']
Banned_Friends=['none']
def_reply={}
def_reply_num={}


def replied_remove(remove):#每15min移除已回复名单
    global replied
    time.sleep(900)
    replied.remove(remove)
    return




def keep_online():#每5min向文件传输助手发送信息以保证持续在线
    while 1:
        itchat.send_msg('..',toUserName='filehelper')
        time.sleep(300)
    return



def standard_reply(msg,From_name):#标准回应  4个参数
    global Banned_Friends,replied
    if (not(From_name in Banned_Friends)) and (not From_name in replied):
        reply='''[托管程序]本人现在没法及时看微信,有事留言就好.
        \n[如果有急事可以回复:有急事,托管程序会通知本人]\n其他选项请回复:其他'''
        if not (From_name in replied): #如果已回复名单里没有这个人
            replied.append(From_name)#加入已回复名单 避免每句话都回复
        try:
            thread3=threading.Thread(target=replied_remove,args=(From_name,))
            thread3.setDaemon(True)
            thread3.start()
        except:
            print('线程3:   ',From_name,'  error')
        itchat.send_msg(reply,msg['FromUserName'])
        return
        #msg_output = json.dumps(msg, indent=4,ensure_ascii=False, sort_keys=False,separators=(',', ':'))
        #print(msg_output)
    return


 
def control(msg,stop_now):#杳泽的控制台  运用文件传输助手   函数在主线程里
    if msg.text!="..":#不是.. [..是用来保持在线的内容]
        if msg['ToUserName']=="filehelper":#表明是我发给文件传输助手的信息  
            if msg.text=="exit":#表明我要退出程序
                print("exiting...")
                itchat.logout()#登出账号
                os._exit(0)#退出程序
            if msg.text=="wait" or msg.text=="W":#表明我要接管微信,暂停程序
                print("start waiting...")
                return True
                #计划0516 (已弃用):用线程解决.弃用原因:实现起来较复杂,且占用资源
            if msg.text=="continue" or msg.text=="C":#表明我要下线,让程序继续运作
                print("stop waiting...")
                return False
            if msg.text=='OCR stop':#停止OCR使用
                print("ocr has been stopped.")
                TRG.ocr_stop_all=True
                #print(ocr_stop_all)
            if msg.text=='OCR continue':#停止OCR使用
                print("ocr continue.")
                TRG.ocr_stop_all=False
                #print(ocr_stop_all)
    return stop_now



def message_record(msg,myUserName):#记录对话
    global beeping
    day_time=str(datetime.datetime.now().date())#记录当前日期
    if msg['FromUserName']==myUserName and msg['ToUserName']!='filehelper':#如果是我发给别人的,并且不是发给文件传输助手
        beeping=False#停止有急事的响铃
        if 'RemarkName' in msg['User']:#如果对方有备注
            file=open(os.path.split(os.path.realpath(__file__))[0]+'\\dialogue\\'+day_time+msg['User']['RemarkName']+'.txt',encoding='utf_8',mode='a')
            file.write("杳泽:"+msg.text+'\n')
            print('                 杳泽','->',msg['User']['RemarkName'],":")#打印我发送的内容
            print("                 ",msg.text)
            print()
        else:#否则显示他的微信名
            file=open(os.path.split(os.path.realpath(__file__))[0]+'\\dialogue\\'+day_time+msg['User']['NickName']+'.txt',encoding='utf_8',mode='a')
            file.write("杳泽:"+msg.text+'\n')
            print('                 杳泽','->',msg['User']['NickName'],":")#打印我发送的内容
            print("                 ",msg.text)
            print()
        file.close()
    else:
        if msg['ToUserName']=='filehelper':#我如果发给了文件传输助手
            #beeping=False#停止有急事的响铃
            print('                 ',"杳泽",'->',"文件传输助手:")#打印发送的内容
            print('                 ',msg.text)
            print()
        else:
            if msg['FromUserName']!=myUserName:#如果是别人发给我的
                if 'RemarkName' in msg['User']:#如果我给对方备注了
                    file=open(os.path.split(os.path.realpath(__file__))[0]+'\\dialogue\\'+day_time+msg['User']['RemarkName']+'.txt',encoding='utf_8',mode='a')
                    file.write(msg['User']['RemarkName']+":"+msg.text+'\n')
                    print(msg['User']['RemarkName']+'->',"杳泽:")#打印发送的内容
                    print(msg.text)
                    print()
                else:#没给备注
                    file=open(os.path.split(os.path.realpath(__file__))[0]+'\\dialogue\\'+day_time+msg['User']['NickName']+'.txt',encoding='utf_8',mode='a')
                    file.write(msg['User']['NickName']+":"+msg.text+'\n')
                    print(msg['User']['NickName'],'->',"杳泽:")#打印发送的内容
                    print(msg.text)
                    print()
            file.close()
    return


def load_reply():#加载自定义回复
    global def_reply
    global def_reply_num
    line_num=0
    nickname=''
    files=os.listdir(os.path.split(os.path.realpath(__file__))[0]+'\\def_reply\\')
    for target in files:
        file=open(os.path.split(os.path.realpath(__file__))[0]+'\\def_reply\\'+target,encoding='utf_8',mode='r')
        while 1:
            line = file.readline()
            line=line.strip('\n')
            if line_num==0:#第一行存的是nickname
                nickname=line
                if not (line in def_reply_num):#还没有存这个人的自定义回复数
                    def_reply[nickname]=[[]]
                    def_reply_num[nickname]=0#记录第一个回复
                else:
                    def_reply[nickname].append([])
                    def_reply_num[nickname]+=1#增加一个回复数
            else:#不是第一行
                def_reply[nickname][def_reply_num[nickname]].append(line)
            line_num+=1
            if not line:
                def_reply[nickname][def_reply_num[nickname]].pop()
                nickname=''
                line_num=0
                break
        file.close()
    print("person:\n",def_reply)
    return


def use_def_reply(msg):
    global def_reply
    possible_answer=[]
    if msg['User']['NickName'] in def_reply:#这个人有自定义回复
        #print("has")
        for num1 in range(len(def_reply[msg['User']['NickName']])):
            if def_reply[msg['User']['NickName']][num1][3]=='on':#如果是开启状态
                #print("on √")
                if def_reply[msg['User']['NickName']][num1][0]=='word':#关键词识别
                    #print("confirm word")
                    #print(def_reply[msg['User']['NickName']][num1][1])
                    if def_reply[msg['User']['NickName']][num1][1] in msg.text:#识别到关键词
                        #print("identified")
                        possible_answer.append(def_reply[msg['User']['NickName']][num1][2])
                    continue
                if def_reply[msg['User']['NickName']][num1][0]=='sentence':#整句识别
                    #print("confirm sentence")
                    #print(len(def_reply[msg['User']['NickName']][num1]))
                    #print(def_reply[msg['User']['NickName']][num1][1])
                    if def_reply[msg['User']['NickName']][num1][1]==msg.text:#
                        possible_answer.append(def_reply[msg['User']['NickName']][num1][2])
                    continue
                if def_reply[msg['User']['NickName']][num1][0]=='special':#特殊句式识别
                    #print("confirm special")
                    possible=True
                    if len(msg.text)==len(def_reply[msg['User']['NickName']][num1][1]):#表明可能能通过特殊句式识别
                        for num3 in range(len(def_reply[msg['User']['NickName']][num1][1])):#遍历整个特殊句式要求
                            # #表示任意英文字符,%表示任意中文字,*表示任意字符\
                            #,<表示任意数字,>表示任意标点符号
                            if def_reply[msg['User']['NickName']][num1][1][num3]=='*':#表明这个位置是任意字符
                                continue
                            if def_reply[msg['User']['NickName']][num1][1][num3]=='%':#表明必须是中文字
                                if '\u4e00' <= msg.text[num3] and msg.text[num3]<= '\u9fff':#表明是中文字
                                    continue
                                else:
                                    possible=False
                                    break#特殊句式识别失败
                            if def_reply[msg['User']['NickName']][num1][1][num3]=='#':#表明必须是任意英文字符
                                if (ord(msg.text[num3])>=65 and ord(msg.text[num3])<=90) or (ord(msg.text[num3])>=97 and ord(msg.text[num3])<=122):#表明是任意英文字符
                                    continue
                                else:
                                    possible=False
                                    break#特殊句式识别失败
                            if def_reply[msg['User']['NickName']][num1][1][num3]=='<':#表明必须是任意数字
                                if ord(msg.text[num3])<=57 and ord(msg.text[num3])>=48:#表明确实是任意数字
                                    continue
                                else:
                                    possible=False
                                    break
                            if def_reply[msg['User']['NickName']][num1][1][num3]=='>':#表明必须是任意标点符号
                                if (ord(msg.text[num3])>=33 and ord(msg.text[num3])<=47) or \
                                    (ord(msg.text[num3])>=58 and ord(msg.text[num3])<=64) or \
                                    (ord(msg.text[num3])>=91 and ord(msg.text[num3])<=96) or \
                                    (ord(msg.text[num3])>=123 and ord(msg.text[num3])<=127):#表明确实是任意标点符号
                                    continue
                                else:
                                    possible=False
                                    break
                            if def_reply[msg['User']['NickName']][num1][1][num3]!='>' and \
                                def_reply[msg['User']['NickName']][num1][1][num3]!='#' and \
                                def_reply[msg['User']['NickName']][num1][1][num3]!='*' and \
                                def_reply[msg['User']['NickName']][num1][1][num3]!='<' and \
                                def_reply[msg['User']['NickName']][num1][1][num3]!='%':#表明这就直接是一个字符或字
                                if msg.text[num3]==def_reply[msg['User']['NickName']][num1][1][num3]:#能匹配上
                                    continue
                                else:
                                    possible=False
                                    break
                    else:
                        possible=False
                    if possible==True:
                        possible_answer.append(def_reply[msg['User']['NickName']][num1][2])
        if len(possible_answer)>0:
            reply_target_num=random.randint(0,len(possible_answer)-1)#随机选一个回复
            itchat.send_msg(possible_answer[reply_target_num],msg['FromUserName'])
            return False
        else:
            return True
    return True


