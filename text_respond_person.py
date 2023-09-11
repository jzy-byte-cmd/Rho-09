import itchat,time,threading,json,os,sys#,win32api,win32con,win32gui,pythoncom,win32com.client
import datetime,random

'''
import chatterbot,spacy
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
'''
from winsound import MB_ICONQUESTION,Beep
from public import replied_remove
import pyautogui

from public import replied
from public import beeping
import public as PB

global learn_talk#开启学我说话的人
global image_nums#已下载图片数量
global def_reply_person#正在定义自动回复的人
global reply_mode#自定义回复的识别模式
global content#自定义回复的相关内容

#global robot_on
#global chatbot
global online_user
global reciter#正在用单词抽查器的人


online_user=[]
#robot_on=False
#chatbot=ChatBot('Rho-09')
beeping=True
image_nums=0
learn_talk={}
def_reply_person={}
reply_mode={}
content_reply={'me':[]}
reciter={}

def do_not_repeat(msg,From_name):#停止 {学我说话} 功能 
    global learn_talk
    if msg.text=='不要学我说话':
        learn_talk[From_name]=False
        itchat.send_msg('我不会再学你说话啦.',msg['FromUserName'])
        return False#不要触发标准回应
    return True



def start_repeat(msg,From_name):#{学我说话} 功能 
    global learn_talk
    if msg.text=='学我说话':
        learn_talk[From_name]=True
        itchat.send_msg('我要开始学你说话咯~',msg['FromUserName'])
        return False#不要触发标准回应
    return True


def repeat(msg,From_name):#{学我说话} 文字
    global learn_talk
    if From_name in learn_talk:
            if learn_talk[From_name]==True:
                itchat.send_msg(msg.text,msg['FromUserName'])
            return False#不要触发标准回应
    return True




def repeat_file(msg,From_name):#{学我说话}  文件
    global learn_talk
    if From_name in learn_talk:
        if learn_talk[From_name]==True:
            if msg.MsgType==3 or msg.MsgType==47:#表明是图片或动画表情消息
                msg.download(msg.fileName)
                itchat.send_image(msg.fileName,msg['FromUserName'])
                os.remove(msg.fileName)
                return False
            if msg.MsgType==62:#表明是视频
                msg.download(msg.fileName)
                itchat.send_video(msg.fileName,msg['FromUserName'])
                os.remove(msg.fileName)
                return False
            if msg.MsgType==1:#地理位置消息
                itchat.send_msg(msg.text,msg['FromUserName'])
                return False
            if msg.MsgType==42:#名片消息
                itchat.send_msg(msg.text,msg['FromUserName'])
                return False
            if msg.MsgType==34:#语音消息
                msg.download(msg.fileName)
                itchat.send_file(msg.fileName,msg['FromUserName'])
                os.remove(msg.fileName)
                return False
            if msg.MsgType==49 and msg.AppMsgType!=2001:#分享链接消息 2001的AppMsgType为红包消息
                itchat.send_msg(msg.FileName+'\n'+msg.Url,msg['FromUserName'])
                return False
            if msg.MsgType==2001:#红包
                itchat.send_msg("这我可模仿不来吖",msg['FromUserName'])
                return False
    return True




def others(msg):#其它选项
    if msg.text=='其他':
        itchat.send_msg('''
1.回复 学我说话 以让程序模仿你说话.[回复 不要学我说话 以结束].
2.回复 自定义回复  自定义自动回复内容[部分完成]
3.回复 单词抽查器 以抽背单词
4.回复 OCR 以识别图像中[未完成]
5.制作人员名单  回复 制作人员名单
''',msg['FromUserName'])
        return False#不要触发标准回应
    return True




