from email import message
import itchat,random,time,threading,os,datetime,easyocr

#from text_respond_person import chatbot,robot_on

global signing #是否正在签到
global signed #已经签到的
global signed_lists  #已经签到的人的字符串形式
global online_chatroom #聊天机器人正在服务的群聊
global waiting #正在等待cd的自动回复内容
#global ocr_reader2

global def_person#定义的人
global reply_mode_group#自定义回复模式,定义中
global content_group_reply#自定义回复的内容,定义中的
global ocr_user#使用ocr的拥护
global ocr_stop_all#禁用OCR

global def_reply_group#读取的内容
global def_reply_group_num#读取的相关序号
global list_before,list_now#以前已有的方案和新增的方案
global is_finding#正在找回自己的方案
global is_managing#正在管理自己的方案
global exif_user#正在使用exif的人
global have_replied#15min内已经回复过的自动回复
global have_replied_wait#即将加入have_replied



waiting=[]
online_chatroom=[]
signed_lists=""
signing=False
signed=[]
ocr_user={}
#ocr_reader2=easyocr.Reader(['ch_tra','en'],gpu=True)
ocr_stop_all=False#关闭OCR指令

def_person={}#正在定义自定义回复的用户
reply_mode_group={}
content_group_reply={}
def_reply_group={}
def_reply_group_num={}
list_before=[]
list_now=[]
is_finding={}
is_managing={}
exif_open={}
have_replied=[]
have_replied_wait=[]

def signin_start(msg,owner_decided):#签到开始函数
    global signing
    global signed
    global signed_lists
    sender=""
    owner=""
    if 'ChatRoomOwner' in msg['User']:
        sender=msg['ActualUserName']
        owner=msg['User']['ChatRoomOwner']
        print("chatroom exist")
    else:
        print("no exist")
        sender=msg['ActualNickName']
        #print(msg['DisplayName'])
        owner=owner_decided
    if sender==owner and signing==False:#表明是群主发的信息
        print("群主消息确认")
        if msg.text=="发起签到":#群主发起签到
            print("确认发起签到")
            signed.append(msg['ActualNickName'])#默认群主已经签到
            signed_lists+=msg['ActualNickName']+"\n"
            signing=True
            #print(type(signed_lists))
            send_message='签到中....\n已签到列表:\n'+str(signed_lists)+"签到完成度:"+"1"+"/"+str(msg['User']['MemberCount'])
            itchat.send_msg(send_message,msg['User']['UserName'])
            itchat.send_msg('在群内以任意形式发言以签到.',msg['User']['UserName'])
            itchat.send_msg("群主回复 结束签到 即可结束签到",msg['User']['UserName'])
    else:
        if sender==owner and msg.text=="发起签到":#表明是群主但是已经有一次签到了
            print("已经存在签到...")
            itchat.send_msg('to 群主,当前已经有一次签到正在进行中...\n回复结束签到以停止',msg['User']['UserName'])
    return



def signin(msg):#签到函数
    global signed
    global signing
    global signed_lists
    if not(msg['ActualNickName'] in signed) and signing==True:#如果不在已签到名单中,并且当前正在签到
        print("签到人数+1")
        signed.append(msg['ActualNickName'])#加入已签到名单
        signed_lists+=msg['ActualNickName']+"\n"
        print("append succeeded")
        ###bug
        send_message='签到中....\n已签到列表:\n'+str(signed_lists)+"签到完成度:"+str(len(signed))+"/"+str(msg['User']['MemberCount'])
        print("message ok")
        result=itchat.send_msg(send_message,msg['User']['UserName'])
        print(result)
    return

def signin_end(msg,owner_decided):#结束签到
    global signed
    global signing
    global signed_lists
    sender=""
    owner=""
    print(msg['ActualNickName'])
    if 'ChatRoomOwner' in msg['User']:
        sender=msg['ActualUserName']
        owner=msg['User']['ChatRoomOwner']
        print("chatroom exist")
    else:
        print("no exist")
        sender=msg['ActualNickName']
        owner=owner_decided
    if len(signed)==msg['User']['MemberCount']:#全员完成签到
        print("签到结束")
        itchat.send_msg('全员已完成签到.',msg['User']['UserName'])
        signing=False                           #重置所有相关变量
        signed.clear()
        signed_lists=""
    if sender==owner and msg.text=="结束签到":
        print("结束签到")
        signing=False                           #重置所有相关变量
        itchat.send_msg('结束签到.',msg['User']['UserName'])
        signed.clear()
        signed_lists=""
    return




def standard_reply_group(msg):
    if msg.isAt==True:
        #写入txt文件
        print(msg.text)
        itchat.send_msg('[托管程序]本人现在不在,有急事可以私聊我.[已将消息内容记录]',msg['User']['UserName'])
    return



def wsh_resume(msg):#温子的简历
    if ('乙烯催熟水管' in str(msg.text)) and (msg['User']['NickName']=='三林伞兵号'):#如果有人说乙烯催熟水管
        itchat.send_msg('''温韶晗,又名温子,于2022年3月于三林中学证道成仙,世称乙烯大仙\n因其在16岁时就在化学课上发现了乙烯催熟水管的办法,
        于2035年02月31日获得诺贝尔化学奖.\n她为人谦和,虽然不知道是大智若愚还是真的愚,但是深受同学们喜爱.''',msg['User']['UserName'])
        return False
    return True



def auto_reply(msg):#自动回复群聊信息   #已弃用
    reply_choice=[
    ["笑死了","笑死我了","笑得我想死","笑死",
    "C:\\Users\\jinzh\\Desktop\\code\\python\\微信自动回复\\pic\\220520-115850.gif",
    "C:\\Users\\jinzh\\Desktop\\code\\python\\微信自动回复\\pic\\220520-115914.gif",
    "C:\\Users\\jinzh\\Desktop\\code\\python\\微信自动回复\\pic\\220520-115920.gif"],
    #笑死的选项
    ["确实难崩","属实难崩","蚌埠住了"],
    #难崩的选项
    ["确实","雀氏","不得不说,确实"]
    #确实的选项
    ]
    if '笑死' in str(msg.text) and not ('笑死' in waiting):#消息里含有笑死 并且笑死不在cd内
        content=random.randint(0,len(reply_choice[0])-1)#随机选一个回复
        if content<=3:
            itchat.send_msg(reply_choice[0][content],msg['User']['UserName'])
        else:
            itchat.send_image(reply_choice[0][content],msg['User']['UserName'])
        waiting.append('笑死')
        thread_laugh=threading.Thread(target=auto_reply_wait,args=(300,'笑死'))#5min后重置cd
        thread_laugh.setDaemon(True)
        thread_laugh.start()
        return
    if '难崩' in str(msg.text) and not('难崩' in waiting):#消息里含有难崩 并且难崩不在cd内
        content=random.randint(0,len(reply_choice[1])-1)
        itchat.send_msg(reply_choice[1][content],msg['User']['UserName'])
        waiting.append('笑死')
        thread_cantbear=threading.Thread(target=auto_reply_wait,args=(300,'难崩'))#5min后重置cd
        thread_cantbear.setDaemon(True)
        thread_cantbear.start()
        return
    if '确实'==str(msg.text) or '雀氏'==str(msg.text) and not('确实' in waiting):#消息里含有确实  并且确实不在cd内
        content=random.randint(0,len(reply_choice[2])-1)
        if content<=2:
            itchat.send_msg(reply_choice[2][content],msg['User']['UserName'])
        else:
            itchat.send_image(reply_choice[2][content],msg['User']['UserName'])
        waiting.append('确实')
        thread_indeed=threading.Thread(target=auto_reply_wait,args=(300,'确实'))#5min后重置cd
        thread_indeed.setDaemon(True)
        thread_indeed.start()
        return
    return


