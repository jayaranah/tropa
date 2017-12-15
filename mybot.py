# -*- coding: utf-8 -*-

import LINETCR
from LINETCR.lib.curve.ttypes import *
from datetime import datetime
import time,random,sys,json,codecs,threading,glob,re,ast,os,subprocess,requests
from googletrans import Translator


cl = LINETCR.LINE()
# cl.login(qr=True)
cl.login(token='EnT1zehU6MkRLcAUC45f.JaIcRyc14sLXZI5dJNLfhW.Xv+dz7kJSnBg4sujr0TeGc397pDmnCpBCjXwQRO5ZhI=')
cl.loginResult()
print "===[Login Success]==="


helpMessage ="""
╔═════════════
║LIST KEYWORD
║╔════════════
║╠Help
║╠Creator
║╠Gcreator
║╠List group:
║╠Leave group:
║╠Cancel
║╠Url:on|off
║╠Autojoin:on|off
║╠Autocancel:on|off
║╠Qr:on|off
║╠Autokick:on|off
║╠Contact:on|off
║╠Gift (1,2,3)
║╠tagbyone
║╠tagbyall
║╠Setview
║╠Viewseen
║╠Boom
║╠Add all
║╠Recover
║╠Remove all chat
║╠Gn: (name)
║╠Kick: (mid)
║╠Invite: (mid)
║╠Welcome
║╠Bc: (text)
║╠Cancelall
║╠Gurl
║╠Self Like
║╠Speed
║╠Ban|Unban
║╠Copy @
║╠Backup me
║╠Ban @|Unban @
║╠Banlist
║╠Kill ban
║╠Reboot
║╠Tr-id
║╠Tr-en
║╠Tr-ar
║╠Tr-jp
║╠Tr-ko
║╚════════════
╚═════════════
"""

mid = cl.getProfile().mid
Creator="u8c0882ad80b5e12971ce2e438e79451f"
admin=["u8c0882ad80b5e12971ce2e438e79451f"]

contact = cl.getProfile()
profile = cl.getProfile()
profile.displayName = contact.displayName
profile.statusMessage = contact.statusMessage
profile.pictureStatus = contact.pictureStatus

wait = {
    "LeaveRoom":True,
    "AutoJoin":True,
    "Members":0,
    "AutoCancel":False,
    "AutoKick":False,       
    "blacklist":{},
    "wblacklist":False,
    "dblacklist":False,
    "Qr":False,
    "Timeline":True,
    "Contact":True,
    "lang":"JP",
    "BlGroup":{}
}


def sendMessage(to, text, contentMetadata={}, contentType=0):
    mes = Message()
    mes.to, mes.from_ = to, profile.mid
    mes.text = text
    mes.contentType, mes.contentMetadata = contentType, contentMetadata
    if to not in messageReq:
        messageReq[to] = -1
    messageReq[to] += 1

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def bot(op):
    try:
#--------------------END_OF_OPERATION--------------------
        if op.type == 0:
            return
        if op.type == 15:
            cl.sendText(op.param1,cl.getContact(op.param2).displayName + ", Happy Way \nAnd Do Not Forget To Be Happy")
            print "NOTIFIED_LEAVE_GROUP"
        if op.type == 17:
			ginfo = cl.getGroup(op.param1)
			cl.sendText(op.param1,"Hi " + cl.getContact(op.param2).displayName + "\nWelcome To: " + str(ginfo.name) + "\nDo Naughty & Do Not Shy😊.\n🙅Avoid Flooding & Minimize The Stickers🙅\nIsang Paalala Mula Sa Mental Hospital😂")
			print "NOTIFIED_ACCEPT_GROUP_INVITATION"

        if op.type == 19:
            cl.sendText(op.param1,cl.getContact(op.param2).displayName + ", Kick yah!!!Byebye😅")
            print "NOTIFIED_KICKOUT_FROM_GROUP"
        if op.type == 32:
            # cl.sendText(op.param1,cl.getContact(op.param2).displayName + ", Invited")
            print "Cancel intive"
        if op.type == 5:
            if wait["autoAdd"] == True:
                cl.findAndAddContactsByMid(op.param1)
                if (wait["message"] in [""," ","\n",None]):
                    pass
                else:
                    cl.sendText(op.param1,str(wait["message"]))
#-------------------NOTIFIED_READ_MESSAGE----------------
        if op.type == 55:
	    try:
	      group_id = op.param1
	      user_id=op.param2
	      # ginfo = cl.getGroup(op.param1)
	      subprocess.Popen('echo "'+ user_id+'|'+str(op.createdTime)+'" >> dataSeen/%s.txt' % group_id, shell=True, stdout=subprocess.PIPE, )
	      # print "[Group]:" + str(ginfo.name) + "  |  [Name]: " + cl.getContact(op.param2).displayName
	    except Exception as e:
	      print e
		  
        if op.type == 55:
	    try:
	      ginfo = cl.getGroup(op.param1)
	      print "[Group]:" + str(ginfo.name) + "  |  [Name]: " + cl.getContact(op.param2).displayName
	    except Exception as e:
	      print e