def emergency(msg):#有急事
    
    if msg.text=='有急事':
        d_time1=datetime.datetime.strptime(str(datetime.datetime.now().date()) + '00:30', '%Y-%m-%d%H:%M')#设定时间范围
        d_time2=datetime.datetime.strptime(str(datetime.datetime.now().date()) + '03:30', '%Y-%m-%d%H:%M')
        n_time=datetime.datetime.now()#获取当前时间
        if not (n_time>d_time1 and n_time<d_time2):#如果不是在00:30~3:30呼叫
            itchat.send_msg('正在通知中...请稍等',msg['FromUserName'])
            thread_call=threading.Thread(target=start_beep,args=())
            thread_call.setDaemon(True)
            thread_call.start()
            time.sleep(18)#等18s蜂鸣总长21s
            if thread_call.is_alive():#如果此时作者还没确认线程,那说明通知失败
                itchat.send_msg('通知估计失败了...',msg['FromUserName'])
                return False#不要触发标准回应
            else:
                os._exit(0)#退出程序  线程中退出
        else:#打扰我睡觉
            itchat.send_msg("夜已经深了,有急事功能不可用,有事请留言",msg['FromUserName'])
        return False
    return True




def start_beep():#开始蜂鸣
    for i in range(0,101):#调大系统音量
        pyautogui.press("volumeup")
    counter=0
    global beeping
    while beeping and counter<8:#总共长21s的蜂鸣
        Beep(800,3000)#如果还没关掉这个线程 那就继续beep
        counter+=1
    beeping=True
    return




def wsh(msg,From_name):#wsh的个性化定制服务
    if msg['User']['RemarkName']=='小雪花':#wsh给我发消息
        if not (From_name in replied): #如果已回复名单里没有这个人
            itchat.send_msg('宝,你来了啊.我现在有事情看不了手机.过会儿我会回复你的.',msg['FromUserName'])
            replied.append(From_name)#加入已回复名单 避免每句话都回复
            try:
                thread3=threading.Thread(target=replied_remove,args=(From_name,))
                thread3.setDaemon(True)
                thread3.start()
            except:
                print('线程3:   ',From_name,'  error')
        return False
    return True


def lists_of_maker(msg):#制作人员名单
    if msg.text=="制作人员名单":
        itchat.send_msg('''
程序编写人员:
杳泽--jzy
主要测试人员:
kzc
wsh
mjq
gaven
                        ''',msg['FromUserName'])
        return False
    return True


def frog_520(msg):
    decider=False
    to_who=""
    if msg.text=="给wsh送孤寡青蛙":#有人给wsh送孤寡青蛙
        decider=True
        to_who="wsh,"
        target_username=itchat.search_friends(remarkName='wsh')
    if msg.text=="给djs送孤寡青蛙":#给djs送
        decider=True
        to_who="djs,"
        target_username=itchat.search_friends(remarkName='杜家晟')
    if msg.text=="给kzc送孤寡青蛙":#给kzc送
        decider=True
        to_who="kzc,"
        target_username=itchat.search_friends(remarkName='康周铖')
    if msg.text=="给mjq送孤寡青蛙":#给mjq送
        decider=True
        to_who="mjq,"
        target_username=itchat.search_friends(remarkName='马嘉绮')
    if msg.text=="给lrb送孤寡青蛙":#给lrb送
        decider=True
        to_who="lrb,"
        target_username=itchat.search_friends(remarkName='李若冰')
    if msg.text=="给xzx送孤寡青蛙":#给xzx送
        decider=True
        to_who="xzx,"
        target_username=itchat.search_friends(remarkName='肖子萱')
    if msg.text=="给crq送孤寡青蛙":#给crq送
        decider=True
        to_who="曹哥,"
        target_username=itchat.search_friends(remarkName='曹哥')
    if msg.text=="给sly送孤寡青蛙":#给sly送
        decider=True
        to_who="乐乐,"
        target_username=itchat.search_friends(remarkName='沈乐吟')
    if msg.text=="给gaven送孤寡青蛙":#给gaven送
        decider=True
        to_who="gaven,"
        target_username=itchat.search_friends(remarkName='gaven')
    if msg.text=="给zyt送孤寡青蛙":#给zyt送
        decider=True
        to_who="zyt,"
        target_username=itchat.search_friends(remarkName='赵韵棠')
    if msg.text=="给jzy送孤寡青蛙":#给jzy送
        itchat.send_msg("我谢谢你嗷",msg['FromUserName'])
        return False
    if decider==True:
        #print(target_username)
        if 'RemarkName' in msg['User']:#有备注
            from_who=to_who+msg['User']['RemarkName']+"给你点了孤寡青蛙"
        else:
            from_who=to_who+msg['User']['NickName']+"给你点了孤寡青蛙"
        itchat.send_msg(from_who,target_username[0]['UserName'])
        itchat.send_image("C:\\Users\\jinzh\\Desktop\\code\\python\\微信自动回复\\1.jpeg",target_username[0]['UserName'])
        itchat.send_image("C:\\Users\\jinzh\\Desktop\\code\\python\\微信自动回复\\2.png",target_username[0]['UserName'])
        itchat.send_image("C:\\Users\\jinzh\\Desktop\\code\\python\\微信自动回复\\3.png",target_username[0]['UserName'])
        itchat.send_msg('''孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡
                            孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡
                            孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡''',target_username[0]['UserName'])
        itchat.send_msg('''孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡
                            孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡
                            孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡
                            孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡
                            孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡
                            孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡
                            孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡''',target_username[0]['UserName'])
        itchat.send_msg('''孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡
                            孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡
                            孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡
                            孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡
                            孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡
                            孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡
                            孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡''',target_username[0]['UserName'])
        itchat.send_msg('''孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡
                            孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡
                            孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡
                            孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡
                            孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡
                            孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡
                            孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡
                            孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡
                            孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡
                            孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡
                            孤寡孤寡孤寡孤寡孤寡孤寡孤寡孤寡''',target_username[0]['UserName'])
        itchat.send_msg("期待下次有人给你点孤寡青蛙",target_username[0]['UserName'])
        itchat.send_msg("已送达",msg['FromUserName'])
        return False
    return True


