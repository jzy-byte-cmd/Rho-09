import itchat


####未完工
def who_delete_me():#判断谁删了我
    username=itchat.search_friends(name='wsh')
    result=itchat.send_msg("",username)
    print(result)
    return