import socket
from flask import Flask, render_template, request,redirect,url_for,session,jsonify, make_response, Response
import pymysql
from datetime import datetime
import configs
import paho.mqtt.client as mqtt
import json
import cv2 as cv
import os
from flask_socketio import SocketIO,emit 
import time
from flask_apscheduler import APScheduler
from threading import Thread
import asyncio
import websockets
import io
import asyncio
import pathlib
import ssl
from apscheduler.schedulers.blocking import BlockingScheduler
import tkinter as tk
from tkinter import messagebox

MQTT_server = '59.120.184.124'
MQTT_port = 1883
app = Flask(__name__)
app.config.from_object(configs)
app.secret_key = b'pD.\x93\x06xQ\xc9\x80\xec\xb1X'
socketio = SocketIO(app)  
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


#註冊介面
@app.route('/Register/', methods=["POST","GET"])
def index_R():
    if request.method == "POST":
        reg_data = [request.form["userid"],request.form["userpw"],
                    request.form["username"], request.form["userphone"]]
        print("reg_data",reg_data)
        check_AC_flag,usermsg = check_AC(reg_data[0])
        if check_AC_flag:
            registration_result = user_register(check_AC_flag, reg_data)
            if registration_result == 'register finish':
                return redirect(url_for('index_Login', RAC = usermsg, L_PW_Error="?"))
            else:
                return render_template('register.html', RAC = usermsg)
        else:
            return render_template('register.html', RAC = usermsg)
    else:
        return render_template('register.html')

@app.route('/Login/', methods=['POST',"GET"])
def index_Login():
    account =""
    pw = ""
    if request.method == "POST":
        account = request.form["userid"]
        pw = request.form["userpw"]
        L_AC_flag, L_PW_flag, ACE_Error, privacy_accepted = LLogin(account, pw)
        session["privacy_accepted"] = privacy_accepted
        print(account,L_AC_flag,pw,L_PW_flag,ACE_Error)
        ace_counter = session.get('ACE_Error', 0)
        if L_AC_flag and L_PW_flag:
            session["AC"] = account
            ACE_Error = 0
            if privacy_accepted == False : 
                return redirect(url_for('index_P'))
            else: return render_template('Management.html')
        elif L_AC_flag and not L_PW_flag:
            return render_template('login.html', L_PW_Error=str(ACE_Error))
        else:
            return render_template('login.html', L_PW_Error="?")
    else:
        return render_template('login.html', L_PW_Error="?")
    

@app.route('/Privacy/', methods=["POST","GET"])
def index_P():
    if 'AC' not in session:
        return redirect(url_for('index_Login'))
    if session.get('privacy_accepted', False):
        return redirect(url_for('index_M'))

    if request.method == "POST":
        value = request.form["reprivacy"]
        if value == "取消":
            return redirect(url_for('index_Login'))
        elif value == "確認":
            account = session['AC']
            update_privacy_accepted(account)
            session['privacy_accepted'] = True
            return redirect(url_for('index_M'))
        else:
            return redirect(url_for('index_M', L_PW_Error="?"))
    else:
        return render_template('privacy.html', L_PW_Error="?")

        
            
@app.route('/Mange/', methods=["POST","GET"])
def index_M():
    if "AC" in session and session['AC'] != "account is stop":
        return render_template('Management.html')
    else: return redirect(url_for('index_Login',L_PW_Error = "?"))


@app.route('/Logout/', methods=["POST","GET"])
def index_Logout():
    if request.method == "POST":
        value = request.form["response"]
        print(value)
        if value != "返回系統":
            session.pop('AC',None)
            session.pop('Dname',None)
            session.pop('Duuid',None)
            return render_template('login.html',L_PW_Error = "?")
        else: return redirect(url_for('index_M'))
    else: return render_template('logout.html')

#AM
@app.route('/MangeAT/', methods=["POST","GET"])
def index_AM():
    if "AC" in session and session['AC'] != "account is stop":
        return render_template('AccountManag.html')
    else: return redirect(url_for('index_AM',L_PW_Error = "?"))

@app.route('/AMange/', methods=["GET","POST"])
def AMange():
    if "AC" in session and session['AC'] != "account is stop":
        if request.method == "POST":
            print("/AMange/Response",request.form['Dname'], request.form['Duuid'])
            session['Dname']= request.form['Dname']
            session['Duuid'] = request.form['Duuid']
            print('response',request.form['Dname'], request.form['Duuid'])
            print('session',session['Dname'],session['Duuid'])
            post_drone_info ()
            #return redirect(url_for('AM_Dinfo'))
        else: return render_template('Account.html',DName_ls= drone_list())
    else: return redirect(url_for('index_Login',L_PW_Error = "?"))