#------------------NOTIFIED_INVITE_INTO_ROOM-------------
        if op.type == 22:
            cl.leaveRoom(op.param1)
#--------------------INVITE_INTO_ROOM--------------------
        if op.type == 21:
            cl.leaveRoom(op.param1)

#--------------NOTIFIED_INVITE_INTO_GROUP----------------

	    if mid in op.param3:
                if wait["AutoJoin"] == True:
                    cl.acceptGroupInvitation(op.param1)
                else:
		    cl.rejectGroupInvitation(op.param1)
	    else:
                if wait["AutoCancel"] == True:
		    if op.param3 in admin:
			pass
		    else:
                        cl.cancelGroupInvitation(op.param1, [op.param3])
		else:
		    if op.param3 in wait["blacklist"]:
			cl.cancelGroupInvitation(op.param1, [op.param3])
			cl.sendText(op.param1, "That's a kicker dont in invite!")
		    else:
			pass
#------------------NOTIFIED_KICKOUT_FROM_GROUP-----------------
        if op.type == 19:
		if wait["AutoKick"] == True:
                    if op.param2 in admin:
                        pass
                    try:
                        cl.kickoutFromGroup(op.param1,[op.param2])
			cl.inviteIntoGroup(op.param1,[op.param3])
                    except:
                        try:
			    cl.kickoutFromGroup(op.param1,[op.param2])
			    cl.inviteIntoGroup(op.param1,[op.param3])
                        except:
                            print ("client Kick regulation or Because it does not exist in the group\ngid=["+op.param1+"]\nmid=["+op.param2+"]")
                        if op.param2 in wait["blacklist"]:
                            pass
                        else:
			    if op.param2 in admin:
			        pass
			    else:
                                wait["blacklist"][op.param2] = True
                    if op.param2 in wait["blacklist"]:
                        pass
                    else:
		        if op.param2 in admin:
			    pass
		        else:
                            wait["blacklist"][op.param2] = True



#--------------------------NOTIFIED_UPDATE_GROUP---------------------
        if op.type == 11:
            if wait["Qr"] == True:
		if op.param2 in admin:
		    pass
		else:
                    cl.sendText(msg.to, "Do not play QR")
            else:
                pass
#--------------------------SEND_MESSAGE---------------------------
        if op.type == 25:
            msg = op.message
#----------------------------------------------------------------------------
            if msg.contentType == 13:
                if wait["wblacklist"] == True:
		    if msg.contentMetadata["mid"] not in admin:
                        if msg.contentMetadata["mid"] in wait["blacklist"]:
                            cl.sendText(msg.to,"already")
                            wait["wblacklist"] = False
                        else:
                            wait["blacklist"][msg.contentMetadata["mid"]] = True
                            wait["wblacklist"] = False
                            cl.sendText(msg.to,"aded")
		    else:
			cl.sendText(msg.to,"Admin Detected~")
			

                elif wait["dblacklist"] == True:
                    if msg.contentMetadata["mid"] in wait["blacklist"]:
                        del wait["blacklist"][msg.contentMetadata["mid"]]
                        cl.sendText(msg.to,"deleted")
                        wait["dblacklist"] = False

                    else:
                        wait["dblacklist"] = False
                        cl.sendText(msg.to,"It is not in the black list")
#--------------------------------------------------------
                elif wait["Contact"] == True:
                     msg.contentType = 0
                     cl.sendText(msg.to,msg.contentMetadata["mid"])
                     if 'displayName' in msg.contentMetadata:
                         contact = cl.getContact(msg.contentMetadata["mid"])
                         try:
                             cu = cl.channel.getCover(msg.contentMetadata["mid"])
                         except:
                             cu = ""
                         cl.sendText(msg.to,"[displayName]:\n" + msg.contentMetadata["displayName"] + "\n[mid]:\n" + msg.contentMetadata["mid"] + "\n[statusMessage]:\n" + contact.statusMessage + "\n[pictureStatus]:\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n[coverURL]:\n" + str(cu))
                     else:
                         contact = cl.getContact(msg.contentMetadata["mid"])
                         try:
                             cu = cl.channel.getCover(msg.contentMetadata["mid"])
                         except:
                             cu = ""
                         cl.sendText(msg.to,"[displayName]:\n" + contact.displayName + "\n[mid]:\n" + msg.contentMetadata["mid"] + "\n[statusMessage]:\n" + contact.statusMessage + "\n[pictureStatus]:\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n[coverURL]:\n" + str(cu))