def chatter(msg):#聊天机器人
    global robot_on
    global chatbot
    if msg.text=="Rho-09":#呼叫Rho-09
        itchat.send_msg("Rho-09已废弃,最后一个版本:V0.0.0.20220522_Beta",msg['FromUserName'])
        return False
        ###
        itchat.send_msg("声明:Rho-09回答的结果基于机器学习\n从Rho-09 online 至 Rho-09 offline期间,\
产生的聊天内容均视为Rho-09的发言,不代表本人立场及观点.同时Rho-09会记录您的聊天至数据库\n若您同意并认可上述条款,可回复 Rho-09在吗 \
以开始和Rho-09聊天.",msg['FromUserName'])
        return False
    if msg.text=='Rho-09在吗':
        itchat.send_msg("Rho-09已废弃,最后一个版本:V0.0.0.20220522_Beta",msg['FromUserName'])
        return False
        ###
        itchat.send_msg("Rho-09\n版本:V0.0.0.20220522_Beta\n适配器:\nLevenshtein距离算法\n\
            时间逻辑适配器\n数学评估适配器\nBestMatch适配器\n\
                停用词:True\n语料库:基础.\n备注:这一版本的Rho-09刚刚诞生,还处于测试阶段,目前的回答能力非常有限.\n\n\
                    回复Rho-09再见 以关闭Rho-09",msg['FromUserName'])
        itchat.send_msg("Rho-09 online",msg['FromUserName'])
        itchat.send_msg("你好.",msg['FromUserName'])
        robot_on=True
        online_user.append(msg['FromUserName'])
        return False
    '''
    if robot_on==True and msg['FromUserName'] in online_user:#Rho-09 online
        result=str(chatbot.get_response(str(msg.text)))
        print(result)
        itchat.send_msg(result,msg['FromUserName'])
    '''
    if msg.text=='Rho-09再见':#rho-09 offline
        itchat.send_msg("Rho-09已废弃,最后一个版本:V0.0.0.20220522_Beta",msg['FromUserName'])
        return False
        ###
        itchat.send_msg('Rho_09 offline',msg['FromUserName'])
        robot_on=False
        online_user.remove(msg['FromUserName'])
        return False
    return True


def relieve(msg):#如果有人和我说ta难过
    if '难过' in msg.text and '我' in msg.text:
        itchat.send_msg("抱抱,别难过了.",msg['FromUserName'])
        itchat.send_image('pic/hug.gif',msg['FromUserName'])
        return False
    return True



