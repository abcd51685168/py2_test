# coding=utf-8
import itchat, time

itchat.auto_login()


@itchat.msg_register(['Text', 'Map', 'Card', 'Note', 'Sharing'])
def text_reply(msg):
    itchat.send('%s: %s' % (msg['Type'], msg['Text']), msg['FromUserName'])


@itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
def download_files(msg):
    fileDir = '%s%s' % (msg['Type'], int(time.time()))
    msg['Text'](fileDir)
    itchat.send('%s received' % msg['Type'], msg['FromUserName'])
    itchat.send('@%s@%s' % ('img' if msg['Type'] == 'Picture' else 'fil', fileDir), msg['FromUserName'])


@itchat.msg_register('Friends')
def add_friend(msg):
    itchat.add_friend(**msg['Text'])
    itchat.get_contract()
    itchat.send_msg(msg['RecommendInfo']['UserName'], 'Nice to meet you!')


@itchat.msg_register('Text', isGroupChat=True)
def text_reply(msg):
    itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])


itchat.run()