#--------------------------------------------------------
            elif msg.text == "Ginfo":
                if msg.toType == 2:
                    ginfo = cl.getGroup(msg.to)
                    try:
                        gCreator = ginfo.creator.displayName
                    except:
                        gCreator = "Error"
                    if wait["lang"] == "JP":
                        if ginfo.invitee is None:
                            sinvitee = "0"
                        else:
                            sinvitee = str(len(ginfo.invitee))
                        if ginfo.preventJoinByTicket == True:
                            u = "close"
                        else:
                            u = "open"
                        cl.sendText(msg.to,"[Group name]\n" + str(ginfo.name) + "\n\n[Gid]\n" + msg.to + "\n\n[Group creator]\n" + gCreator + "\n\n[Profile status]\nhttp://dl.profile.line.naver.jp/" + ginfo.pictureStatus + "\n\nMembers:" + str(len(ginfo.members)) + "members\nPending:" + sinvitee + "people\nURL:" + u + "it is inside")
                    else:
                        cl.sendText(msg.to,"[group name]\n" + str(ginfo.name) + "\n[gid]\n" + msg.to + "\n[group creator]\n" + gCreator + "\n[profile status]\nhttp://dl.profile.line.naver.jp/" + ginfo.pictureStatus)
                else:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"Can not be used outside the group")
                    else:
                        cl.sendText(msg.to,"Not for use less than group")

#--------------------------------------------------------
            elif msg.text is None:
                return
#--------------------------------------------------------
            elif msg.text in ["Creator"]:
                msg.contentType = 13
                msg.contentMetadata = {'mid': Creator}
                cl.sendMessage(msg)
		cl.sendText(msg.to,"That's makes me")
#--------------------------------------------------------
	    elif msg.text in ["Group creator","Gcreator","gcreator"]:
		ginfo = cl.getGroup(msg.to)
		gCreator = ginfo.creator.mid
                msg.contentType = 13
                msg.contentMetadata = {'mid': gCreator}
                cl.sendMessage(msg)
		cl.sendText(msg.to,"It's Who Made This Group")
#--------------------------------------------------------
            elif msg.contentType == 16:
                if wait["Timeline"] == True:
                    msg.contentType = 0
                    msg.text = "post URL\n" + msg.contentMetadata["postEndUrl"]
                    cl.sendText(msg.to,msg.text)
#--------------------------------------------------------
            elif msg.text in ["Key","help","Help"]:
                cl.sendText(msg.to,helpMessage)
#--------------------------------------------------------
            elif msg.text in ["List group"]:
                gid = cl.getGroupIdsJoined()
                h = ""
		jml = 0
                for i in gid:
		    gn = cl.getGroup(i).name
                    h += "♦【%s】\n" % (gn)
		    jml += 1
                cl.sendText(msg.to,"======[List Group]======\n"+ h +"Total group: "+str(jml))
#--------------------------------------------------------
	    elif "Leave group: " in msg.text:
		ng = msg.text.replace("Leave group: ","")
		gid = cl.getGroupIdsJoined()
                for i in gid:
                    h = cl.getGroup(i).name
		    if h == ng:
			cl.sendText(i,"Bye "+h+"~")
		        cl.leaveGroup(i)
			cl.sendText(msg.to,"Success left ["+ h +"] group")
		    else:
			pass
#--------------------------------------------------------
#--------------------------------------------------------
            elif msg.text in ["cancel","Cancel"]:
                if msg.toType == 2:
					if msg.from_ in admin:
						X = cl.getGroup(msg.to)
						if X.invitee is not None:
							gInviMids = [contact.mid for contact in X.invitee]
							cl.cancelGroupInvitation(msg.to, gInviMids)
						else:
							cl.sendText(msg.to,"No one is inviting")
					else:
						Cl.sendText(msg.to,"Can not be used outside the group")
#--------------------------------------------------------
            elif msg.text in ["Ourl","Url:on"]:
                if msg.toType == 2:
					if msg.from_ in admin:
						X = cl.getGroup(msg.to)
						X.preventJoinByTicket = False
						cl.updateGroup(X)
						cl.sendText(msg.to,"Url Active")
					else:
						cl.sendText(msg.to,"Can not be used outside the group")
#--------------------------------------------------------
            elif msg.text in ["Curl","Url:off"]:
                if msg.toType == 2:
					if msg.from_ in admin:
						X = cl.getGroup(msg.to)
						X.preventJoinByTicket = True
						cl.updateGroup(X)
						cl.sendText(msg.to,"Url inActive")

					else:
						cl.sendText(msg.to,"Can not be used outside the group")
#--------------------------------------------------------
            elif msg.text in ["Join on","Autojoin:on"]:
				if msg.from_ in admin:
					wait["AutoJoin"] = True
					cl.sendText(msg.to,"AutoJoin Active")

            elif msg.text in ["Join off","Autojoin:off"]:
				if msg.from_ in admin:
					wait["AutoJoin"] = False
					cl.sendText(msg.to,"AutoJoin inActive")