def auto_reply_wait(wait_time,content):#自动回复内容的cd   已弃用
    global waiting
    time.sleep(wait_time)
    waiting.remove(content)
    return




def chatter(msg):#聊天机器人
    global robot_on
    global chatbot
    global online_chatroom
    if msg.text=="Rho-09":#呼叫Rho-09
        itchat.send_msg("Rho-09已废弃,最后一个版本:V0.0.0.20220522_Beta",msg['User']['UserName'])
        return False
        ###
        itchat.send_msg("声明:Rho-09回答的结果基于机器学习\n从Rho-09 online 至 Rho-09 offline期间,\
产生的聊天内容均视为Rho-09的发言,不代表本人立场及观点.同时Rho-09会记录您的聊天至数据库\n若您同意并认可上述条款,可回复 Rho-09在吗 \
以开始和Rho-09聊天.",msg['User']['UserName'])
        return False
    if msg.text=='Rho-09在吗':
        itchat.send_msg("Rho-09已废弃,最后一个版本:V0.0.0.20220522_Beta",msg['User']['UserName'])
        return False
        ###
        itchat.send_msg("Rho-09\n版本:V0.0.0.20220522_Beta\n适配器:\nLevenshtein距离算法\n\
时间逻辑适配器\n数学评估适配器\nBestMatch适配器\n\
停用词:True\n语料库:基础.\n备注:这一版本的Rho-09刚刚诞生,还处于测试阶段,目前的回答能力非常有限.\n\n\
回复Rho-09再见 以关闭Rho-09",msg['User']['UserName'])
        itchat.send_msg("Rho-09 online",msg['User']['UserName'])
        itchat.send_msg("你好.",msg['User']['UserName'])
        robot_on=True
        online_chatroom.append(msg['User']['UserName'])
        return False
    '''
    if robot_on==True and msg['User']['UserName'] in online_chatroom:#Rho-09 online
        result=str(chatbot.get_response(str(msg.text)))
        print(result)
        itchat.send_msg(result,msg['User']['UserName'])
    '''
    if msg.text=='Rho-09再见':#rho-09 offline
        itchat.send_msg("Rho-09已废弃,最后一个版本:V0.0.0.20220522_Beta",msg['User']['UserName'])
        return False
        ###
        itchat.send_msg('Rho_09 offline',msg['User']['UserName'])
        robot_on=False
        online_chatroom.remove(msg['User']['UserName'])
        return False
    return True


def OCR_group_start(msg):#启动Ocr
    global ocr_user
    global ocr_stop_all
    #print(ocr_stop_all)
    if msg.text=='OCR':#启动OCR
        if ocr_stop_all==True:#暂停使用OCR
            itchat.send_msg("目前杳泽的电脑有较大运算负荷,出于安全性和性能考虑,OCR已被暂停使用,可稍后再试",msg['User']['UserName'])
        else:
            #print("ocr in")
            #print(msg['ActualNickName'])
            ocr_user[msg['ActualNickName']]=True
            itchat.send_msg("to "+msg['ActualNickName']+",请把要识别的图片发出来,回复stop以停止识别",msg['User']['UserName'])
            return False
    if msg.text=='stop':#停止识别
        itchat.send_msg("to "+msg['ActualNickName']+",已停止识别",msg['User']['UserName'])
        ocr_user[msg['ActualNickName']]=False
        return False
    return True

def OCR_group(msg):#ocr识别
    global ocr_user
    #global ocr_reader2
    message=''
    if msg['ActualNickName'] in ocr_user:
        if ocr_user[msg['ActualNickName']]==True:#表明此人正在开启识别
            ocr_reader1= easyocr.Reader(['ch_sim','en'],gpu=True) #用GPU更快
            print("start ocr")
            name=os.path.split(os.path.realpath(__file__))[0]+'\\downloaded_files\\'+msg.fileName
            msg.download(os.path.split(os.path.realpath(__file__))[0]+'\\downloaded_files\\'+msg.fileName)
            result1=ocr_reader1.readtext(name,detail = 0)
            for i in range(len(result1)):#
                message+=result1[i]+'\n'
            itchat.send_msg("识别结果:\n"+message,msg['User']['UserName'])
            os.remove(name)
            return False
    return True



def menu(msg):
    if msg.text=='选项':
        itchat.send('''
1.回复 OCR 以使用光学识别.
2.回复 自定义回复  以查看自定义回复相关内容
3.回复 EXIF 以提取图片信息[如果有的话]
''',msg['User']['UserName'])
        return False
    return True