def ambition(msg):#如果有人问我的志向/想成为什么样的人
    if ('你' in msg.text and '志向' in msg.text and( '什么' in msg.text or '啥' in msg.text)) or \
    (msg.text=='你想成为什么样的人') or (msg.text=='你想成为怎样的人'):
        itchat.send_msg("I would like to be a man of focus,\
            commitment and sheer will.",msg['FromUserName'])
        return False
    return True


def love(msg):#涉及恋爱方面的话题
    if ('恋爱' in msg.text and '谈' in msg.text) or '喜欢' in msg.text or '爱' in msg.text:#可能涉及谈恋爱或喜欢或爱
        itchat.send_msg("智者不入爱河.后半句究竟是\"愚者自甘堕落\",还是\"遇你难做智者,甘愿沦为愚者\"\
            \n这点你要好好考虑清楚.",msg['FromUserName'])
        return False
    return True



def def_own_reply_start(msg):#开始/管理自定义回复
    global def_reply_person
    global content_reply
    if msg.text=='新增自定义回复':#自己创建一个自定义回复
        itchat.send_msg("啊哈,看来你想整点新鲜的",msg['FromUserName'])
        itchat.send_msg("想要退出自定义回复 可回复exit1",msg['FromUserName'])
        def_reply_person[msg['FromUserName']]=0
        return False
    if msg.text=='使用别人的自定义回复':#用别人的自定义回复
        itchat.send_msg("emmm...这个还没写好",msg['FromUsername'])
        #itchat.send_msg("请告诉我那个人的昵称",msg['FromUserName'])
        #^^^^

        return False
    if msg.text=='自定义回复':#询问自定义回复相关的内容
        itchat.send_msg("回复新增自定义回复,\n以自己新创一个自定义回复\n\n回复使用别人的自定义回复,\n以使用别人已经设计好的自定义回复\n\n回复管理自定义回复,\n以管理自己的自定义回复\n\n回复更新自定义回复,\n以将改昵称前的自定义回复连接到现有的昵称",msg['FromUserName'])
        return False
    if msg.text=='更新自定义回复':#更新自己改名前的自定义回复
        itchat.send_msg("emmm...这个还没写好",msg['FromUsername'])
        #itchat.send_msg("请问你先前使用自定义回复时的昵称是什么呢?",msg['FromUserName'])
        #^^^^
        return False    
    if msg.text=='管理自定义回复':
        itchat.send_msg("emmmm....这个还没写好",msg['FromUserName'])
        #^^^^
        return False
    if msg.text=='exit1':#退出自定义回复
        content_reply[msg['FromUserName']].clear()
        def_reply_person[msg['FromUserName']]=-1
        itchat.send_msg("自定义自动回复已退出",msg['FromUserName'])
    return True

