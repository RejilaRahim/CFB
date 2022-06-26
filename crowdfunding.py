import datetime
import random

from flask import Flask, request, render_template, redirect, session
from  DBConnection import Db

app = Flask(__name__)
app.secret_key = "abc"


import json
from web3 import Web3, HTTPProvider

# truffle development blockchain address
blockchain_address = 'http://127.0.0.1:8545'
# Client instance to interact with the blockchain
web3 = Web3(HTTPProvider(blockchain_address))
# Set the default account (so we don't need to set the "from" for every transaction call)
web3.eth.defaultAccount = web3.eth.accounts[0]

compiled_contract_path = 'C:/Users/rejil/PycharmProjects/crowdfunig/node_modules/.bin/build/contracts/cf.json'
# Deployed contract address (see `migrate` command output: `contract address`)
deployed_contract_address = '0x1387bB00b5744C923feCE116c2F239D61adF9357'


@app.route('/')
def home():
    return render_template("cfbindex.html")

@app.route('/login',methods=['get','post'])
def login():
    db = Db()
    if request.method == "POST":
        username = request.form['t1']
        password = request.form['t2']
        res = db.selectOne("select * from Login where user_name = '"+username+"' and password = '"+password+"'")
        if res is not None:
            session['log'] = "log"
            if res['user_type'] == "admin":
                return redirect('/admin_home')
            elif res['user_type'] == "user":
                session['lid'] = res['login_ID']
                return redirect('/User_home')
            else:
                return '''<script>alert("User doesn't exist" );window.location="/"</script>'''

        else:
            return '''<script>alert("User doesn't exist" );window.location="/"</script>'''
    else:
        return render_template("Login.html")

@app.route('/admin_home')
def admin_home():
    if session['log']=="log":
     return render_template("admin/Ad_home.html")
    else:
        return redirect('/')

@app.route('/User_home')
def user_home():
    if session['log'] == "log":
     return render_template("user/User_home.html")
    else:
        return redirect('/')

@app.route('/view_user')
def View_user():
    if session['log'] == "log":
        db = Db()
        res = db.select("select * from user")
        return render_template("admin/View_User.html",data=res)
    else:
        return redirect('/')

@app.route('/view_don')
def View_don():
    if session['log'] == "log":
        with open(compiled_contract_path) as file:
            contract_json = json.load(file)  # load contract info as JSON
            contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

        contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
        blocknumber = web3.eth.get_block_number()
        res=[]
        for i in range(blocknumber,0,-1):
            a=web3.eth.get_transaction_by_block(i,0)
            r=contract.decode_function_input(a['input'])
            res1={}
            res1['bid']=r[1]['bid']
            res1['uid']=r[1]['uid']
            res1['d']=r[1]['d']
            res1['da']=r[1]['da']
            print(r[1]['bid'])
            db=Db()
            q=db.selectOne("select * from donation_request where req_id ='"+str(r[1]['bid'])+"'")
            if q is not None:
                 res1['donation']=q['donation']
            else:
                res1['donation']='Removed'
            q1=db.selectOne("select * from user WHERE user_ID='"+str(res1['uid'])+"'")
            if q1 is not  None :
                res1['uname']=q1['username']
            else:
                res1['uname']="Removed"

            res.append(res1)
        return render_template("admin/View_user_don.html",data=res)
    else:
        return redirect('/')

@app.route('/view_donr/<ik>')
def view_donr(ik):
    if session['log'] == "log":
        with open(compiled_contract_path) as file:
            contract_json = json.load(file)  # load contract info as JSON
            contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

        contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
        blocknumber = web3.eth.get_block_number()
        res=[]
        for i in range(blocknumber,0,-1):
            a=web3.eth.get_transaction_by_block(i,0)
            r=contract.decode_function_input(a['input'])
            res1={}
            print(str(ik),"oooooooo",str(r[1]['bid']))
            if str(ik)==str(r[1]['bid']):
                res1['bid']=r[1]['bid']
                res1['uid']=r[1]['uid']
                res1['d']=r[1]['d']
                res1['da']=r[1]['da']
                print(r[1]['bid'])
                db=Db()
                q=db.selectOne("select * from donation_request where req_id ='"+str(r[1]['bid'])+"'")
                if q is not None:
                     res1['donation']=q['donation']
                else:
                    res1['donation']='Removed'
                q1=db.selectOne("select * from user WHERE user_ID='"+str(res1['uid'])+"'")
                if q1 is not  None :
                    res1['uname']=q1['username']
                else:
                    res1['uname']="Removed"

                res.append(res1)
        return render_template("admin/View_user_don.html",data=res)
    else:
        return redirect('/')