def def_own_reply_start(msg):#开始/管理自定义回复
    global def_person
    global content_group_reply
    global list_before,list_now
    global def_reply_group
    global def_reply_group_num
    global is_finding,is_managing
    if not(msg['ActualUserName'] in is_finding):#防止访问不存在的键
        is_finding[msg['ActualUserName']]=-1
    if not(msg['ActualUserName'] in is_managing):#防止访问不存在的键
        is_managing[msg['ActualUserName']]=-1
    if msg.text=='新增自定义回复':#自己创建一个自定义回复
        itchat.send_msg("to "+msg['ActualNickName']+",啊哈,看来你想整点新鲜的",msg['User']['UserName'])
        itchat.send_msg("想要退出自定义回复 可回复exit",msg['User']['UserName'])
        def_person[msg['ActualUserName']]=0
        return False
    if msg.text=='找回我的回复':#找回先前的回复
        itchat.send_msg("to "+msg['ActualNickName']+",请告诉我你先前的昵称,回复 exit3 以停止找回",msg['User']['UserName'])
        is_finding[msg['ActualUserName']]=0
        return False
    if msg.text=='exit3':#停止找回先前的回复
        itchat.send_msg("to "+msg['ActualNickName']+",已停止找回先前的回复",msg['User']['UserName'])
        is_finding[msg['ActualUserName']]=-1
        return False
    if msg.text=='exit4':#停止方案管理
        itchat.send_msg("to "+msg['ActualNickName']+",已退出回复方案管理",msg['User']['UserName'])
        is_managing[msg['ActualUserName']]=-1
        return False
    if is_finding[msg['ActualUserName']]==0:#正在找回回复
        if msg.text in def_reply_group:#
            itchat.send_msg("to "+msg['ActualNickName']+",找到此昵称关联的"+str(len(def_reply_group[msg.text]))+"个回复方案,以将其转移到你现有昵称下",msg['User']['UserName'])
            target_files=os.listdir(os.path.split(os.path.realpath(__file__))[0]+'\\def_reply_group\\')
            message_tem=""
            for target in target_files:
                file=open(os.path.split(os.path.realpath(__file__))[0]+'\\def_reply_group\\'+target,encoding='utf_8',mode='r')
                original_content=[]
                while 1:
                    line=file.readline()
                    line=line.strip('\n')
                    original_content.append(line)
                    if not line:
                        file.close()
                        break
                if original_content[0]==msg.text:#表明是他的方案
                    file=open(os.path.split(os.path.realpath(__file__))[0]+'\\def_reply_group\\'+target,encoding='utf_8',mode='w')#覆盖写入
                    file.write(msg['ActualNickName']+'\n')  
                    file.write(original_content[1]+'\n')
                    file.write(original_content[2]+'\n')
                    file.write(original_content[3]+'\n')
                    file.write(original_content[4]+'\n')
                    file.write(original_content[5])
                    file.close()
                    message_tem+='\n'+target
            itchat.send_msg("to "+msg['ActualNickName']+",已找回的方案:"+message_tem,msg['User']['UserName'])
            message_tem=""
            is_finding[msg['ActualUserName']]=-1
            def_reply_group={}
            def_reply_group_num={}#清空已读取的方案
            load_reply_group()#重新加载
        else:
            itchat.send_msg("to "+msg['ActualNickName']+",没有找到和这个昵称有关的回复方案,请检查拼写是否有误,并重新发送",msg['User']['UserName'])
        return False

    if msg.text=='自定义回复':#询问自定义回复相关的内容
        itchat.send_msg("1.回复 新增自定义回复,\n以自己新创一个自定义回复\n\n2.回复 找回我的回复,\n以找回由于更改昵称而丢失的回复\n\n3.回复 管理我的回复,\n以管理自己的自定义回复\n\n4.回复 更新自定义回复,\n以更新审核通过的自定义回复",msg['User']['UserName'])
        return False
    if msg.text=='更新自定义回复':#更新自己改名前的自定义回复
        def_reply_group={}
        def_reply_group_num={}#清空已读取的方案
        list_now=load_reply_group()#更新现有的方案
        list_changed=list(set(list_now)-set(list_before))#获取新增的方案
        list_before=list_now #更新list before
        list_now=[]#清空listnow
        message_tem=""
        for i in list_changed:
            i=i.replace('.txt','')
            message_tem+='\n'+i
        itchat.send_msg("to "+msg['ActualNickName']+",新审核通过的方案:"+message_tem,msg['User']['UserName'])
        list_changed=[]#清空list_changed
        message_tem=""#清空messagetem
        rejected_files=os.listdir(os.path.split(os.path.realpath(__file__))[0]+'\\def_reply_group_rejected\\')#被驳回的方案
        for i in rejected_files:
            i=i.replace('.txt','')
            message_tem+='\n'+i
        itchat.send_msg("to "+msg['ActualNickName']+",被驳回的方案:"+message_tem,msg['User']['UserName'])
        rejected_files=[]
        message_tem=""
        waiting_files=os.listdir(os.path.split(os.path.realpath(__file__))[0]+'\\reply_check_group\\')#正在审核中的方案
        for i in waiting_files:
            i=i.replace('.txt','')
            message_tem+='\n'+i
        itchat.send_msg("to "+msg['ActualNickName']+",正在审核的方案:"+message_tem,msg['User']['UserName'])
        waiting_files=[]
        message_tem=""
        '''
        had_files=os.listdir(os.path.split(os.path.realpath(__file__))[0]+'\\def_reply_group\\')#已有的方案
        for i in had_files:
            message_tem+='\n'+i
        itchat.send_msg("to "+msg['ActualNickName']+",已经通过的方案:"+message_tem,msg['User']['UserName'])
        had_files=[]
        message_tem=""
        '''
        return False    
    if msg.text=='管理我的回复':
        itchat.send_msg("暂时还没好,差一点点,今天实在写不动了",msg['User']['UserName'])
        return False
        '''
        message_tem=""
        all_files=os.listdir(os.path.split(os.path.realpath(__file__))[0]+'\\def_reply_group\\')
        for i in all_files:
            i=i.replace('.txt','')
            message_tem+='\n'+i+"  status:"
            file=open(os.path.split(os.path.realpath(__file__))[0]+'\\def_reply_group\\'+i+'.txt',encoding='utf_8',mode='r')#读取
            while 1:
                line=file.readline()
                line=line.strip('\n')
                if line=='off' or line=='on':
                    message_tem+=line
                if not line:
                    file.close()
                    break
        itchat.send_msg("to "+msg['ActualNickName']+",您的所有回复方案:"+message_tem,msg['User']['UserName'])
        itchat.send_msg("to "+msg['ActualNickName']+",告诉我要切换开关状态的 回复方案名称,以切换方案的开关状态,回复exit4以退出方案管理",msg['User']['UserName'])
        is_managing[msg['ActualUserName']]=0
        return False
    if is_managing[msg['ActualUserName']]==0:#表明正在管理恢复方案
        all_files=os.listdir(os.path.split(os.path.realpath(__file__))[0]+'\\def_reply_group\\')
        for i in all_files:
            if i==msg.text:#表明确实有这个方案
                original_content=[]
                file=open(os.path.split(os.path.realpath(__file__))[0]+'\\def_reply_group\\'+i+'.txt',encoding='utf_8',mode='r')
                while 1:
                    line=file.readline()
                    line=line.strip('\n')
                    original_content.append(line)
                    if not line:
                        file.close()
                        break
                file=open(os.path.split(os.path.realpath(__file__))[0]+'\\def_reply_group\\'+i+'.txt',encoding='utf_8',mode='w')
                file.write(original_content[0]+'\n')
                file.write(original_content[1]+'\n')
                file.write(original_content[2]+'\n')
                file.write(original_content[3]+'\n')
                file.write(original_content[4]+'\n')
                if original_content[5]=='on':
                    file.write('off')
                else:
                    if original_content[5]=='off':
                        file.write('on')
                file.close()
                itchat.send_msg("to "+msg['ActualNickName']+",已完成更改,已退出 管理",msg['User']['UserName'])
                is_managing[msg['ActualUserName']]=-1
                def_reply_group={}
                def_reply_group_num={}
                load_reply_group()
                return False
                '''

    if msg.text=='exit':#退出自定义回复
        content_group_reply[msg['ActualUserName']].clear()
        def_person[msg['ActualUserName']]=-1
        itchat.send_msg("自定义自动回复已退出",msg['User']['UserName'])
    return True