def def_own_reply(msg):#自定义回复ing
    global def_reply_person
    global reply_mode
    global content_reply
    if msg['FromUserName'] in def_reply_person:#如果这个人在储存相关名单字典里
        if def_reply_person[msg['FromUserName']]==-1:#如果是没在自定义回复
            return True
        if def_reply_person[msg['FromUserName']]==0:#如果进行到第0步
            itchat.send_msg("那么请问你想我按照哪种方式来回复你呢?\n1.识别关键词\n2.识别整个句子\n3.识别特殊格式的消息\
            \n(请你回复相应数字喔)",msg['FromUserName'])
            def_reply_person[msg['FromUserName']]=1#进行第1步
            return False
        if def_reply_person[msg['FromUserName']]==1:#进行到第1步
            if msg.text !='1' and msg.text !='2' and msg.text !='3':#表明没按照上一步的要求
                itchat.send_msg("啊哦,貌似你没按照要求来喔,我们得重新回到上一步",msg['FromUserName'])
                itchat.send_msg("请问你想我按照哪种方式来回复你呢?\n1.识别关键词\n2.识别整个句子\n3.识别特殊格式的消息\
            \n(请你回复相应数字喔)",msg['FromUserName'])
                return False
            if msg.text =='1':#希望识别关键词
                itchat.send_msg("你希望识别什么关键词呢?",msg['FromUserName'])
                def_reply_person[msg['FromUserName']]=2#进行第2步
                reply_mode[msg['FromUserName']]='word'#识别关键词模式
                return False
            if msg.text =='2':#希望识别整个句子
                itchat.send_msg("你希望识别什么内容呢?(注意:识别的内容必须完全一致才能触发自动回复,标点符号区分全半角,也区分空格)",msg['FromUserName'])
                def_reply_person[msg['FromUserName']]=2#进行第2步
                reply_mode[msg['FromUserName']]='sentence'#识别整个句子模式
                return False
            if msg.text =='3':#希望识别特殊格式的消息
                itchat.send_msg("你希望识别什么特殊格式的消息呢?把格式告诉我吧. #表示任意英文字符, %表示任意中文字, *表示任意字符, <表示任意数字, >表示任意标点符号",msg['FromUserName'])
                itchat.send_msg("例1:\n你##><吧\n[表示识别第一个字为\'你\',最后一个字为\'吧\',中间为任意2个英文字符,任意1个标点符号,任意1个数字](有顺序)]",msg['FromUserName'])
                def_reply_person[msg['FromUserName']]=2#进行第2步
                reply_mode[msg['FromUserName']]='special'#识别关键词模式
                return False
        if def_reply_person[msg['FromUserName']]==2:#进行到第2步
            if reply_mode[msg['FromUserName']]=='word':#如果是识别关键词模式
                itchat.send_msg("你希望我识别到 "+msg.text+" 这个关键词后怎么回复你呢?(直接回复需要回复的内容)",msg['FromUserName'])
                content_reply[msg['FromUserName']]=[]
                content_reply[msg['FromUserName']].append(msg.text)
                def_reply_person[msg['FromUserName']]=3#进行第3步
                return False
            if reply_mode[msg['FromUserName']]=='sentence':#如果是识别整个句子
                itchat.send_msg("你希望我识别到 "+msg.text+" 这句话后怎么回复你呢?(直接回复需要回复的内容)",msg['FromUserName'])
                content_reply[msg['FromUserName']]=[]
                content_reply[msg['FromUserName']].append(msg.text)
                def_reply_person[msg['FromUserName']]=3#进行第3步
                return False
            if reply_mode[msg['FromUserName']]=='special':
                itchat.send_msg("你希望我怎么回答 "+msg.text+" 这类话呢?",msg['FromUserName'])
                content_reply[msg['FromUserName']]=[]
                content_reply[msg['FromUserName']].append(msg.text)
                def_reply_person[msg['FromUserName']]=3#进行第3步
                return False
        if def_reply_person[msg['FromUserName']]==3:#进行到第3步
            itchat.send_msg("啊哈,我们就快完成了",msg['FromUserName'])
            if reply_mode[msg['FromUserName']]=='word':#识别关键词
                content_reply[msg['FromUserName']].append(msg.text)
                itchat.send_msg("预期效果:(*代表任意字符)\n"+msg['User']['NickName']+":**"+content_reply[msg['FromUserName']][0]+"***\n杳泽:"+content_reply[msg['FromUserName']][1],msg['FromUserName'])
                itchat.send_msg("是否保存?(请回复y/n)",msg['FromUserName'])
                def_reply_person[msg['FromUserName']]=4#去第4步
                return False
            if reply_mode[msg['FromUserName']]=='sentence':#识别整个句子
                content_reply[msg['FromUserName']].append(msg.text)
                itchat.send_msg("预期效果:\n"+msg['User']['NickName']+":"+content_reply[msg['FromUserName']][0]+"\n杳泽:"+content_reply[msg['FromUserName']][1],msg['FromUserName'])
                itchat.send_msg("是否保存?(请回复y/n)",msg['FromUserName'])
                def_reply_person[msg['FromUserName']]=4#去第4步
                return False
            if reply_mode[msg['FromUserName']]=='special':#识别特殊句式
                content_reply[msg['FromUserName']].append(msg.text)
                itchat.send_msg("预期效果:\n"+msg['User']['NickName']+":"+content_reply[msg['FromUserName']][0]+"\n杳泽:"+content_reply[msg['FromUserName']][1],msg['FromUserName'])
                itchat.send_msg("是否保存?(请回复y/n)",msg['FromUserName'])
                def_reply_person[msg['FromUserName']]=4#去第4步
                return False
        if def_reply_person[msg['FromUserName']]==4:#进行第4步
            if msg.text!='y' and msg.text!='n' and msg.text!='Y' and msg.text!='N':#表明没按照要求来
                itchat.send_msg("啊哦,貌似你没按照要求来喔,我们得重新回到上一步",msg['FromUserName'])
                if reply_mode[msg['FromUserName']]=='word':#识别关键词
                    itchat.send_msg("预期效果:\n"+msg['User']['NickName']+":**"+content_reply[msg['FromUserName']][0]+"***\n杳泽:"+content_reply[msg['FromUserName']][1],msg['FromUserName'])
                    itchat.send_msg("是否保存?(请回复y/n)",msg['FromUserName'])
                    return False
                if reply_mode[msg['FromUserName']]=='sentence':#识别整个句子
                    itchat.send_msg("预期效果:\n"+msg['User']['NickName']+":"+content_reply[msg['FromUserName']][0]+"\n杳泽:"+content_reply[msg['FromUserName']][1],msg['FromUserName'])
                    itchat.send_msg("是否保存?(请回复y/n)",msg['FromUserName'])
                    return False
                if reply_mode[msg['FromUserName']]=='special':#识别特殊句式
                    itchat.send_msg("预期效果:\n"+msg['User']['NickName']+":"+content_reply[msg['FromUserName']][0]+"\n杳泽:"+content_reply[msg['FromUserName']][1],msg['FromUserName'])
                    itchat.send_msg("是否保存?(请回复y/n)",msg['FromUserName'])
                    return False
            if msg.text=='y' or msg.text=='Y':#确认保存
                itchat.send_msg("好嘞!为了便于管理,请问这套回复要叫什么呢?\n(如果回复 默认,则将这套自定义回复以 模式+内容+时间来自动命名)",msg['FromUserName'])
                def_reply_person[msg['FromUserName']]=5#去第5步
                return False
            if msg.text=='n' or msg.text=='N':#不保存
                itchat.send_msg("好吧,我们重头来过,如果你不想自定义回复了 可以回复exit",msg['FromUserName'])
                def_reply_person[msg['FromUserName']]=1
                itchat.send_msg("那么请问你想我按照哪种方式来回复你呢?\n1.识别关键词\n2.识别整个句子\n3.识别特殊格式的消息\
                \n(请你回复相应数字喔)",msg['FromUserName'])
                content_reply[msg['FromUserName']].clear()
                reply_mode[msg['FromUserName']]=''
                return False
        if def_reply_person[msg['FromUserName']]==5:
            if msg.text!='默认':#如果不是默认
                itchat.send_msg("OK!这套方案已经被命名为"+msg.text+",并且默认开启了",msg['FromUserName'])
                itchat.send_msg("但是要经过审核之后才能生效哈",msg['FromUserName'])
                file=open(os.path.split(os.path.realpath(__file__))[0]+'\\reply_check\\'+msg.text+".txt",encoding='utf_8',mode='w')
                file.write(msg['User']['NickName']+'\n')
                file.write(reply_mode[msg['FromUserName']]+'\n')
                file.write(content_reply[msg['FromUserName']][0]+'\n')
                file.write(content_reply[msg['FromUserName']][1]+'\n')
                file.write('on')
                file.close()
                def_reply_person[msg['FromUserName']]=-1
                content_reply[msg['FromUserName']].clear()
                reply_mode[msg['FromUserName']]=''
                return False
            if msg.text=='默认':#默认名称
                itchat.send_msg("OK!这套方案现在被命名为了"+reply_mode[msg['FromUserName']]+","+content_reply[0]+","+str(datetime.datetime.now())\
                    ,msg['FromUserName'])
                itchat.send_msg("但是要经过审核之后才能生效哈",msg['FromUserName'])
                file=open(os.path.split(os.path.realpath(__file__))[0]+'\\reply_check\\'+reply_mode[msg['FromUserName']]+","+content_reply[0]+","+str(datetime.datetime.now())+".txt",encoding='utf_8',mode='w')
                file.write(msg['User']['NickName']+'\n')
                file.write(reply_mode[msg['FromUserName']]+'\n')
                file.write(content_reply[msg['FromUserName']][0]+'\n')
                file.write(content_reply[msg['FromUserName']][1]+'\n')
                file.write('on')
                file.close()
                def_reply_person[msg['FromUserName']]=-1
                content_reply[msg['FromUserName']].clear()
                reply_mode[msg['FromUserName']]=''
                return False
    return True