#--------------------------------------------------------
            elif msg.text in ["Autocancel:on"]:
				if msg.from_ in admin:
					wait["AutoCancel"] = True
					cl.sendText(msg.to,"The group of people and below decided to automatically refuse invitation")
					print wait["AutoCancel"][msg.to]
					
            elif msg.text in ["Autocancel:off"]:
				if msg.from_ in admin:
					wait["AutoCancel"] = False
					cl.sendText(msg.to,"Invitation refused turned off")
					print wait["AutoCancel"][msg.to]
#--------------------------------------------------------
            elif msg.text in ["Qr:on"]:
				if msg.from_ in admin:
					wait["Qr"] = True
					cl.sendText(msg.to,"QR Protect Active")
					print "Command Qr:on executed"
					
            elif "Qr:off" in msg.text:
				if msg.from_ in admin:
					wait["Qr"] = False
					cl.sendText(msg.to,"Qr Protect inActive")
					print "Command Qr:off executed"
#--------------------------------------------------------
            elif "Autokick:on" in msg.text:
				if msg.from_ in admin:
					wait["AutoKick"] = True
					cl.sendText(msg.to,"AutoKick Active")

            elif "Autokick:off" in msg.text:
				if msg.from_ in admin:
					wait["AutoKick"] = False
					cl.sendText(msg.to,"AutoKick inActive")
#--------------------------------------------------------
            elif msg.text in ["K on","Contact:on"]:
				if msg.from_ in admin:
					wait["Contact"] = True
					cl.sendText(msg.to,"Contact Active")

            elif msg.text in ["K off","Contact:off"]:
				if msg.from_ in admin:
					wait["Contact"] = False
					cl.sendText(msg.to,"Contact inActive")
#--------------------------------------------------------
            elif msg.text in ["Status"]:
				if msg.from_ in admin:
					md = ""
					if wait["AutoJoin"] == True: md+="✦ Auto join : on\n"
					else: md +="✦ Auto join : off\n"
					if wait["Contact"] == True: md+="✦ Info Contact : on\n"
					else: md+="✦ Info Contact : off\n"
					if wait["AutoCancel"] == True:md+="✦ Auto cancel : on\n"
					else: md+= "✦ Auto cancel : off\n"
					if wait["Qr"] == True: md+="✦ Qr Protect : on\n"
					else:md+="✦ Qr Protect : off\n"
					if wait["AutoKick"] == True: md+="✦ Autokick : on\n"
					else:md+="✦ Autokick : off"
					cl.sendText(msg.to,"=====[Status]=====\n"+md)
#--------------------------------------------------------
            elif msg.text in ["Gift","gift"]:
				if msg.from_ in admin:
					msg.contentType = 9
					msg.contentMetadata={'PRDID': 'a0768339-c2d3-4189-9653-2909e9bb6f58',
										'PRDTYPE': 'THEME',
										'MSGTPL': '5'}
					msg.text = None
					cl.sendMessage(msg)


            elif msg.text in ["Gift1"]:
				if msg.from_ in admin:
					msg.contentType = 9
					msg.contentMetadata={'PRDID': '696d7046-843b-4ed0-8aac-3113ed6c0733',
										'PRDTYPE': 'THEME',
										'MSGTPL': '6'}
					msg.text = None
					cl.sendMessage(msg)

            elif msg.text in ["Gift2"]:
				if msg.from_ in admin:
					msg.contentType = 9
					msg.contentMetadata={'PRDID': '8fe8cdab-96f3-4f84-95f1-6d731f0e273e',
										'PRDTYPE': 'THEME',
										'MSGTPL': '7'}
					msg.text = None
					cl.sendMessage(msg)

            elif msg.text in ["Gift3"]:
				if msg.from_ in admin:
					msg.contentType = 9
					msg.contentMetadata={'PRDID': 'ae3d9165-fab2-4e70-859b-c14a9d4137c4',
										'PRDTYPE': 'THEME',
										'MSGTPL': '8'}
					msg.text = None
					cl.sendMessage(msg)