@app.route('/Fleet/', methods=["GET"])
def Fleet():
    if "AC" in session and session['AC'] != "account is stop":
        print(session)
        return render_template('Fleet.html')
    else: return redirect(url_for('index_Login',L_PW_Error = "?"))

@app.route('/AMange/Dinfo/', methods=["GET"])
def AM_Dinfo():
    if "AC" in session and session['AC'] != "account is stop":
        print(session)
        return render_template('AccountInfo.html')
    else: return redirect(url_for('index_Login',L_PW_Error = "?"))

@app.route('/AMange/DTdata/', methods=["GET"])
def AM_DTdata():
    if "AC" in session and session['AC'] != "account is stop":
        return render_template('AccountFlyHistory.html')
    else: return redirect(url_for('index_Login',L_PW_Error = "?"))

@app.route('/AMange/DFRecord/', methods=["GET"])
def AM_DFRecord():
    if "AC" in session and session['AC'] != "account is stop":
        return render_template('AccountRecord.html')
    else: return redirect(url_for('index_Login',L_PW_Error = "?"))

#DM
@app.route('/DMange/', methods=["GET"])
def DMange():
    if "AC" in session and session['AC'] != "account is stop":    
        return render_template('Drone.html',DName_ls= drone_list())
    else: return redirect(url_for('index_Login',L_PW_Error = "?"))


@app.route('/DMange/DFSS/', methods=["POST","GET"])
def DM_DFSS():
    if "AC" in session and session['AC'] != "account is stop":
        return render_template('DroneMapVideo.html',DName_ls= drone_list())
    else: return redirect(url_for('index_Login',L_PW_Error = "?"))
    # if "AC" in session and session['AC'] != "account is stop":
    #     uuid = ""
    #     if uuid == msg_list['sn']:
    #         return render_template('DroneMapVideo.html',video_way = f'rtmp://topologyuav.com/gcpuser/{uuid}')
    # else: return redirect(url_for('index_Login',L_PW_Error = "?"))
    

@app.route('/DMange/DFproject/', methods=["GET"])
def DM_DFproject():
    if "AC" in session and session['AC'] != "account is stop":
        return render_template('DronePlan.html',DName_ls = drone_list())
    else: return redirect(url_for('index_Login',L_PW_Error = "?"))

@app.route('/DMange/DFSwitch/', methods=["GET"])
def DM_DFSwitch():
    if "AC" in session and session['AC'] != "account is stop":
        return render_template('DroneView.html',DName_ls = drone_list())
    else: return redirect(url_for('index_Login',L_PW_Error = "?"))

@app.route('/DMange/DFSM/', methods=["GET"])
def DM_DFSM():
    if "AC" in session and session['AC'] != "account is stop":
        return render_template('DroneViews.html',DName_ls = drone_list())
    else: return redirect(url_for('index_Login',L_PW_Error = "?"))

#MM
@app.route('/MMange/', methods=["GET"])
def MMange():
    if "AC" in session and session['AC'] != "account is stop":
        return render_template('Mission.html')
    else: return redirect(url_for('index_Login',L_PW_Error = "?"))

@app.route('/MMange/Planning/', methods=["GET"])
def MMange_DFdata():
    if "AC" in session and session['AC'] != "account is stop":
        return render_template('MissionSet.html')
    else: return redirect(url_for('index_Login',L_PW_Error = "?"))

@app.route('/MMange/RPlanning/', methods=["GET"])
def MM_DFproject():
    if "AC" in session and session['AC'] != "account is stop":
        return render_template('MissionReview.html')
    else: return redirect(url_for('index_Login',L_PW_Error = "?"))


#新增無人機
@app.route('/DMange/NDrone/', methods=['POST',"GET"])
def New_Drone():
    Drone_name = ""
    Drone_uuid = ""
    if "AC" in session and session['AC'] != "account is stop":
        if request.method == "POST":
            Drone_name = request.form['Dname']
            Drone_uuid = request.form['Duuid']
            print(Drone_name,Drone_uuid)
            Drone_MSG = get_drone_info (Drone_name,Drone_uuid)
            if Drone_MSG == "register drone finish": return redirect(url_for('DMange',DName_ls= drone_list()))
            else: return render_template('addDrone.html',Drone_MSG = Drone_MSG)
        else:
            return render_template('addDrone.html',Drone_MSG = "?")
    else: return redirect(url_for('index_Login',L_PW_Error = "?"))