def recite_helper(msg):
    global reciter
    if not (msg['FromUserName'] in reciter):#没存对方的名字
        reciter[msg['FromUserName']]={'isReciting':-1}
    if msg.text=='exit2':#退出背单词
        reciter[msg['FromUserName']]['isReciting']=-1
        itchat.send_msg("单词抽查器已退出",msg['FromUserName'])
        return False
    if reciter[msg['FromUserName']]['isReciting']==0:
        msg.text=msg.text.replace('\n',' ')#将换行符替换为空格
        msg.text=msg.text.replace('\t',' ')#将制表符替换为空格
        list1=msg.text.split(' ')
        print(list1)
        reciter[msg['FromUserName']]['content']=list1#存入单词和中文
        list1=[]
        itchat.send_msg("准备已完成,回复 start 以开始抽查",msg['FromUserName'])
        reciter[msg['FromUserName']]['isReciting']=1#表明准备完毕
        return False
    #print(reciter[msg['FromUserName']])
    if msg.text=='start' and reciter[msg['FromUserName']]['isReciting']==1:#开始抽查
        print("start")
        reciter[msg['FromUserName']]['isReciting']=2#表明正在抽查
        if len(reciter[msg['FromUserName']]['content'])>0:
            num=random.randint(0,len(reciter[msg['FromUserName']]['content'])-1)
            itchat.send_msg(reciter[msg['FromUserName']]['content'][num],msg['FromUserName'])
            reciter[msg['FromUserName']]['checking']=num#记录抽查的单词
        return False
    if reciter[msg['FromUserName']]['isReciting']==2:#表明正在抽查
        if (reciter[msg['FromUserName']]['checking'] %2)==0:#表明抽查的是英文
            itchat.send_msg(reciter[msg['FromUserName']]['content'][reciter[msg['FromUserName']]['checking']]+"的中文意思是:\n"+reciter[msg['FromUserName']]['content'][reciter[msg['FromUserName']]['checking']+1],msg['FromUserName'])
            if len(reciter[msg['FromUserName']]['content'])>0:#抽查下一个
                    num=random.randint(0,len(reciter[msg['FromUserName']]['content'])-1)
                    itchat.send_msg(reciter[msg['FromUserName']]['content'][num],msg['FromUserName'])
                    reciter[msg['FromUserName']]['checking']=num#记录抽查的单词
        else:#表明抽查的中文
            if msg.text==reciter[msg['FromUserName']]['content'][reciter[msg['FromUserName']]['checking']-1]:#如果对的话
                itchat.send_msg("√",msg['FromUserName'])
                if len(reciter[msg['FromUserName']]['content'])>0:#抽查下一个
                    num=random.randint(0,len(reciter[msg['FromUserName']]['content'])-1)
                    itchat.send_msg(reciter[msg['FromUserName']]['content'][num],msg['FromUserName'])
                    reciter[msg['FromUserName']]['checking']=num#记录抽查的单词
            else:
                itchat.send("X\n"+reciter[msg['FromUserName']]['content'][reciter[msg['FromUserName']]['checking']-1],msg['FromUserName'])
                if len(reciter[msg['FromUserName']]['content'])>0:#抽查下一个
                    num=random.randint(0,len(reciter[msg['FromUserName']]['content'])-1)
                    itchat.send_msg(reciter[msg['FromUserName']]['content'][num],msg['FromUserName'])
                    reciter[msg['FromUserName']]['checking']=num#记录抽查的单词
        return False

    if msg.text=='单词抽查器':#有人想背单词
        reciter[msg['FromUserName']]={}
        reciter[msg['FromUserName']]['isReciting']=0
        itchat.send_msg("请把要抽背的中文和英文之间用空格隔开,并发给我.\n示例:",msg['FromUserName'])
        itchat.send_msg("test 测试,测验\napple 苹果",msg['FromUserName'])
        itchat.send_msg("回复exit2以终止单词抽查器",msg['FromUserName'])
        return False
    return True