#--------------------------------------------------------
            elif "tagbyone" == msg.text:
            	 if msg.from_ in admin:
                  group = cl.getGroup(msg.to)
                  mem = [contact.mid for contact in group.members]
                  for mm in mem:
                      xname = cl.getContact(mm).displayName
                      xlen = str(len(xname)+1)
                      msg.contentType = 0
                      msg.text = "@"+xname+" "
                      msg.contentMetadata = {'MENTION':'{"MENTIONEES":[{"S":"0","E":'+json.dumps(xlen)+',"M":'+json.dumps(mm)+'}]}','EMTVER':'4'}
                  try:
                      cl.sendMessage(msg)
                  except Exception as e:
                      print str(e)
				
            elif msg.text in ["tagbyall"]:
            	 if msg.from_ in admin:
                  group = cl.getGroup(msg.to)
                  nama = [contact.mid for contact in group.members]

                  cb = ""
                  cb2 = ""
                  strt = int(0)
                  akh = int(0)
                  for md in nama:
                      akh = akh + int(6)

                      cb += """{"S":"""+json.dumps(str(strt))+""","E":"""+json.dumps(str(akh))+""","M":"""+json.dumps(md)+"},"""

                      strt = strt + int(7)
                      akh = akh + 1
                      cb2 += "@nrik \n"

                  cb = (cb[:int(len(cb)-1)])
                  msg.contentType = 0
                  msg.text = cb2
                  msg.contentMetadata ={'MENTION':'{"MENTIONEES":['+cb+']}','EMTVER':'4'}

                  try:
                      cl.sendMessage(msg)
                      cl.sendText(msg.to, "╠═ATTENDANCE═╣")
                  except Exception as error:
                      print error

#--------------------------CEK SIDER------------------------------
            # elif "Setlastpoint" in msg.text:
                # subprocess.Popen("echo '' > dataSeen/"+msg.to+".txt", shell=True, stdout=subprocess.PIPE)
                # #cl.sendText(msg.to, "Checkpoint checked!")
                # cl.sendText(msg.to, "Set the lastseens' point(｀・ω・´)\n\n" + datetime.now().strftime('%H:%M:%S'))
                # print "Setlastpoint"
# #--------------------------------------------
            # elif "Viewlastseen" in msg.text:
	        # lurkGroup = ""
	        # dataResult, timeSeen, contacts, userList, timelist, recheckData = [], [], [], [], [], []
                # with open('dataSeen/'+msg.to+'.txt','r') as rr:
                    # contactArr = rr.readlines()
                    # for v in xrange(len(contactArr) -1,0,-1):
                        # num = re.sub(r'\n', "", contactArr[v])
                        # contacts.append(num)
                        # pass
                    # contacts = list(set(contacts))
                    # for z in range(len(contacts)):
                        # arg = contacts[z].split('|')
                        # userList.append(arg[0])
                        # timelist.append(arg[1])
                    # uL = list(set(userList))
                    # for ll in range(len(uL)):
                        # try:
                            # getIndexUser = userList.index(uL[ll])
                            # timeSeen.append(time.strftime("%d日 %H:%M:%S", time.localtime(int(timelist(getIndexUser)) / 1000)))
                            # recheckData.append(userList(getIndexUser))
                        # except IndexError:
                            # conName.append('nones')
                            # pass
                    # contactId = cl.getContacts(recheckData)
                    # for v in range(len(recheckData)):
                        # dataResult.append(contactId[v].displayName + ' ('+timeSeen[v]+')')
                        # pass
                    # if len(dataResult) > 0:
                        # grp = '\n• '.join(str(f) for f in dataResult)
                        # total = '\nThese %iuesrs have seen at the lastseen\npoint(｀・ω・´)\n\n%s' % (len(dataResult), datetime.now().strftime('%H:%M:%S') )
                        # cl.sendText(msg.to, "• %s %s" % (grp, total))
                    # else:
                        # cl.sendText(msg.to, "Sider ga bisa di read cek setpoint dulu bego tinggal ketik\nSetlastpoint\nkalo mau liat sider ketik\nViewlastseen")
                    # print "Viewlastseen"
            # elif "Setview" in msg.text:
                # subprocess.Popen("echo '' > dataSeen/"+msg.to+".txt", shell=True, stdout=subprocess.PIPE)
                # cl.sendText(msg.to, "Checkpoint checked!")
                # print "@setview"

            # elif "Viewseen" in msg.text:
	        # lurkGroup = ""
	        # dataResult, timeSeen, contacts, userList, timelist, recheckData = [], [], [], [], [], []
                # with open('dataSeen/'+msg.to+'.txt','r') as rr:
                    # contactArr = rr.readlines()
                    # for v in xrange(len(contactArr) -1,0,-1):
                        # num = re.sub(r'\n', "", contactArr[v])
                        # contacts.append(num)
                        # pass
                    # contacts = list(set(contacts))
                    # for z in range(len(contacts)):
                        # arg = contacts[z].split('|')
                        # userList.append(arg[0])
                        # timelist.append(arg[1])
                    # uL = list(set(userList))
                    # for ll in range(len(uL)):
                        # try:
                            # getIndexUser = userList.index(uL[ll])
                            # timeSeen.append(time.strftime("%H:%M:%S", time.localtime(int(timelist[getIndexUser]) / 1000)))
                            # recheckData.append(userList[getIndexUser])
                        # except IndexError:
                            # conName.append('nones')
                            # pass
                    # contactId = cl.getContacts(recheckData)
                    # for v in range(len(recheckData)):
                        # dataResult.append(contactId[v].displayName + ' ('+timeSeen[v]+')')
                        # pass
                    # if len(dataResult) > 0:
                        # tukang = "List Viewer\n*"
                        # grp = '\n* '.join(str(f) for f in dataResult)
                        # total = '\n\nTotal %i viewers (%s)' % (len(dataResult), datetime.now().strftime('%H:%M:%S') )
                        # cl.sendText(msg.to, "%s %s %s" % (tukang, grp, total))
                    # else:
                        # cl.sendText(msg.to, "Belum ada viewers")
                    # print "@viewseen"