@app.route('/view_complaint')
def View_complaint():
    if session['log'] == "log":
        db = Db()
        res = db.select("select * from complaint,user where complaint.user_ID=user.user_ID and complaint.reply='pending'")
        return render_template("admin/View_complaint.html",data=res)
    else:
        return redirect('/')

@app.route('/send_reply/<cid>',methods=['get','post'])
def send_reply(cid):
    if session['log'] == "log":
        db = Db()
        if request.method == "POST":
            reply = request.form['textarea']
            db.update("update complaint set reply='"+reply+"', r_date=curdate() where complaint_ID='"+cid+"'")
            return '''<script>alert("Replied Succesfully" );window.location="/view_complaint"</script>'''
        else:
            return render_template("admin/Complaint.html")
    else:
        return redirect('/')


@app.route('/add_donation',methods=['get','post'])
def add_donation():
    if session['log'] == "log":
        db = Db()
        if request.method == "POST":
            donation = request.form['textarea']
            db.insert("insert into donation_request VALUES ('','"+donation+"',curdate(),'pending','"+request.form['a']+"')")
            return '''<script>alert("Successfully Added");window.location="/add_donation"</script>'''
        else:
            return render_template("admin/Don_req.html")
    else:
        return redirect('/')

@app.route('/view_don_req')
def view_don_req():
    if session['log'] == "log":
        db = Db()
        res = []
        r=db.select("select * from donation_request")
        for ik in r:
            # print(ik)
            with open(compiled_contract_path) as file:
                contract_json = json.load(file)  # load contract info as JSON
                contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
            contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
            blocknumber = web3.eth.get_block_number()
            sum=0
            for i in range(blocknumber, 0, -1):
                a = web3.eth.get_transaction_by_block(i, 0)
                r = contract.decode_function_input(a['input'])
                res1 = {}
                res1['bid'] = r[1]['bid']
                res1['uid'] = r[1]['uid']
                res1['d'] = r[1]['d']
                res1['da'] = r[1]['da']
                if str(ik['req_ID'])==str(r[1]['bid']):
                    sum+=int(r[1]['d'])
                else:
                    sum=sum

                # db = Db()
                res1['donation']=ik['donation']
                res1['amount']=ik['amount']
                res1['date']=ik['date']
                res1['s']=sum
                print(sum)
                res1['status']=ik['status']
                res1['req_ID']=ik['req_ID']
            res.append(res1)
            sum=0

        return render_template("admin/View_don_req.html",data=res)
    else:
        return redirect('/')

@app.route('/updatedonation/<i>')
def updatedonation(i):
    if session['log'] == "log":
        db = Db()
        res = db.update("update donation_request set status='Closed' where req_ID='"+i+"'")
        return redirect('/view_don_req')
    else:
        return redirect('/')

@app.route('/change_pass',methods=['get','post'])
def change_password():
    if session['log'] == "log":
        db = Db()
        if request.method == "POST":
            password = request.form['textfield']
            pass1 = request.form['textfield2']
            pass2 = request.form['textfield3']
            res = db.selectOne("select * from login where password = '"+password+"'")
            if res is not None:
                if pass1 == pass2 :
                    db.update("update login set password='"+pass2+"'where password = '"+password+"'")
                    return'''<script>alert("Password Changed Successfully");window.location ="/"</script>'''
                else :
                    return '''<script>alert("Password doesn't match");window.location ="/change_pass"</script>'''

            else :
                return '''<script>alert("Incorrect Password");window.location ="/change_pass"</script>'''
        return render_template("admin/Change_pass.html")
    else:
        return redirect('/')