# 登入檢測
def LLogin(account,pw):
    L_AC_flag = False 
    L_PW_flag = False
    dense_db = pymysql.connect(host='localhost',port=3306,user='account_user',
                passwd='A22_92ws', db='userdatabase',charset='utf8')
    dense_cursor = dense_db.cursor()
    L_sql = f"select * from denseinfo"
    drone_ls_len = dense_cursor.execute(L_sql)
    drone_ls = dense_cursor.fetchall()
    for i in range(0,drone_ls_len):
        if account == drone_ls[i][0] and account!='' and len(pw)>= 8:
            ACE_counter = drone_ls[i][2]
            privacy_accepted = drone_ls[i][3]
            if pw == drone_ls[i][1] and ACE_counter <3:
                L_AC_flag = True
                L_PW_flag = True
                ACE_counter = 0
            else:
                if ACE_counter >= 3: 
                    L_AC_flag = True
                    L_PW_flag = False
                    session["AC"] = 'account is stop'
                else:
                    ACE_counter += 1
                    L_PW_flag = False
            print(f'error {ACE_counter}')
            if privacy_accepted == 0:
                return L_AC_flag, L_PW_flag, ACE_counter, False 
            else:
                return L_AC_flag, L_PW_flag, ACE_counter, True 
        else: ACE_counter = 0
    dense_db.commit()
    dense_db.close()
    return L_AC_flag, L_PW_flag, ACE_counter, False 

# 使用者帳戶檢查
def check_AC(user_AC):
    msg = ''
    dense_db = pymysql.connect(host='localhost',port=3306,user='account_user',
                                passwd='A22_92ws',db='userdatabase',charset='utf8')
    dense_cursor = dense_db.cursor()
    exam_sql = f"select account from denseinfo;"
    exam_len = dense_cursor.execute(exam_sql)
    user_account = dense_cursor.fetchall()
    AC_counter = 0
    print('exam_len',exam_len)
    for i in range(0,exam_len):
        if user_AC =='': 
            msg = 'No account'
            check_AC_flag = False
            break
        elif user_account[i][0] != user_AC and user_AC != '': AC_counter += 1 
        elif user_account[i][0] == None: 
            msg = 'account is available'
            check_AC_flag = True

    if AC_counter == exam_len:
        msg = 'account is available'
        check_AC_flag = True
    else: 
        msg ='the same account'
        check_AC_flag = False
    print(check_AC_flag,msg)
    dense_db.close()
    return check_AC_flag, msg

# 使用者註冊
def user_register(check_flag,reg_data):
    dense_db = pymysql.connect(host='localhost', port=3306, user='account_user',
                    passwd='A22_92ws', db='userdatabase', charset='utf8')
    user_db = pymysql.connect(host='localhost', port=3306, user='user_name',
                        passwd='A1ot_use', db='userdatabase', charset='utf8')
    user_cursor = user_db.cursor()
    dense_cursor = dense_db.cursor()
    if check_flag == True:
        dense_sql = f"INSERT IGNORE INTO `denseinfo`  (account, pw, Error_count) VALUES('{reg_data[0]}','{reg_data[1]}','0');"
        Repeat_densesql = f"select account from denseinfo where account like binary '{reg_data[0]}'"
        Repeat_dense_len = dense_cursor.execute(Repeat_densesql)
        if Repeat_dense_len == 0: 
            dense_cursor.execute(dense_sql)
            dense_db.commit()
            dense_db.close()
            Repeat_usersql = f"select account from userdroneinfo where account like binary'{reg_data[0]}'"
            user_sql = f"INSERT IGNORE INTO `userdroneinfo` (account,drone_name,uuid,user_name,tellphone) VALUES('{reg_data[0]}','','','{reg_data[2]}','{reg_data[3]}');"
            user_len = user_cursor.execute(Repeat_usersql)
            if user_len == 0:
                user_cursor.execute(user_sql)
                user_db.commit()
                user_db.close()
                usermsg ='register finish'
            else: usermsg ='register failed'
        else:
                usermsg = 'register failed'
    else:
        usermsg = 'register failed'
    return usermsg