#--------------------------------------------------------

#KICK_BY_TAG
	    elif "Boom " in msg.text:
            	 if msg.from_ in admin:
					if 'MENTION' in msg.contentMetadata.keys()!= None:
						names = re.findall(r'@(\w+)', msg.text)
						mention = ast.literal_eval(msg.contentMetadata['MENTION'])
						mentionees = mention['MENTIONEES']
						print mentionees
						for mention in mentionees:
							cl.kickoutFromGroup(msg.to,[mention['M']])

#--------------------------------------------------------
	    elif "Add all" in msg.text:
            	 if msg.from_ in admin:
					thisgroup = cl.getGroups([msg.to])
					Mids = [contact.mid for contact in thisgroup[0].members]
					mi_d = Mids[:33]
					cl.findAndAddContactsByMids(mi_d)
					cl.sendText(msg.to,"Success Add all")
#--------------------------------------------------------
	    elif "Recover" in msg.text:
            	 if msg.from_ in admin:
					thisgroup = cl.getGroups([msg.to])
					Mids = [contact.mid for contact in thisgroup[0].members]
					mi_d = Mids[:33]
					cl.createGroup("Recover", mi_d)
					cl.sendText(msg.to,"Success recover")
#--------------------------------------------------------
	    # elif msg.text in ["Remove all chat"]:
            	 # if msg.from_ in admin:
					# cl.removeAllMessages(op.param2)
					# cl.sendText(msg.to,"Removed all chat")
#--------------------------------------------------------
            elif ("Gn: " in msg.text):
                if msg.toType == 2:
					if msg.from_ in admin:
						X = cl.getGroup(msg.to)
						X.name = msg.text.replace("Gn: ","")
						cl.updateGroup(X)
					else:
						cl.sendText(msg.to,"It can't be used besides the group.")
#--------------------------------------------------------
            elif "Kick: " in msg.text:
            	 if msg.from_ in admin:
					midd = msg.text.replace("Kick: ","")
					if midd not in admin:
						 cl.kickoutFromGroup(msg.to,[midd])
					else:
						 cl.sendText(msg.to,"Admin Detected")
#--------------------------------------------------------
            elif "Invite: " in msg.text:
            	 if msg.from_ in admin:
					midd = msg.text.replace("Invite: ","")
					cl.findAndAddContactsByMid(midd)
					cl.inviteIntoGroup(msg.to,[midd])
#--------------------------------------------------------
            # elif msg.text in ["#welcome","Welcome","welcome","Welkam","welkam"]:
                # gs = cl.getGroup(msg.to)
                # cl.sendText(msg.to,"Selamat datang di "+ gs.name)
#--------------------------------------------------------
            elif "Bc: " in msg.text:
            	if msg.from_ in admin:
					bc = msg.text.replace("Bc: ","")
					gid = cl.getGroupIdsJoined()
					for i in gid:
						cl.sendText(i,"=======[BROADCAST]=======\n\n"+bc+"\n\nContact Me : line.me/ti/p/~@xpk5386g")
					cl.sendText(msg.to,"Success BC BosQ")
#--------------------------------------------------------
            elif msg.text in ["Cancelall"]:
                gid = cl.getGroupIdsInvited()
                for i in gid:
                    cl.rejectGroupInvitation(i)
                cl.sendText(msg.to,"All invitations have been refused")
#--------------------------------------------------------
            elif msg.text in ["Gurl"]:
                if msg.toType == 2:
                    x = cl.getGroup(msg.to)
                    if x.preventJoinByTicket == True:
                        x.preventJoinByTicket = False
                        cl.updateGroup(x)
                    gurl = cl.reissueGroupTicket(msg.to)
                    cl.sendText(msg.to,"line://ti/g/" + gurl)
                else:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"Can't be used outside the group")
                    else:
                        cl.sendText(msg.to,"Not for use less than group")
#--------------------------------------------------------
	    elif msg.text in ["Self Like"]:
		try:
		    print "activity"
		    url = cl.activity(limit=1)
		    print url
		    cl.like(url['result']['posts'][0]['userInfo']['mid'], url['result']['posts'][0]['postInfo']['postId'], likeType=1001)
		    cl.comment(url['result']['posts'][0]['userInfo']['mid'], url['result']['posts'][0]['postInfo']['postId'], "Mau Bot Protect?\nFollow ig : @rid1bdbx\nLalu dm ke dia")
		    cl.sendText(msg.to, "Success~")
		except Exception as E:
		    try:
			cl.sendText(msg.to,str(E))
		    except:
			pass