@app.route('/registration',methods=['get','post'])
def registration():
    db = Db()
    if request.method == "POST":
        username = request.form['textfield']
        dob = request.form['textfield2']
        place = request.form['textfield3']
        post = request.form['textfield4']
        pin = request.form['textfield5']
        email = request.form['textfield6']
        phone = request.form['textfield7']
        image = request.files['fileField']
        date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
        image.save(r"C:\\Users\\rejil\\PycharmProjects\\crowdfunig\\static\\Image\\"+date+".jpg")
        path = ("/static/Image/"+date+".jpg")
        password = request.form['textfield8']
        cpass = request.form['textfield9']
        result=db.selectOne("select * from login where user_name='"+email+"' ")
        if result is not  None:
            return '''<script>alert("User already exists");window.location ="/"</script>'''
        else:
            if password==cpass:
                res = db.insert("insert into login VALUES ('','"+email+"','"+str(cpass)+"','user')")
                db.insert("insert into `user` VALUES ('"+str(res)+"','"+username+"','"+dob+"','"+place+"','"+post+"','"+pin+"','"+email+"','"+phone+"','"+str(path)+"')")
                return '''<script>alert("User Registered Successfully");window.location ="/"</script>'''
            else :
                return '''<script>alert("Password Mismatch");window.location ="/registration"</script>'''
    else:
        return render_template("user/User_reg.html")

@app.route('/complaint',methods=['get','post'])
def complaint():
    if session['log'] == "log":
       db = Db()
       if request.method == "POST":
           complaint = request.form['textarea']
           db.insert("insert into complaint VALUES ('','"+complaint+"','pending',curdate(),'pending' ,'"+str(session['lid'])+"')")
           return '''<script>alert("Complaint Sent Succesfully" );window.location="/complaint"</script>'''
       else:
           return render_template("user/Complaint.html")
    else:
        return redirect('/')

@app.route('/viewcomplaint')
def view_complaint():
    if session['log'] == "log":
        db = Db()
        res = db.select("select * from complaint WHERE  user_ID = '"+str(session['lid'])+"'")
        return render_template("user/view_complaint.html",data=res)
    else:
        return redirect('/')

# @app.route('/donation_add',methods=['post','get'])
# def donation_add():
#     if request.method=='POST':
#         n1=request.form['n1']
#         n2=request.form['n2']
#         n3=request.form['n3']
#         n4=request.form['n4']
#         n5=request.form['n5']
#
#         with open(compiled_contract_path) as file:
#             contract_json = json.load(file)  # load contract info as JSON
#             contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
#
#         contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
#         blocknumber = web3.eth.get_block_number()
#
#         message2 = contract.functions.addEmployee(blocknumber + 1,n1,n2,n3,n4,n5,(session['lid'])).transact()
#     else:
#         return render_template("user/product_add.html")
@app.route('/view_pre_don')
def view_pre_don():
    if session['log'] == "log":
        with open(compiled_contract_path) as file:
            contract_json = json.load(file)  # load contract info as JSON
            contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

        contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
        blocknumber = web3.eth.get_block_number()
        res=[]
        for i in range(blocknumber,0,-1):
            a=web3.eth.get_transaction_by_block(i,0)
            r=contract.decode_function_input(a['input'])
            res1={}
            res1['bid']=r[1]['bid']
            res1['uid']=r[1]['uid']
            res1['d']=r[1]['d']
            res1['da']=r[1]['da']
            print(r[1]['bid'])
            db=Db()
            q=db.selectOne("select * from donation_request where req_id ='"+str(r[1]['bid'])+"'")
            if q is not None:
                 res1['donation']=q['donation']
            else:
                res1['donation']='Removed'
            if session['lid']==r[1]['uid']:
                res.append(res1)
        return render_template("user/View_pre_don.html",data = res)
    else:
        return redirect('/')