#更新隱私權次數
def update_privacy_accepted(account):
    dense_db = pymysql.connect(host='localhost',port=3306,user='account_user',
                passwd='A22_92ws', db='userdatabase',charset='utf8')
    dense_cursor = dense_db.cursor()
    prysql = f"UPDATE denseinfo SET privacy_accepted = '1' WHERE account = '{account}';"
    dense_cursor.execute(prysql)
    dense_db.commit() 
    dense_cursor.close()


# 新增無人機
def get_drone_info (drone_name,drone_uuid):
    user_db = pymysql.connect(host='localhost',port=3306, user='user_name',
                        passwd='A1ot_use', db='userdatabase',charset='utf8')
    user_cursor = user_db.cursor()
    print(drone_name,drone_uuid)
    drone_msg = ''
    counter = 0
    uuid_sql = f"select uuid from userdroneinfo where uuid like binary'{drone_uuid}';"
    info_len = user_cursor.execute(uuid_sql)
    print('uuid',info_len,'uuid len',len(drone_uuid))
    if drone_name != '' and drone_uuid != '' and len(drone_uuid) == 15 and info_len < 1:
        Uname_sql = f"select drone_name from userdroneinfo where account like binary'{session['AC']}';"
        Uinfo_len = user_cursor.execute(Uname_sql)
        get_Uinfo_data = user_cursor.fetchall()
        print('Uav name numbers',Uinfo_len)
        # print(get_Uinfo_data,end='\t')
        for i in range(0,Uinfo_len):
            print(get_Uinfo_data[i][0])
            if get_Uinfo_data[0][0] == '' or get_Uinfo_data[0][0] == ' ':
                Dname_sql = f"update userdroneinfo drone_name set drone_name = '{drone_name}' where account = '{session['AC']}';"
                user_cursor.execute(Dname_sql)
                Duuid_sql = f"update userdroneinfo uuid set uuid = '{drone_uuid}' where account = '{session['AC']}';"
                user_cursor.execute(Duuid_sql)
                user_db.commit()
                user_db.close()
                drone_msg = 'register drone finish'
                # create_fly_Ttables(data[2])
                break
            elif get_Uinfo_data[i][0] == drone_name :
                drone_msg = 'drone name the same'
                break
            else: counter += 1
        if counter == Uinfo_len:
            Duuid_sql = f"INSERT IGNORE INTO `userdroneinfo`  (account, drone_name, uuid) VALUES('{session['AC']}','{drone_name}','{drone_uuid}');"
            user_cursor.execute(Duuid_sql)
            user_db.commit()
            user_db.close()
            #create_fly_Ttables(drone_uuid)
            drone_msg = 'register drone finish'
    else:
        drone_msg ='uuid the same'
    print(drone_msg)
    return drone_msg

#創建無人機總表  待補connect
def create_fly_Ttables(drone_uuid):
    data_db = pymysql.connect(host='localhost', port=3306, 
    user='user_name', passwd='A1ot_use', db='alldronedatabases',charset='utf8')
    data_cursor = data_db.cursor()
    sql_ins = f"CREATE TABLE `Total-{drone_uuid}` ( \
                name varchar(100), sn varchar(100), \
                mission varchar(100), Time varchar(100),\
                Vcc varchar(100),Flight_Mode varchar(100),\
                lon varchar(100), lat varchar(100), alt varchar(100),\
                GPS_FIX int,Satellites_visible int,\
                ground_speed varchar(100),Vertical_speed varchar(100),\
                YAW varchar(100),Mission_status varchar(100));"
    data_cursor.execute(sql_ins)
    data_db.commit()

#無人機列表
def drone_list():
    user_db = pymysql.connect(host='localhost',port=3306, user='user_name',
                        passwd='A1ot_use', db='userdatabase',charset='utf8')
    user_cursor = user_db.cursor()
    Drone_sql = f"select drone_name,uuid from userdroneinfo where account like binary'{session['AC']}';"
    user_cursor.execute(Drone_sql)
    drone_name = user_cursor.fetchall()
    if len(drone_name) == 0:
        DName = [['No drone','No uuid']]
    else: DName =  [item for item in drone_name]
    #print(DName[0],len(DName),type(DName[0][0]))
    return DName