#--------------------------------------------------------
            elif msg.text in ["Sp","Speed","speed"]:
                start = time.time()
		print("Speed")
                elapsed_time = time.time() - start
		cl.sendText(msg.to, "Progress...")
                cl.sendText(msg.to, "%sseconds" % (elapsed_time))

#--------------------------------------------------------
            elif msg.text in ["Ban"]:
                wait["wblacklist"] = True
                cl.sendText(msg.to,"send contact")

            elif msg.text in ["Unban"]:
                wait["dblacklist"] = True
                cl.sendText(msg.to,"send contact")
#--------------------------------------------------------
	    elif "Backup me" in msg.text:
		try:
		    cl.updateDisplayPicture(profile.pictureStatus)
		    cl.updateProfile(profile)
		    cl.sendText(msg.to, "Success backup profile")
		except Exception as e:
		    cl.sendText(msg.to, str(e))
#--------------------------------------------------------
	    elif "Copy " in msg.text:
                copy0 = msg.text.replace("Copy ","")
                copy1 = copy0.lstrip()
                copy2 = copy1.replace("@","")
                copy3 = copy2.rstrip()
                _name = copy3
		group = cl.getGroup(msg.to)
		for contact in group.members:
		    cname = cl.getContact(contact.mid).displayName
		    if cname == _name:
			cl.CloneContactProfile(contact.mid)
			cl.sendText(msg.to, "Success~")
		    else:
			pass
		
#--------------------------------------------------------
            elif "Ban @" in msg.text:
                if msg.toType == 2:
                    print "@Ban by mention"
                    _name = msg.text.replace("Ban @","")
                    _nametarget = _name.rstrip('  ')
                    gs = cl.getGroup(msg.to)
                    targets = []
                    for g in gs.members:
                        if _nametarget == g.displayName:
                            targets.append(g.mid)
                    if targets == []:
                        cl.sendText(msg.to,"Not found")
                    else:
                        for target in targets:
			    if target not in admin:
                                try:
                                    wait["blacklist"][target] = True
                                    f=codecs.open('st2__b.json','w','utf-8')
                                    json.dump(wait["blacklist"], f, sort_keys=True, indent=4,ensure_ascii=False)
                                    cl.sendText(msg.to,"Succes BosQ")
                                except:
                                    cl.sendText(msg.to,"Error")
			    else:
				cl.sendText(msg.to,"Admin Detected~")
#--------------------------------------------------------
            elif msg.text in ["Banlist"]:
                if wait["blacklist"] == {}:
                    cl.sendText(msg.to,"nothing")
                else:
                    mc = ""
                    for mi_d in wait["blacklist"]:
                        mc += "->" +cl.getContact(mi_d).displayName + "\n"
                    cl.sendText(msg.to,"===[Blacklist User]===\n"+mc)

#--------------------------------------------------------
            elif "Unban @" in msg.text:
                if msg.toType == 2:
                    print "@Unban by mention"
                    _name = msg.text.replace("Unban @","")
                    _nametarget = _name.rstrip('  ')
                    gs = cl.getGroup(msg.to)
                    targets = []
                    for g in gs.members:
                        if _nametarget == g.displayName:
                            targets.append(g.mid)
                    if targets == []:
                        cl.sendText(msg.to,"Not found")
                    else:
                        for target in targets:
                            try:
                                del wait["blacklist"][target]
                                f=codecs.open('st2__b.json','w','utf-8')
                                json.dump(wait["blacklist"], f, sort_keys=True, indent=4,ensure_ascii=False)
                                cl.sendText(msg.to,"Succes BosQ")
                            except:
                                cl.sendText(msg.to,"Succes BosQ")