def def_own_reply(msg):#自定义回复ing
    global def_person
    global reply_mode_group
    global content_group_reply
    if msg['ActualUserName'] in def_person:#如果这个人在储存相关名单字典里
        #print("in")
        if def_person[msg['ActualUserName']]==-1:#如果是没在自定义回复
            return True
        if def_person[msg['ActualUserName']]==0:#如果进行到第0步
            itchat.send_msg("to "+msg['ActualNickName']+",那么请问你想我按照哪种方式来回复你呢?\n1.识别关键词\n2.识别整个句子\n3.识别特殊格式的消息\
            \n(请你回复相应数字喔)",msg['User']['UserName'])
            def_person[msg['ActualUserName']]=1#进行第1步
            return False
        if def_person[msg['ActualUserName']]==1:#进行到第1步
            if msg.text !='1' and msg.text !='2' and msg.text !='3':#表明没按照上一步的要求
                itchat.send_msg("to "+msg['ActualNickName']+",啊哦,貌似你没按照要求来喔,我们得重新回到上一步",msg['User']['UserName'])
                itchat.send_msg("to "+msg['ActualNickName']+",请问你想我按照哪种方式来回复你呢?\n1.识别关键词\n2.识别整个句子\n3.识别特殊格式的消息\
            \n(请你回复相应数字喔)",msg['User']['UserName'])
                return False
            if msg.text =='1':#希望识别关键词
                itchat.send_msg("to "+msg['ActualNickName']+",你希望识别什么关键词呢?",msg['User']['UserName'])
                def_person[msg['ActualUserName']]=2#进行第2步
                reply_mode_group[msg['ActualUserName']]='word'#识别关键词模式
                return False
            if msg.text =='2':#希望识别整个句子
                itchat.send_msg("to "+msg['ActualNickName']+",你希望识别什么内容呢?(注意:识别的内容必须完全一致才能触发自动回复,标点符号区分全半角,也区分空格)",msg['User']['UserName'])
                def_person[msg['ActualUserName']]=2#进行第2步
                reply_mode_group[msg['ActualUserName']]='sentence'#识别整个句子模式
                return False
            if msg.text =='3':#希望识别特殊格式的消息
                itchat.send_msg("to "+msg['ActualNickName']+",你希望识别什么特殊格式的消息呢?把格式告诉我吧. #表示任意英文字符, %表示任意中文字, *表示任意字符, <表示任意数字, >表示任意标点符号",msg['User']['UserName'])
                itchat.send_msg("to "+msg['ActualNickName']+",例1:\n你##><吧\n[表示识别第一个字为\'你\',最后一个字为\'吧\',中间为任意2个英文字符,任意1个标点符号,任意1个数字](有顺序)]",msg['User']['UserName'])
                def_person[msg['ActualUserName']]=2#进行第2步
                reply_mode_group[msg['ActualUserName']]='special'#识别关键词模式
                return False
        if def_person[msg['ActualUserName']]==2:#进行到第2步
            if reply_mode_group[msg['ActualUserName']]=='word':#如果是识别关键词模式
                itchat.send_msg("to "+msg['ActualNickName']+",你希望我识别到 "+msg.text+" 这个关键词后怎么回复你呢?(直接回复需要回复的内容)",msg['User']['UserName'])
                content_group_reply[msg['ActualUserName']]=[]
                content_group_reply[msg['ActualUserName']].append(msg.text)
                def_person[msg['ActualUserName']]=3#进行第3步
                return False
            if reply_mode_group[msg['ActualUserName']]=='sentence':#如果是识别整个句子
                itchat.send_msg("to "+msg['ActualNickName']+",你希望我识别到 "+msg.text+" 这句话后怎么回复你呢?(直接回复需要回复的内容)",msg['User']['UserName'])
                content_group_reply[msg['ActualUserName']]=[]
                content_group_reply[msg['ActualUserName']].append(msg.text)
                def_person[msg['ActualUserName']]=3#进行第3步
                return False
            if reply_mode_group[msg['ActualUserName']]=='special':
                itchat.send_msg("to "+msg['ActualNickName']+",你希望我怎么回答 "+msg.text+" 这类话呢?",msg['User']['UserName'])
                content_group_reply[msg['ActualUserName']]=[]
                content_group_reply[msg['ActualUserName']].append(msg.text)
                def_person[msg['ActualUserName']]=3#进行第3步
                return False
        if def_person[msg['ActualUserName']]==3:#进行到第3步
            content_group_reply[msg['ActualUserName']].append(msg.text)#收集回复
            itchat.send_msg("to "+msg['ActualNickName']+",你希望这个自动回复只对你响应还是对所有群友都响应呢?(回复s/a)",msg['User']['UserName'])
            def_person[msg['ActualUserName']]=4
            return False
        if def_person[msg['ActualUserName']]==4:#进行到第4步
            if msg.text!='s' and msg.text!='a' and msg.text!='S' and msg.text!='A':#表明没按要求来
                itchat.send_msg("to "+msg['ActualNickName']+",貌似你没按照要求回复喔.",msg['User']['UserName'])
                itchat.send_msg("to "+msg['ActualNickName']+",你希望这个自动回复只对你响应还是对所有群友都响应呢?(回复s/a)",msg['User']['UserName'])
                return False
            if msg.text=='s' or msg.text=='S':#表明单独使用
                content_group_reply[msg['ActualUserName']].append('single')
            if msg.text=='a' or msg.text=='A':#表明全体都使用
                content_group_reply[msg['ActualUserName']].append(msg['User']['NickName'])#记录群聊id
            itchat.send_msg("啊哈,我们就快完成了",msg['User']['UserName'])
            #print(content_group_reply)
            if reply_mode_group[msg['ActualUserName']]=='word':#识别关键词
                itchat.send_msg("to "+msg['ActualNickName']+",预期效果:(*代表任意字符)\n"+msg['User']['NickName']+":**"+content_group_reply[msg['ActualUserName']][0]+"***\n杳泽:"+content_group_reply[msg['ActualUserName']][1]+"\n使用模式:"+content_group_reply[msg['ActualUserName']][2],msg['User']['UserName'])
                itchat.send_msg("to "+msg['ActualNickName']+",是否保存?(请回复y/n)",msg['User']['UserName'])
                def_person[msg['ActualUserName']]=5#去第5步
                return False
            if reply_mode_group[msg['ActualUserName']]=='sentence':#识别整个句子
                itchat.send_msg("to "+msg['ActualNickName']+",预期效果:\n"+msg['User']['NickName']+":"+content_group_reply[msg['ActualUserName']][0]+"\n杳泽:"+content_group_reply[msg['ActualUserName']][1]+"\n使用模式:"+content_group_reply[msg['ActualUserName']][2],msg['User']['UserName'])
                itchat.send_msg("to "+msg['ActualNickName']+",是否保存?(请回复y/n)",msg['User']['UserName'])
                def_person[msg['ActualUserName']]=5#去第5步
                return False
            if reply_mode_group[msg['ActualUserName']]=='special':#识别特殊句式
                itchat.send_msg("to "+msg['ActualNickName']+",预期效果:\n"+msg['User']['NickName']+":"+content_group_reply[msg['ActualUserName']][0]+"\n杳泽:"+content_group_reply[msg['ActualUserName']][1]+"\n使用模式:"+content_group_reply[msg['ActualUserName']][2],msg['User']['UserName'])
                itchat.send_msg("to "+msg['ActualNickName']+",是否保存?(请回复y/n)",msg['User']['UserName'])
                def_person[msg['ActualUserName']]=5#去第5步
                return False
        if def_person[msg['ActualUserName']]==5:#进行第5步
            if msg.text!='y' and msg.text!='n' and msg.text!='Y' and msg.text!='N':#表明没按照要求来
                itchat.send_msg("to "+msg['ActualNickName']+",啊哦,貌似你没按照要求来喔,我们得重新回到上一步",msg['User']['UserName'])
                if reply_mode_group[msg['ActualUserName']]=='word':#识别关键词
                    itchat.send_msg("to "+msg['ActualNickName']+",预期效果:\n"+msg['User']['NickName']+":**"+content_group_reply[msg['ActualUserName']][0]+"***\n杳泽:"+content_group_reply[msg['ActualUserName']][1],msg['User']['UserName'])
                    itchat.send_msg("to "+msg['ActualNickName']+",是否保存?(请回复y/n)",msg['User']['UserName'])
                    return False
                if reply_mode_group[msg['ActualUserName']]=='sentence':#识别整个句子
                    itchat.send_msg("to "+msg['ActualNickName']+",预期效果:\n"+msg['User']['NickName']+":"+content_group_reply[msg['ActualUserName']][0]+"\n杳泽:"+content_group_reply[msg['ActualUserName']][1],msg['User']['UserName'])
                    itchat.send_msg("to "+msg['ActualNickName']+",是否保存?(请回复y/n)",msg['User']['UserName'])
                    return False
                if reply_mode_group[msg['ActualUserName']]=='special':#识别特殊句式
                    itchat.send_msg("to "+msg['ActualNickName']+",预期效果:\n"+msg['User']['NickName']+":"+content_group_reply[msg['ActualUserName']][0]+"\n杳泽:"+content_group_reply[msg['ActualUserName']][1],msg['User']['UserName'])
                    itchat.send_msg("to "+msg['ActualNickName']+",是否保存?(请回复y/n)",msg['User']['UserName'])
                    return False
            if msg.text=='y' or msg.text=='Y':#确认保存
                itchat.send_msg("to "+msg['ActualNickName']+",好嘞!为了便于管理,请问这套回复要叫什么呢?\n(如果回复 默认,则将这套自定义回复以 模式+内容+时间来自动命名)",msg['User']['UserName'])
                def_person[msg['ActualUserName']]=6#去第5步
                return False
            if msg.text=='n' or msg.text=='N':#不保存
                itchat.send_msg("to "+msg['ActualNickName']+",好吧,我们重头来过,如果你不想自定义回复了 可以回复exit",msg['User']['UserName'])
                def_person[msg['ActualUserName']]=1
                itchat.send_msg("那么请问你想我按照哪种方式来回复你呢?\n1.识别关键词\n2.识别整个句子\n3.识别特殊格式的消息\
                \n(请你回复相应数字喔)",msg['User']['UserName'])
                content_group_reply[msg['ActualUserName']].clear()
                reply_mode_group[msg['ActualUserName']]=''
                return False
        if def_person[msg['ActualUserName']]==6:
            if msg.text!='默认':#如果不是默认
                itchat.send_msg("OK!这套方案已经被命名为"+msg.text+",并且默认开启了",msg['User']['UserName'])
                itchat.send_msg("但是要经过审核之后才能生效哈",msg['User']['UserName'])
                file=open(os.path.split(os.path.realpath(__file__))[0]+'\\reply_check_group\\'+msg.text+".txt",encoding='utf_8',mode='w')
                file.write(msg['ActualNickName']+'\n')
                file.write(reply_mode_group[msg['ActualUserName']]+'\n')
                file.write(content_group_reply[msg['ActualUserName']][0]+'\n')
                file.write(content_group_reply[msg['ActualUserName']][1]+'\n')
                file.write(content_group_reply[msg['ActualUserName']][2]+'\n')
                file.write('on')
                file.close()
                def_person[msg['ActualUserName']]=-1
                content_group_reply[msg['ActualUserName']].clear()
                reply_mode_group[msg['ActualUserName']]=''
                return False
            if msg.text=='默认':#默认名称
                itchat.send_msg("OK!这套方案现在被命名为了"+reply_mode_group[msg['ActualUserName']]+","+content_group_reply[msg['ActualUserName']][0]+","+str(datetime.datetime.now())\
                    ,msg['User']['UserName'])
                itchat.send_msg("但是要经过审核之后才能生效哈",msg['User']['UserName'])
                file=open(os.path.split(os.path.realpath(__file__))[0]+'\\reply_check_group\\'+reply_mode_group[msg['ActualUserName']]+","+content_group_reply[msg['ActualUserName']][0]+","+str(datetime.datetime.now())+".txt",encoding='utf_8',mode='w')
                file.write(msg['ActualNickName']+'\n')
                file.write(reply_mode_group[msg['ActualUserName']]+'\n')
                file.write(content_group_reply[msg['ActualUserName']][0]+'\n')
                file.write(content_group_reply[msg['ActualUserName']][1]+'\n')
                file.write(content_group_reply[msg['ActualUserName']][2]+'\n')
                file.write('on')
                file.close()
                def_person[msg['ActualUserName']]=-1
                content_group_reply[msg['ActualUserName']].clear()
                reply_mode_group[msg['ActualUserName']]=''
                return False
    return True