# 無人機 機體資訊
@socketio.on('DName')
def post_drone_info ():
    find_uuid_flag = False
    # socketio.emit(DU) # uav_uuid
    uav_db = pymysql.connect(host='localhost',port=3306, user='user_name',
                passwd='A1ot_use', db='uavmanagement',charset='utf8')
    cursor = uav_db.cursor()
    get_info = f"select * from drone;"
    grtinfo_len = cursor.execute(get_info)
    get_data = cursor.fetchall()
    for i in range(0, grtinfo_len):
        if session['Duuid'] == get_data[i][17]:
            drone_ls = {'D_name':session['Dname'],'D_n':get_data[i][0],'D_e':get_data[i][1],'D_c':get_data[i][2]
            ,'D_w':get_data[i][3],'D_s':get_data[i][4],'D_a':get_data[i][5],'D_p':get_data[i][6]
            ,'D_nl':get_data[i][7],'D_l':get_data[i][8],'D_t':get_data[i][9],'D_loiter':get_data[i][10]
            ,'D_speed':get_data[i][11],'D_TTime':get_data[i][12],'D_RW':get_data[i][13],'D_LH':get_data[i][14]
            ,'D_LR':get_data[i][15],'D_b':get_data[i][16],'D_uu':get_data[i][17],'I_n':get_data[i][18]
            ,'I_num':get_data[i][19],'I_dd':get_data[i][20],'Uav_pic':get_data[i][21],'msg': 'true uuid'}
            find_uuid_flag = True
            break
    if find_uuid_flag != True: 
        drone_ls = {'D_name':session['Dname'],'D_n':'None','D_e':'None','D_c':'None','D_w':'None','D_s':'None',
        'D_a':'None','D_p':'None','D_nl':'None','D_l':'None','D_t':'None','D_loiter':'None',
        'D_speed':'None','D_TTime':'None','D_RW':'None','D_LH':'None','D_LR':'None',
        'D_b':'None','D_uu':'None','I_n':'None','I_num':'None','I_dd':'None',
        'Uav_pic':'None','msg': 'error uuid'}
    uav_db.close()    
    #print(drone_ls)
    socketio.emit('DDinfo',drone_ls)


def on_flydata_connect(client, userdata, flags, rc):
   topic = f"drone/droneuuid"
   if rc == 0:
       print('Connected successfully',topic)
       client.subscribe(topic) # 订阅主题
   else:
       print('Bad connection. Code:', rc)

# 獲得無人機飛行資料
def on_flydata_drone_message(client, userdata, message):
    global msg_list
    msg_list = json.JSONDecoder().decode(message.payload.decode('utf-8'))
    if msg_list != 0:
        pass

    data = dict(topic=message.topic, payload=message.payload.decode())
    # print('Received message on topic: {topic} with payload: {payload}'.format(**data))

# 傳送無人機飛行資料
@socketio.on('MQTT_flydata') 
def transfer_data(drone_name,drone_uuid):
    socketio.emit(drone_name,drone_uuid) #user & uav_uuid
    # drone_name,uuid = DD
    uav_db = pymysql.connect(host='localhost',port=3306, user='user_name',
                passwd='A1ot_use', db='uavmanagement',charset='utf8')
    cursor = uav_db.cursor()
    get_info = f"select * from drone;"
    grtinfo_len = cursor.execute(get_info)
    get_data = cursor.fetchall()
    for i in range(0, grtinfo_len):
        if drone_uuid == get_data[i][17]:
            drone_ls = {'D_n':get_data[i][0],'D_t':get_data[i][9], 'D_RW':get_data[i][13], 'D_LR':get_data[i][15],}
            break
        print(drone_ls)

    all_ls = {"name":drone_name,"sn":msg_list["sn"],"Time":msg_list["Time"],"mission":msg_list["mission"], 
            "Vcc":msg_list["Vcc"], "Flight_Mode":msg_list["Flight_Mode"],
            "lon":msg_list["lon"], "lat":msg_list["lat"], "alt":msg_list["alt"],
            "GPS_FIX":msg_list["GPS_FIX"], "Satellites_visible":msg_list["Satellites_visible"],
            "groud_speed":msg_list["groud_speed"], "Vertical_speed":msg_list["Vertical_speed"], 
            "YAW":msg_list["YAW"],'timestamp': time.time()}
    socketio.emit('MQTT_flydataR',all_ls)

@scheduler.task('interval', id='menu_detail', seconds=1)
def generate_data():
    transfer_data('param1_value', 'param2_value')