#--------------------------------------------------------
            elif msg.text in ["Kill ban"]:
                if msg.toType == 2:
                    group = cl.getGroup(msg.to)
                    gMembMids = [contact.mid for contact in group.members]
                    matched_list = []
                    for tag in wait["blacklist"]:
                        matched_list+=filter(lambda str: str == tag, gMembMids)
                    if matched_list == []:
                        cl.sendText(msg.to,"There was no blacklist user")
                        return
                    for jj in matched_list:
                        cl.kickoutFromGroup(msg.to,[jj])
                    cl.sendText(msg.to,"Blacklist emang pantas tuk di usir")
					
            elif msg.text in ["re:invite"]:
            	 if msg.from_ in admin:
						X = cl.getGroup(msg.to)
						X.preventJoinByTicket = False
						cl.updateGroup(X)
						invsend = 0
						Ti = cl.reissueGroupTicket(msg.to)
						cl.acceptGroupInvitationByTicket(msg.to,Ti)
						cl.sendText(msg.to,"Progress█░░░░░░░ 10%")
						time.sleep(0.001)
						cl.sendText(msg.to,"Progress██░░░░░░ 28%")
						time.sleep(0.001)
						cl.sendText(msg.to,"Progress█████░░░ 65%")
						time.sleep(0.001)
						cl.sendText(msg.to,"Progress██████████ 100%")
						time.sleep(0.001)
						G = cl.getGroup(msg.to)
						G.preventJoinByTicket = True
						cl.updateGroup(G)
						Ticket = cl.reissueGroupTicket(msg.to)
						print "[Command]reinvite executed]"
						cl.sendText(msg.to,"Done")

                    
            elif "Tr-id " in msg.text:
                isi = msg.text.replace("Tr-id ","")
                translator = Translator()
                hasil = translator.translate(isi, dest='id')
                A = hasil.text
                A = A.encode('utf-8')
                cl.sendText(msg.to, A)
            elif "Tr-en " in msg.text:
                isi = msg.text.replace("Tr-en ","")
                translator = Translator()
                hasil = translator.translate(isi, dest='en')
                A = hasil.text
                A = A.encode('utf-8')
                cl.sendText(msg.to, A)
            elif "Tr-ar" in msg.text:
                isi = msg.text.replace("Tr-ar ","")
                translator = Translator()
                hasil = translator.translate(isi, dest='ar')
                A = hasil.text
                A = A.encode('utf-8')
                cl.sendText(msg.to, A)
            elif "Tr-jp" in msg.text:
                isi = msg.text.replace("Tr-jp ","")
                translator = Translator()
                hasil = translator.translate(isi, dest='ja')
                A = hasil.text
                A = A.encode('utf-8')
                cl.sendText(msg.to, A)
            elif "Tr-ko" in msg.text:
                isi = msg.text.replace("Tr-ko ","")
                translator = Translator()
                hasil = translator.translate(isi, dest='ko')
                A = hasil.text
                A = A.encode('utf-8')
                cl.sendText(msg.to, A)

            elif "Tr-tag" in msg.text:
                isi = msg.text.replace("Tr-tag ","")
                translator = Translator()
                hasil = translator.translate(isi, dest='tl')
                A = hasil.text
                A = A.encode('utf-8')
                cl.sendText(msg.to, A)
				
	    elif msg.text in ["Kalender","/waktu"]:
                timeNow = datetime.now()
                timeHours = datetime.strftime(timeNow,"(%H:%M)")
                day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                inihari = datetime.today()
                hr = inihari.strftime('%A')
                bln = inihari.strftime('%m')
                for i in range(len(day)):
                    if hr == day[i]: hasil = hari[i]
                for k in range(0, len(bulan)):
                    if bln == str(k): blan = bulan[k-1]
                rst = hasil + ", " + inihari.strftime('%d') + " - " + blan + " - " + inihari.strftime('%Y') + "\nJam : [ " + inihari.strftime('%H:%M:%S') + " ]"
                cl.sendText(msg.to, rst)
#--------------------------------------------------------
#            elif "Cleanse" in msg.text:
#                if msg.toType == 2:
#                    print "Kick all member"
#                    _name = msg.text.replace("Cleanse","")
#                    gs = cl.getGroup(msg.to)
#                    cl.sendText(msg.to,"Dadaaah~")
#                    targets = []
#                    for g in gs.members:
#                        if _name in g.displayName:
#                            targets.append(g.mid)
#                    if targets == []:
#                        cl.sendText(msg.to,"Not found.")
#                    else:
#                        for target in targets:
#			     if target not in admin:
#                                try:
#                                    cl.kickoutFromGroup(msg.to,[target])
#                                    print (msg.to,[g.mid])
#                                except Exception as e:
#                                    cl.sendText(msg.to,str(e))
#			 cl.inviteIntoGroup(msg.to, targets)

#--------------------------------------------------------
#Restart_Program
	    elif msg.text in ["Reboot"]:
		cl.sendText(msg.to, "Bot has been restarted")
		restart_program()
		print "@Restart"
		
		
            elif "Turn off bots" in msg.text:
               if msg.from_ in Creator:
                 try:
                     import sys
                     sys.exit()
                 except:
                     pass
#--------------------------------------------------------



        if op.type == 59:
            print op


    except Exception as error:
        print error


#thread2 = threading.Thread(target=nameUpdate)
#thread2.daemon = True
#thread2.start()

while True:
    try:
        Ops = cl.fetchOps(cl.Poll.rev, 5)
    except EOFError:
        raise Exception("It might be wrong revision\n" + str(cl.Poll.rev))

    for Op in Ops:
        if (Op.type != OpType.END_OF_OPERATION):
            cl.Poll.rev = max(cl.Poll.rev, Op.revision)
            bot(Op)