def load_reply_group():#加载自定义回复
    global def_reply_group
    global def_reply_group_num
    line_num=0
    nickname=''
    files=os.listdir(os.path.split(os.path.realpath(__file__))[0]+'\\def_reply_group\\')
    for target in files:
        file=open(os.path.split(os.path.realpath(__file__))[0]+'\\def_reply_group\\'+target,encoding='utf_8',mode='r')
        while 1:
            line = file.readline()
            line=line.strip('\n')
            if line_num==0:#第一行存的是nickname
                nickname=line
                if not (line in def_reply_group_num):#还没有存这个人的自定义回复数
                    def_reply_group[nickname]=[[]]
                    def_reply_group_num[nickname]=0#记录第一个回复
                else:
                    def_reply_group[nickname].append([])
                    def_reply_group_num[nickname]+=1#增加一个回复数
            else:#不是第一行
                line=line.replace('，',',')
                line=line.replace('。',',')
                line=line.replace('；',';')
                line=line.replace('：',':')
                line=line.replace('’','\'')
                line=line.replace('‘','\'')
                line=line.replace('“','"')
                line=line.replace('”','"')
                line=line.replace('【','[')
                line=line.replace('】',']')
                line=line.replace('、','\\')
                line=line.replace('《','<')
                line=line.replace('》','>')
                line=line.replace('？','?')
                line=line.replace('（','(')
                line=line.replace('）',')')
                line=line.replace('！','!')
                line=line.replace('·','`')
                def_reply_group[nickname][def_reply_group_num[nickname]].append(line)
            line_num+=1
            if not line:
                if len(def_reply_group[nickname][def_reply_group_num[nickname]])>0:
                    def_reply_group[nickname][def_reply_group_num[nickname]].pop()
                nickname=''
                line_num=0
                break
        file.close()
    print("group:\n",def_reply_group)
    return files