def record_Tflydata(msg):
    db = pymysql.connect(host='localhost',port=3306,user='user_name',
                         passwd='A1ot_use', db=f"alldronedatabases",charset='utf8')
    cursor = db.cursor()
    table_list_sql = "show tables;"
    table_list_len = cursor.execute(table_list_sql)
    table_name_ls = cursor.fetchall()
    for i in range(0, table_list_len):
        if "Total-"+ msg['sn']== table_name_ls[i][0] and msg_list["mission"] != 'no-action':
            sql = f"INSERT INTO `Total-{msg['sn']}` (name, sn, mission,\
            Time, Vcc,Flight_Mode, lon, lat, alt, GPS_FIX,Satellites_visible,\
            ground_speed,Vertical_speed, YAW) VALUES('" +msg['name']+"','"+\
            msg['sn']+"','"+msg['mission']+"','"+ msg['Time']+"','"+ str(msg['Vcc'])+\
            "','"+ msg['Flight_Mode']+"','"+str(msg['lon'])+"','"+ str(msg['lat'])+"','"+\
            str(msg['alt'])+"','"+str(msg['GPS_FIX'])+"','"+ str(msg['Satellites_visible'])+\
            "','"+str(msg['groud_speed'])+"','"+ str(msg['Vertical_speed'])+"','"+\
            str(msg['YAW'])+"','"+ str(msg_list["mission"]-datetime.now().strftime("%Y-%m-%d"))+"');"
        
        elif "Total-"+ msg['sn']== table_name_ls[i][0]:
            sql = f"INSERT INTO `Total-{msg['sn']}` (name, sn, mission,\
            Time, Vcc,Flight_Mode, lon, lat, alt, GPS_FIX,Satellites_visible,\
            ground_speed,Vertical_speed, YAW) VALUES('" +msg['name']+"','"+\
            msg['sn']+"','"+msg['mission']+"','"+ msg['Time']+"','"+ str(msg['Vcc'])+\
            "','"+ msg['Flight_Mode']+"','"+str(msg['lon'])+"','"+ str(msg['lat'])+"','"+\
            str(msg['alt'])+"','"+str(msg['GPS_FIX'])+"','"+ str(msg['Satellites_visible'])+\
            "','"+str(msg['groud_speed'])+"','"+ str(msg['Vertical_speed'])+"','"+ str(msg['YAW'])+",None);"    
        
        cursor.execute(sql)
        #提交修改
        db.commit()

# # 存影片 
# def read_frame(mission_date,ip = '59.120.184.126', uuid =''):
#     save_path = f"/home/hj-back/Videos/{session['AC']}/{uuid}"
#     if not os.path.isdir(save_path):
#         os.makedirs(save_path)
#     video_name = save_path + mission_date + '.mp4'
#     cap = cv.VideoCapture(f'rtmp://{ip}/gcpuser/{uuid}') 
#     # Get video information
#     video_fourcc = cv.VideoWriter_fourcc(*'MJPG')
#     # 建立 VideoWriter 物件
#     writer = cv.VideoWriter(video_name, video_fourcc, int(cap.get(cv.CAP_PROP_FPS)), 
#         (int(cap.get(cv.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))) 
#     # read web camera
#     while(cap.isOpened()):
#         ret, img = cap.read()
#         if not ret:
#             writer.write(img)
#     writer.release()

def rtspVideo():
    rtsp_url = "rtsp://59.120.184.126:8554/mystream"
    cap = cv.VideoCapture(rtsp_url)

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        # 在這裡對影像進行處理（例如濾鏡、旋轉等）
        
        cv.imshow('RTSP Video', frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

def make_mission(way_points, user_name, project_name):
    with open (f'~/Desktop/{user_name}/mission/{project_name}.txt',mode='w',encoding='utf-8') as f:
        f.write(way_points)
    return "Finish"

# 使用者影片列表
def get_video_name(uuid):
    ls = [item for item in os.listdir(f"/home/hj-back/Videos/{session['AC']}/{uuid}")]



if __name__ == "__main__":
    client = mqtt.Client(clean_session=True) 
    client.on_connect = on_flydata_connect
    client.on_message = on_flydata_drone_message
    client.username_pw_set("mqttuser","mqtt42607866")
    client.connect(MQTT_server, MQTT_port, keepalive=60)
    client.loop_start()
    context = ('fullchain.pem', 'privkey.pem')
    app.run(debug=True, ssl_context=context, host="59.120.184.126",port=5002)

    