@app.route('/view_don_req1')
def view_don_req1():
    if session['log'] == "log":
        db = Db()
        res = db.select("select * from donation_request")
        return render_template("user/View_don_req.html",data=res)
    else:
        return redirect('/')

@app.route('/bank_details',methods=['get','post'])
def bank_details():
    if session['log'] == "log":
       if request.method=='POST':
            accno=request.form['textfield2']
            bank=request.form['select']
            ifsc=request.form['text']
            cvv=request.form['textfield3']
            db=Db()
            q=db.selectOne("select * from bank where accnumber='"+accno+"' and ifsc='"+ifsc+"'")
            if q is None:
                db.insert("insert into bank VALUES ('','"+accno+"','"+cvv+"','"+str(random.randint(0000,9999))+"','"+str(session['lid'])+"','"+bank+"','"+ifsc+"')")
                return '''<script>alert("Insert Succesfully" );window.location="/bank_details"</script>'''
            else :
                return '''<script>alert("Account already exists" );window.location="/bank_details"</script>'''
       else :
           return render_template('user/Bank_details.html')
    else:
        return redirect('/')

@app.route('/view_bank')
def view_bank():
    if session['log'] == "log":
        db = Db()
        res= db.select("select * from bank WHERE  userid='" + str(session['lid']) + "'")
        return render_template("user/View_bank.html", data=res)
    else:
        return redirect('/')

@app.route('/send_donation/<il>/<amnt1>',methods=['get','post'])
def donation(il,amnt1):
    if session['log'] == "log":
        print(il,amnt1)
        if request.method=='POST':
            acc=request.form["textfield"]
            cvv=request.form["textfield2"]
            amnt=request.form["textfield3"]
            print("giiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii",session['bamnt'],(int(session['bamnt'])+int(amnt)))
            if (int(amnt)) <= int(session['bamnt']):
                db=Db()
                res= db.selectOne("select * from bank where accnumber='"+acc+"' and  cvv='"+cvv+"' and userid='"+str(session['lid'])+"'")
                if res is not None:
                    if int(amnt)<=int(res['amount']):
                        with open(compiled_contract_path) as file:
                                    contract_json = json.load(file)  # load contract info as JSON
                                    contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
                        contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
                        blocknumber = web3.eth.get_block_number()
                        d=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        message2 = contract.functions.addUser(int(il),session['lid'],amnt,d).transact()
                        return '''<script>alert("Donation Added Successfully");window.location="/send_donation/'''+il+'''/'''+amnt1+'''"</script>'''
                    else:
                        return '''<script>alert("Insufficient Balance");window.location="/send_donation/'''+il+'''/'''+amnt1+'''"</script>'''
                else:
                    return '''<script>alert("Account not found" );window.location="/send_donation/'''+il+'''/'''+amnt1+'''"</script>'''
            else:
                return '''<script>alert("Amount exceeds!!!!" );window.location="/view_don_req1"</script>'''

        with open(compiled_contract_path) as file:
            contract_json = json.load(file)  # load contract info as JSON
            contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
        contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
        blocknumber = web3.eth.get_block_number()
        sum = 0
        print("jiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
        for i in range(blocknumber, 0, -1):
            print("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
            a = web3.eth.get_transaction_by_block(i, 0)
            r = contract.decode_function_input(a['input'])
            res1 = {}
            res1['bid'] = r[1]['bid']
            res1['uid'] = r[1]['uid']
            res1['d'] = r[1]['d']
            res1['da'] = r[1]['da']
            if str(il) == str(r[1]['bid']):
                sum += int(r[1]['d'])
            else:
                sum = sum
        if int(amnt1)==sum:
            return '''<script>alert("Account closed !!!!" );window.location="/view_don_req1"</script>'''
        else:
            t=int(amnt1)-sum
            session['bamnt']=t
        return render_template("user/Add_donation.html",data=t)
    else:
        return redirect('/')


@app.route('/logout')
def logout():
    session['log']=""
    return redirect('/')


if __name__ == '__main__':
    app.run(port=3000,debug=True)