def use_def_reply(msg):
    global def_reply_group
    global have_replied
    global have_replied_wait
    possible_answer=[]
    msg.text=msg.text.replace('，',',')
    msg.text=msg.text.replace('。',',')
    msg.text=msg.text.replace('；',';')
    msg.text=msg.text.replace('：',':')
    msg.text=msg.text.replace('’','\'')
    msg.text=msg.text.replace('‘','\'')
    msg.text=msg.text.replace('“','"')
    msg.text=msg.text.replace('”','"')
    msg.text=msg.text.replace('【','[')
    msg.text=msg.text.replace('】',']')
    msg.text=msg.text.replace('、','\\')
    msg.text=msg.text.replace('《','<')
    msg.text=msg.text.replace('》','>')
    msg.text=msg.text.replace('？','?')
    msg.text=msg.text.replace('（','(')
    msg.text=msg.text.replace('）',')')
    msg.text=msg.text.replace('！','!')
    msg.text=msg.text.replace('·','`')
    ###将所有全角标点替换为半角标点,以方便识别符号
    if msg['ActualNickName'] in def_reply_group:#这个人有自定义回复
        #print("has")
        for num1 in range(len(def_reply_group[msg['ActualNickName']])):
            if def_reply_group[msg['ActualNickName']][num1][4]=='on':#如果是开启状态
                #print("on √")
                if def_reply_group[msg['ActualNickName']][num1][0]=='word':#关键词识别
                    #print("confirm word")
                    #print(def_reply[msg['User']['NickName']][num1][1])
                    if def_reply_group[msg['ActualNickName']][num1][1] in msg.text:#识别到关键词
                        #print("identified")
                        print(have_replied)
                        print(def_reply_group[msg['ActualNickName']][num1][1])
                        if not(def_reply_group[msg['ActualNickName']][num1][1] in have_replied):#如果15min内还没有回复过
                            possible_answer.append(def_reply_group[msg['ActualNickName']][num1][2])
                            if not(def_reply_group[msg['ActualNickName']][num1][1] in have_replied_wait):
                                have_replied_wait.append(def_reply_group[msg['ActualNickName']][num1][1])
                    continue
                if def_reply_group[msg['ActualNickName']][num1][0]=='sentence':#整句识别
                    #print("confirm sentence")
                    #print(len(def_reply[msg['User']['NickName']][num1]))
                    #print(def_reply[msg['User']['NickName']][num1][1])
                    if def_reply_group[msg['ActualNickName']][num1][1]==msg.text:#
                        print(have_replied)
                        print(def_reply_group[msg['ActualNickName']][num1][1])
                        if not(def_reply_group[msg['ActualNickName']][num1][1] in have_replied):#如果15min内还没有回复过
                            possible_answer.append(def_reply_group[msg['ActualNickName']][num1][2])
                            if not(def_reply_group[msg['ActualNickName']][num1][1] in have_replied_wait):
                                have_replied_wait.append(def_reply_group[msg['ActualNickName']][num1][1])
                    continue
                if def_reply_group[msg['ActualNickName']][num1][0]=='special':#特殊句式识别
                    #print("confirm special")
                    possible=True
                    if len(msg.text)==len(def_reply_group[msg['ActualNickName']][num1][1]):#表明可能能通过特殊句式识别
                        for num3 in range(len(def_reply_group[msg['ActualNickName']][num1][1])):#遍历整个特殊句式要求
                            # #表示任意英文字符,%表示任意中文字,*表示任意字符\
                            #,<表示任意数字,>表示任意标点符号
                            if def_reply_group[msg['ActualNickName']][num1][1][num3]=='*':#表明这个位置是任意字符
                                continue
                            if def_reply_group[msg['ActualNickName']][num1][1][num3]=='%':#表明必须是中文字
                                if '\u4e00' <= msg.text[num3] and msg.text[num3]<= '\u9fff':#表明是中文字
                                    continue
                                else:
                                    possible=False
                                    break#特殊句式识别失败
                            if def_reply_group[msg['ActualNickName']][num1][1][num3]=='#':#表明必须是任意英文字符
                                if (ord(msg.text[num3])>=65 and ord(msg.text[num3])<=90) or (ord(msg.text[num3])>=97 and ord(msg.text[num3])<=122):#表明是任意英文字符
                                    continue
                                else:
                                    possible=False
                                    break#特殊句式识别失败
                            if def_reply_group[msg['ActualNickName']][num1][1][num3]=='<':#表明必须是任意数字
                                if ord(msg.text[num3])<=57 and ord(msg.text[num3])>=48:#表明确实是任意数字
                                    continue
                                else:
                                    possible=False
                                    break
                            if def_reply_group[msg['ActualNickName']][num1][1][num3]=='>':#表明必须是任意标点符号
                                if (ord(msg.text[num3])>=33 and ord(msg.text[num3])<=47) or \
                                    (ord(msg.text[num3])>=58 and ord(msg.text[num3])<=64) or \
                                    (ord(msg.text[num3])>=91 and ord(msg.text[num3])<=96) or \
                                    (ord(msg.text[num3])>=123 and ord(msg.text[num3])<=127):#表明确实是任意标点符号
                                    continue
                                else:
                                    possible=False
                                    break
                            if def_reply_group[msg['ActualNickName']][num1][1][num3]!='>' and \
                                def_reply_group[msg['ActualNickName']][num1][1][num3]!='#' and \
                                def_reply_group[msg['ActualNickName']][num1][1][num3]!='*' and \
                                def_reply_group[msg['ActualNickName']][num1][1][num3]!='<' and \
                                def_reply_group[msg['ActualNickName']][num1][1][num3]!='%':#表明这就直接是一个字符或字
                                if msg.text[num3]==def_reply_group[msg['ActualNickName']][num1][1][num3]:#能匹配上
                                    continue
                                else:
                                    possible=False
                                    break
                    else:
                        possible=False
                    if possible==True:
                        print(have_replied)
                        print(def_reply_group[msg['ActualNickName']][num1][1])
                        if not(def_reply_group[msg['ActualNickName']][num1][1] in have_replied):#如果15min内还没有回复过
                            possible_answer.append(def_reply_group[msg['ActualNickName']][num1][2])
                            if not(def_reply_group[msg['ActualNickName']][num1][1] in have_replied_wait):
                                have_replied_wait.append(def_reply_group[msg['ActualNickName']][num1][1])

        ##尝试使用别人的自动回复
        all_keys=def_reply_group.keys()#取出所有人的键
        for user in all_keys:#遍历所有人的自定义回复
            #print(user)
            for num1 in range(len(def_reply_group[user])):
                #print(def_reply_group[user][num1][4])
                #print(def_reply_group[user][num1][3])
                if def_reply_group[user][num1][4]=='on' and def_reply_group[user][num1][3]==msg['User']['NickName']:#如果是开启状态,并且设置的所有人可以用
                    #print("on √")
                    if def_reply_group[user][num1][0]=='word':#关键词识别
                        #print("confirm word")
                        #print(def_reply[msg['User']['NickName']][num1][1])
                        if def_reply_group[user][num1][1] in msg.text:#识别到关键词
                            #print("identified")
                            print(have_replied)
                            print(def_reply_group[user][num1][1])
                            if not(def_reply_group[user][num1][1] in have_replied):#如果15min内还没有回复过
                                possible_answer.append(def_reply_group[user][num1][2])
                                if not(def_reply_group[user][num1][1] in have_replied_wait):
                                    have_replied_wait.append(def_reply_group[user][num1][1])
                        continue
                    if def_reply_group[user][num1][0]=='sentence':#整句识别
                        #print(def_reply_group[user][num1][2])
                        #print("confirm sentence")
                        #print(len(def_reply[msg['User']['NickName']][num1]))
                        #print(def_reply[msg['User']['NickName']][num1][1])
                        #print(def_reply_group[user][num1][1])
                        #print(msg.text)
                        #print(def_reply_group[user][num1][1]==msg.text)
                        if def_reply_group[user][num1][1]==msg.text:#
                            print(have_replied)
                            print(def_reply_group[user][num1][1])
                            if not(def_reply_group[user][num1][1] in have_replied):#如果15min内还没有回复过
                                possible_answer.append(def_reply_group[user][num1][2])
                                if not(def_reply_group[user][num1][1] in have_replied_wait):
                                    have_replied_wait.append(def_reply_group[user][num1][1])
                        continue
                    if def_reply_group[user][num1][0]=='special':#特殊句式识别
                        #print("confirm special")
                        possible=True
                        if len(msg.text)==len(def_reply_group[user][num1][1]):#表明可能能通过特殊句式识别
                            for num3 in range(len(def_reply_group[user][num1][1])):#遍历整个特殊句式要求
                                # #表示任意英文字符,%表示任意中文字,*表示任意字符\
                                #,<表示任意数字,>表示任意标点符号
                                if def_reply_group[user][num1][1][num3]=='*':#表明这个位置是任意字符
                                    continue
                                if def_reply_group[user][num1][1][num3]=='%':#表明必须是中文字
                                    if '\u4e00' <= msg.text[num3] and msg.text[num3]<= '\u9fff':#表明是中文字
                                        continue
                                    else:
                                        possible=False
                                        break#特殊句式识别失败
                                if def_reply_group[user][num1][1][num3]=='#':#表明必须是任意英文字符
                                    if (ord(msg.text[num3])>=65 and ord(msg.text[num3])<=90) or (ord(msg.text[num3])>=97 and ord(msg.text[num3])<=122):#表明是任意英文字符
                                        continue
                                    else:
                                        possible=False
                                        break#特殊句式识别失败
                                if def_reply_group[user][num1][1][num3]=='<':#表明必须是任意数字
                                    if ord(msg.text[num3])<=57 and ord(msg.text[num3])>=48:#表明确实是任意数字
                                        continue
                                    else:
                                        possible=False
                                        break
                                if def_reply_group[user][num1][1][num3]=='>':#表明必须是任意标点符号
                                    if (ord(msg.text[num3])>=33 and ord(msg.text[num3])<=47) or \
                                        (ord(msg.text[num3])>=58 and ord(msg.text[num3])<=64) or \
                                        (ord(msg.text[num3])>=91 and ord(msg.text[num3])<=96) or \
                                        (ord(msg.text[num3])>=123 and ord(msg.text[num3])<=127):#表明确实是任意标点符号
                                        continue
                                    else:
                                        possible=False
                                        break
                                if def_reply_group[user][num1][1][num3]!='>' and \
                                    def_reply_group[user][num1][1][num3]!='#' and \
                                    def_reply_group[user][num1][1][num3]!='*' and \
                                    def_reply_group[user][num1][1][num3]!='<' and \
                                    def_reply_group[user][num1][1][num3]!='%':#表明这就直接是一个字符或字
                                    if msg.text[num3]==def_reply_group[user][num1][1][num3]:#能匹配上
                                        continue
                                    else:
                                        possible=False
                                        break
                        else:
                            possible=False
                        if possible==True:
                            print(have_replied)
                            print(def_reply_group[user][num1][1])
                            if not(def_reply_group[user][num1][1] in have_replied):#如果15min内还没有回复过
                                possible_answer.append(def_reply_group[user][num1][2])
                                if not(def_reply_group[user][num1][1] in have_replied_wait):
                                    have_replied_wait.append(def_reply_group[user][num1][1])

        if len(possible_answer)>0:
            reply_target_num=random.randint(0,len(possible_answer)-1)#随机选一个回复
            itchat.send_msg(possible_answer[reply_target_num],msg['User']['UserName'])
            for i in have_replied_wait:#将have_replied_wait中的加入have_replied
                if not(i in have_replied):#如果have_replied里没有
                    have_replied.append(i)
                    thread_reply=threading.Thread(target=def_reply_cd,args=(i,))
                    thread_reply.setDaemon(True)
                    thread_reply.start()
            have_replied_wait=[]
            possible_answer=[]
            return False
        else:
            return True
    else:#如果这个人没有自定义回复,可以采用他人设置的自定义回复
        all_keys=def_reply_group.keys()#取出所有人的键
        for user in all_keys:#遍历所有人的自定义回复
            #print(user)
            for num1 in range(len(def_reply_group[user])):
                #print(def_reply_group[user][num1][4])
                #print(def_reply_group[user][num1][3])
                if def_reply_group[user][num1][4]=='on' and def_reply_group[user][num1][3]==msg['User']['NickName']:#如果是开启状态,并且设置的所有人可以用
                    #print("on √")
                    if def_reply_group[user][num1][0]=='word':#关键词识别
                        #print("confirm word")
                        #print(def_reply[msg['User']['NickName']][num1][1])
                        if def_reply_group[user][num1][1] in msg.text:#识别到关键词
                            #print("identified")
                            print(have_replied)
                            print(def_reply_group[user][num1][1])
                            if not(def_reply_group[user][num1][1] in have_replied):#如果15min内还没有回复过
                                possible_answer.append(def_reply_group[user][num1][2])
                                if not(def_reply_group[user][num1][1] in have_replied_wait):
                                    have_replied_wait.append(def_reply_group[user][num1][1])
                        continue
                    if def_reply_group[user][num1][0]=='sentence':#整句识别
                        #print("confirm sentence")
                        #print(len(def_reply[msg['User']['NickName']][num1]))
                        #print(def_reply[msg['User']['NickName']][num1][1])
                        if def_reply_group[user][num1][1]==msg.text:#
                            print(have_replied)
                            print(def_reply_group[user][num1][1])
                            if not(def_reply_group[user][num1][1] in have_replied):#如果15min内还没有回复过
                                possible_answer.append(def_reply_group[user][num1][2])
                                if not(def_reply_group[user][num1][1] in have_replied_wait):
                                    have_replied_wait.append(def_reply_group[user][num1][1])
                        continue
                    if def_reply_group[user][num1][0]=='special':#特殊句式识别
                        #print("confirm special")
                        possible=True
                        if len(msg.text)==len(def_reply_group[user][num1][1]):#表明可能能通过特殊句式识别
                            for num3 in range(len(def_reply_group[user][num1][1])):#遍历整个特殊句式要求
                                # #表示任意英文字符,%表示任意中文字,*表示任意字符\
                                #,<表示任意数字,>表示任意标点符号
                                if def_reply_group[user][num1][1][num3]=='*':#表明这个位置是任意字符
                                    continue
                                if def_reply_group[user][num1][1][num3]=='%':#表明必须是中文字
                                    if '\u4e00' <= msg.text[num3] and msg.text[num3]<= '\u9fff':#表明是中文字
                                        continue
                                    else:
                                        possible=False
                                        break#特殊句式识别失败
                                if def_reply_group[user][num1][1][num3]=='#':#表明必须是任意英文字符
                                    if (ord(msg.text[num3])>=65 and ord(msg.text[num3])<=90) or (ord(msg.text[num3])>=97 and ord(msg.text[num3])<=122):#表明是任意英文字符
                                        continue
                                    else:
                                        possible=False
                                        break#特殊句式识别失败
                                if def_reply_group[user][num1][1][num3]=='<':#表明必须是任意数字
                                    if ord(msg.text[num3])<=57 and ord(msg.text[num3])>=48:#表明确实是任意数字
                                        continue
                                    else:
                                        possible=False
                                        break
                                if def_reply_group[user][num1][1][num3]=='>':#表明必须是任意标点符号
                                    if (ord(msg.text[num3])>=33 and ord(msg.text[num3])<=47) or \
                                        (ord(msg.text[num3])>=58 and ord(msg.text[num3])<=64) or \
                                        (ord(msg.text[num3])>=91 and ord(msg.text[num3])<=96) or \
                                        (ord(msg.text[num3])>=123 and ord(msg.text[num3])<=127):#表明确实是任意标点符号
                                        continue
                                    else:
                                        possible=False
                                        break
                                if def_reply_group[user][num1][1][num3]!='>' and \
                                    def_reply_group[user][num1][1][num3]!='#' and \
                                    def_reply_group[user][num1][1][num3]!='*' and \
                                    def_reply_group[user][num1][1][num3]!='<' and \
                                    def_reply_group[user][num1][1][num3]!='%':#表明这就直接是一个字符或字
                                    if msg.text[num3]==def_reply_group[user][num1][1][num3]:#能匹配上
                                        continue
                                    else:
                                        possible=False
                                        break
                        else:
                            possible=False
                        if possible==True:
                            print(have_replied)
                            print(def_reply_group[user][num1][1])
                            if not(def_reply_group[user][num1][1] in have_replied):#如果15min内还没有回复过
                                possible_answer.append(def_reply_group[user][num1][2])
                                if not(def_reply_group[user][num1][1] in have_replied_wait):
                                    have_replied_wait.append(def_reply_group[user][num1][1])
        if len(possible_answer)>0:
            reply_target_num=random.randint(0,len(possible_answer)-1)#随机选一个回复
            itchat.send_msg(possible_answer[reply_target_num],msg['User']['UserName'])
            for i in have_replied_wait:#将have_replied_wait中的加入have_replied
                if not(i in have_replied):#如果have_replied里没有
                    have_replied.append(i)
                    thread_reply=threading.Thread(target=def_reply_cd,args=(i,))
                    thread_reply.setDaemon(True)
                    thread_reply.start()
            have_replied_wait=[]
            possible_answer=[]
            return False
        else:
            return True

