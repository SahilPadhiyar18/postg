from telnetlib import STATUS
from this import d
from click import password_option
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

db = SQLAlchemy()
DB_NAME = "database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)

class dbms(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    rid = db.Column(db.String(1000))
    humidity = db.Column(db.String(1000))
    temp = db.Column(db.String(1000))

class motordata(db.Model):
    id =     db.Column(db.Integer,primary_key=True)
    date =   db.Column(db.String(1000))
    time =   db.Column(db.String(1000))
    status = db.Column(db.String(1000))
    onby =   db.Column(db.String(1000))

class acstatus(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    ac = db.Column(db.String(1000))
    status = db.Column(db.String(1000))

class alaram(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    motor = db.Column(db.String(1000))
    status = db.Column(db.String(1000))
    shour = db.Column(db.String(1000))
    smin = db.Column(db.String(1000))
    szone = db.Column(db.String(1000))
    ehour = db.Column(db.String(1000))
    emin = db.Column(db.String(1000))
    ezone = db.Column(db.String(1000))

class Logindata(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(1000))
    email = db.Column(db.String(1000))
    passsword = db.Column(db.String(1000))
    addkey = db.Column(db.String(1000))

@app.route('/', methods=['GET', 'POST']) 
def home_page():    
    # db.session.query(motordata).delete()
    # db.session.commit()
    # db.session.query(Logindata).delete()
    # db.session.commit()
    return render_template('login.html')

@app.route('/LoginSubmit', methods=['POST'])
def logInSubmit():
    if request.method == "POST":      
        emailid = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("ck")
        try:
            print("Step1")
            admin = Logindata.query.filter_by(email = emailid).first()
            if(admin.passsword == password):
                if(admin.id == 1):
                    return render_template('home.html',name = admin.name )
                else:
                    return render_template('user.html',name = admin.name )                    
                print("Step2")
            else:
                return render_template('login.html')
                print("Step3")
        except:
            return render_template('login.html')
            print("Step4")
        # if(str(name) == "valid":
        #     pass     
        print("Step5")  
    
@app.route('/validemail', methods=['POST'])   #login
def validemail():
    if (request.method == 'POST'):
        name = (request.json['name'])
        # print(name)
        admin = Logindata.query.filter_by(email = name).all()
        if(len(admin) >= 1):
            return "valid"
        else:
            return "not valid"

@app.route('/cheakUserName', methods=['POST'])  #signup
def CheakUserName():
    if (request.method == 'POST'):
        name = (request.json['name'])
        print(name)
        admin = Logindata.query.filter_by(email = name).all()
        if(len(admin) == 1):
            return "email exist"
        else:
            return "chek"

@app.route("/ne")
def secret():
    return render_template("signup.html")

@app.route("/home")
def home():
    return render_template("home.html")


@app.route('/signUpSubmit', methods=['POST'])
def signUpSubmit():
    if request.method == "POST":
        try:    
            name = request.form.get("ck")  
            if(str(name) == "chek"):
                add = request.form.get("fname")
                full_name = request.form.get("lname")
                emailaddr = request.form.get("email")
                passwordt = request.form.get("password")
                print("step1")
                # print(add + "s") 
                print(add) 
                if(add == "s@hil" or add == "bhus@n"):
                    t = Logindata(name =full_name, email = emailaddr ,passsword=passwordt, addkey =add)
                    db.session.add(t)
                    db.session.commit()
                    print("step2")
                    return render_template('user.html',name = full_name )
        except:
                print("step3")
    return render_template('signup.html')

@app.route('/datapage', methods=['GET', 'POST']) 
def data_page():
    # a = dbms.query.get
    dates = db.session.query(motordata.date).all()
    times = db.session.query(motordata.time).all() 
    state = db.session.query(motordata.status).all() 
    onbye = db.session.query(motordata.onby).all() 
    return render_template('datapage.html',data = dates[::-1] ,data1 = times[::-1],status = state[::-1],onby=onbye[::-1])
    
@app.route('/data', methods=['GET', 'POST']) 
def data():
    # a = dbms.query.get
    dates = db.session.query(Logindata.name).all()
    times = db.session.query(Logindata.email).all() 
    state = db.session.query(Logindata.passsword).all() 
    return render_template('data.html',data = dates[::-1] ,data1 = times[::-1],status = state[::-1])

@app.route('/switch', methods=['POST'])
def aaa():
    sw = (request.json['sw'])
    stat = (request.json['data'])
    if(sw==1):
        acno = "AC1"
    elif(sw==2):
        acno = "AC2"
    elif(sw==3):
        acno = "AC3"
    elif(sw==4):
        acno = "AC4"
    else:
        acno = "as"
    admin = acstatus.query.filter_by(ac=acno).first()
    admin.status = stat
    db.session.commit()
    now = datetime.now()
    nowdate = now.strftime("%b %d, %Y")
    nowtime = now.strftime("%I:%M:%S %p")
    if(admin.id == 1):
        try:
            
            name = (request.json['name'])
            t = motordata(date =nowdate, time = nowtime ,status=admin.status , onby =name)
            db.session.add(t)
            db.session.commit()    
            # print("name")
            # print(name)
        except:
            t = motordata(date =nowdate, time = nowtime ,status=admin.status , onby ="Error")
            db.session.add(t)
            db.session.commit()
    
    # t = acstatus(ac = sw ,status=stat)
    # db.session.add(t)
    # db.session.commit()
    # ##print(sw,asog)
    # a = dbms.query.get(switch)
    # a = db.session.query(dbms.switch).all()
    # a = dbms.query.order_by(dbms.data).all()
    # stmt = dbms.query.all()
    # a = dbms.query.with_entities(dbms.switch)
    # b = len(a)-1
    # #print(a[b][0])
    # data = {
    #         "Modules" : 15,
    #         "Subject" : "Data Structures and Algorithms",
    #     }
    # admin = acstatus.query.filter_by(ac='22').first()
    # admin.ac = "AC1"
    # admin.status = 'off'
    # db.session.commit()
    # admin = acstatus.query.filter_by(ac='23').first()
    # admin.ac = "AC2"
    # admin.status = 'off'
    # db.session.commit()    
    # admin = acstatus.query.filter_by(ac='18').first()
    # admin.ac = "AC3"
    # admin.status = 'off'
    # db.session.commit()
    
    # admin = acstatus.query.filter_by(ac='19').first()
    # admin.ac = "AC4"
    # admin.status = 'off'
    # db.session.commit()
    a = db.session.query(alaram.shour).all()
    ##print(a)
    # return json
    return "ok"

@app.route('/update', methods=['POST'])
def update():
    roomno = (request.json['rno']) 
    humi = (request.json['humi'])
    te = (request.json['temp'])
    t = dbms(rid = roomno , humidity = humi ,temp=te)
    db.session.add(t)
    db.session.commit()
    return "Updateed"

@app.route('/temp', methods=['POST'])
def temp():
    try:
        shour = db.session.query(alaram.shour).first()
        smin = db.session.query(alaram.smin).first()
        szone = db.session.query(alaram.szone).first()
        ehour = db.session.query(alaram.ehour).first()
        emin = db.session.query(alaram.emin).first()
        ezone = db.session.query(alaram.ezone).first()
        admin = acstatus.query.filter_by(id=3).first()
        if(int(admin.status) == 0 ):
            b = "Alarm is off and motor1 start at " + str(shour[0]) + ":" + str(smin[0]) + " " + str(szone[0]) + " and turn off at "+ str(ehour[0]) + ":" + str(emin[0]) + " " + str(ezone[0]  )   
        else:
            b = "Alarm is set motor1 start at " + str(shour[0]) + ":" + str(smin[0]) + " " + str(szone[0]) + " and turn off at "+ str(ehour[0]) + ":" + str(emin[0]) + " " + str(ezone[0]  )   
    except:
        # pass
        b = "emty"
    return b

@app.route('/temp1', methods=['POST'])
def temp1():
    try:
        shour = db.session.query(alaram.shour).all()
        smin = db.session.query(alaram.smin).all()
        szone = db.session.query(alaram.szone).all()
        ehour = db.session.query(alaram.ehour).all()
        emin = db.session.query(alaram.emin).all()
        ezone = db.session.query(alaram.ezone).all()
        admin = acstatus.query.filter_by(id=4).first()
        if(int(admin.status) == 0 ):
            b = "Alarm is off and motor2 start at " + str(shour[1][0]) + ":" + str(smin[1][0]) + " " + str(szone[1][0]) + " and turn off at "+ str(ehour[1][0]) + ":" + str(emin[1][0]) + " " + str(ezone[1][0]  )   
        else:
            b = "alaram is set motor2 start at " + str(shour[1][0]) + ":" + str(smin[1][0]) + " " + str(szone[1][0]) + " and turn off at "+ str(ehour[1][0]) + ":" + str(emin[1][0]) + " " + str(ezone[1][0]  )   
    except:
        # pass
        b = "emty"
    return b


@app.route('/espupdate', methods=['GET','POST'])
def espupdate():
    try:
        a = request.args.get('a')
        b = request.args.get('b')
        c = request.args.get('c')
        t = dbms(rid = a , humidity = b ,temp=c)
        # db.session.add(t)
        # db.session.commit()
        return str(a)+str(b)
    except:
        return "pass"

@app.route('/espac', methods=['GET','POST'])
def espac():
    try:
        # esp = request.args.get('esp')
        # motor = request.args.get('motor')
        # admin = acstatus.query.filter_by(id=1).first()
        # admin.status = 
        # db.session.commit()
        db.session.query(dbms).delete()
        db.session.commit()
        now = datetime.now()
        nowdate = now.strftime("%b %d, %Y")
        nowtime = now.strftime("%I:%M:%S %p")
        t = dbms(rid = nowdate , humidity = nowtime , temp = "ping") 
        db.session.add(t)
        db.session.commit()
        shour = int(db.session.query(alaram.shour).first())
        smin = int(db.session.query(alaram.smin).first())
        szone = db.session.query(alaram.szone).first()
        ehour = int(db.session.query(alaram.ehour).first())
        emin = int(db.session.query(alaram.emin).first())
        ezone = db.session.query(alaram.ezone).first()
        nowhour = int(now.strftime("%I"))
        nowmin = int(now.strftime("%M"))
        nowzone = now.strftime("%p")
        a = db.session.query(acstatus.status).all()
        b = a[0][0]
        c = a[1][0]
        d = a[2][0]
        e = a[3][0]
        # if(d==1):
        #     if(nowhour > shour and nowhour < ehour and nowmin> emin):
        #         if(smin==nowmin):
        #             if(str(szone)==str(szone)):
        #                 d = 1
        #             else:
        #                 d = 0
        #         else:
        #             d = 0
        #     else:
        #         d = 0
        # elif:
        #     d = 0           
    except:
        b = 5
        c = 5
        d = 5
        e = 5
    return str(b) + str(c)+ str(d)+ str(e) 

@app.route('/sched', methods=['GET','POST'])
def sched():
    try:
        # #print("comi")
        smotor = int(request.json['motor'])
        admin = alaram.query.filter_by(id=smotor).first()
        admin.shour = (request.json['shour'])
        admin.smin = (request.json['smin'])
        admin.szone = (request.json['szone'])
        admin.ehour = (request.json['ehour'])
        admin.emin = (request.json['emin'])
        admin.ezone = (request.json['ezone'])
        db.session.commit()
    except:
        # #print("pass")
        pass
    return "ok"

@app.route('/swpos', methods=['GET','POST'])
def swpos():
    data = db.session.query(acstatus.status).all()
    data = db.session.query(acstatus.status).all()
    ##print(str(data[0][0]) + str(data[1][0]))
    return str(data[0][0]) + str(data[1][0])


@app.route('/online', methods=['GET','POST'])
def online():
    try:
        data = db.session.query(dbms.humidity).all()
        lhour = int(data[0][0][0:2])
        lmin = int(data[0][0][3:5])
        now = datetime.now()
        # nowdate = now.strftime("%b %d, %Y")
        nowhour = int(now.strftime("%I"))
        nowmin = int(now.strftime("%M"))
        if(nowhour == lhour):
            if(nowmin-lmin < 2 ):
                return "online"
            else:
                return "ofline"
        else:
            return "offline"        
    except:
        return "data is not come"
    


if __name__ == '__main__':
    # with app.app_context():
        # db.create_all()
    # db.switch.drop()
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port=82)
        