def def_reply_cd(target):#自动回复的cd
    global have_replied
    time.sleep(900)#等15min
    have_replied.remove(target)#移除已回复,cd清空
    return

def exif_start(msg):#开启EXIF
    global exif_open
    if not(msg['ActualUserName'] in exif_open):
        exif_open[msg['ActualUserName']]=False
    if msg.text=='EXIF':#
        exif_open[msg['ActualUserName']]=True
        itchat.send_msg("to "+msg['ActualNickName']+",请把要读取exif信息的图片发出来,回复exit5以退出exif识别",msg['User']['UserName'])
        return False
    if msg.text=='exit5':#退出exif识别
        exif_open[msg['ActualUserName']]=False
        itchat.send_msg("to "+msg['ActualNickName']+"已停止exif识别",msg['User']['UserName'])
        return False
    return True

def exif(msg):#提取图片EXIF信息
    global exif_open
    if msg['ActualUserName'] in exif_open:
        if exif_open[msg['ActualUserName']]==True:#exif开启中
            name=os.path.split(os.path.realpath(__file__))[0]+'\\'+msg.fileName      #msg.fileName
            msg.download(os.path.split(os.path.realpath(__file__))[0]+'\\'+msg.fileName)    #msg.fileName)
            os.system("rename "+name+" target.png")
            itchat.send_msg("读取结果:\n"+os.popen('e: && exif.exe').read(),msg['User']['UserName'])
            os.remove(os.path.split(os.path.realpath(__file__))[0]+'\\'+'target.png')
            return False
    return True 


