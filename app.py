from itertools import count
from logging import fatal
import re
from flask import Flask,render_template,request,session,redirect,url_for,flash
from MySQLdb import connections

from flask_mysqldb import MySQL
import datetime


app = Flask(__name__)
import json
jsonfiles = open('static\jsonfile.json','r')
data = jsonfiles.read()
load = json.loads(data)

app.config['SECRET_KEY']='secretkey'
app.config['MYSQL_HOST']='localhost'
app.config["MYSQL_USER"]='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='online_election'

db = MySQL(app)

now = datetime.datetime.now().date()
nowtime=datetime.datetime.now().time()

variable=False

@app.route('/',methods=['POST','GET'])
def home():
    var=True
    cur = db.connection.cursor()
    cur.execute('SELECT * FROM release_election')
    fetchdata = cur.fetchall()
    count=cur.rowcount
    cur.close()
    if count>0:
        if now < fetchdata[0][3]:
            return render_template("timeline.html",data=fetchdata)
        elif(now > fetchdata[0][3] and now < fetchdata[0][4]):
            list=db.connection.cursor()
            list.execute('SELECT * FROM shortlist_candidate')
            retrieve=list.fetchall()
            list.close()
            return render_template('showCandidates.html' ,data=retrieve)
        elif(now == fetchdata[0][4]):
            list=db.connection.cursor()
            list.execute('SELECT * FROM shortlist_candidate')
            retrieve=list.fetchall()
            list.close()
            return render_template('castVote.html', data=retrieve)
        else:
            bool=False
            rslt1=db.connection.cursor()
            rslt1.execute('SELECT ID,Fname,Lname,Email,VoteCount FROM shortlist_candidate')
            rsltdata1=rslt1.fetchall()
            rslt1.close()
            rslt2=db.connection.cursor()
            rslt2.execute('SELECT Max(VoteCount) FROM shortlist_candidate')
            rsltdata2=rslt2.fetchall()
            rslt2.close()
            max=rsltdata2[0][0]
            rslt2=db.connection.cursor()
            if max!=None:
                rslt2.execute("SELECT ID,Fname, Lname, Email,VoteCount FROM shortlist_candidate WHERE VoteCount ='%d'"%(max))
                rsltdata2=rslt2.fetchall()
                rslt2.close()
        
            if now>=fetchdata[0][7]:
                bool=True
            return render_template('result.html',data1=rsltdata1,data2=rsltdata2,bool=bool) 
    else:
        var=False
        return render_template("noelection.html")          

@app.route('/dashboard', methods=['GET','POST'])
def Dashboard():

    if ('user' in session and session['user'] == load['Admin_username']):
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM release_election')
        fetchdata = cur.fetchall()
        count2=cur.rowcount
        cur.close()
        return render_template ("admin.html",data=fetchdata)
    else:    
        if request.method=='POST':
            Username = request.form.get('username')
            Password = request.form.get('password')
        
            if (Username == load['Admin_username'] and Password == load['Admin_password']):
                session['user'] = Username
                cur = db.connection.cursor()
                cur.execute('SELECT * FROM release_election')
                fetchdata = cur.fetchall()
                cur.close()
                return render_template ('admin.html',data=fetchdata)
            else:
                flash('Invalid username or password')
                return render_template('adminLogin.html')
        return render_template('adminLogin.html')


@app.route('/logout')
def Logout():
    if 'user' in session:
        session.pop('user',None)
        flash('Admin Logged Out successfully')
        return redirect('/dashboard')
    else:
        return('First Login to Logout session')

@app.route('/logout1')
def Logout1():
    if 'user1' in session:
        session.pop('user1',None)
        return redirect('/clogin')
    else:
        return('you have already logged out')

@app.route('/logout2')
def Logout2():
    if 'user3' in session:
        session.pop('user3',None)
        return redirect('/vlogin')
    else:
        return('You have already logged out')

@app.route('/release', methods=['GET','POST'])
def Adde():
    if 'user' in session:
        add=db.connection.cursor()
        add.execute('SELECT EID FROM release_election')
        count = add.rowcount

        if count>0:
            bool=False
            return render_template('addElection.html',bool=bool)

        else :
            bool=True
            if request.method=='POST':
                etitle = request.form['ename']
                rstart = request.form['sdate']
                rend = request.form['edate']
                vcast = request.form['vcasting']
                vstart = request.form['vstart']
                vend = request.form['vend']
                rdeclare = request.form['rdate']
    
                cur = db.connection.cursor()
                cur.execute("INSERT INTO release_election(ETitle,Cstart,Cend,Vdate,Vstart,Vend,Rdeclare) VALUES (%s,%s,%s,%s,%s,%s,%s)",(etitle,rstart,rend,vcast,vstart,vend,rdeclare))
                db.connection.commit()
                flash('Election Released successfully')
            return render_template('addElection.html' , bool=bool)
    else:
        return("Unauthorised access")

@app.route('/Candidates')
def Registrations():
    if 'user' in session:
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM candidate_registration')
        fetchdata = cur.fetchall()
        cur.close()
        return render_template("verifyCandidate.html" ,data=fetchdata)
    else:
        return('Unauthorized access')
    
@app.route('/Voters')
def vRegistrations():
    if 'user' in session:
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM voter_registration')
        fetchdata = cur.fetchall()
        cur.close()
        return render_template("verifyVoters.html" ,data=fetchdata)
    else:
        return('Unauthorized access')
    
@app.route('/cregister' ,methods=['GET','POST'])
def Cregister():
    curl = db.connection.cursor()
    curl.execute('SELECT Cstart,Cend FROM release_election')
    fetchdate = curl.fetchall()
    count1=curl.rowcount
    curl.close()
    
    if count1==1:
        bool=False
        if now > fetchdate[0][0] and now < fetchdate[0][1]:
            bool=True
        if request.method=='POST':
            Email=request.form['email']
            exist=db.connection.cursor()
            exist.execute('SELECT * FROM candidate_registration WHERE Email=%s',(Email,))
            count=exist.rowcount
            exist.close()
            if count==0:
                Cfname=request.form['fname']
                Clname=request.form['lname']
                Dob=request.form['dob']
                Mobile=request.form['phone']
                Gender=request.form['gender']
                Password=request.form['password']
                #Esymbol=request.files['logo']
                Intro = request.form['intro']
        
                cur = db.connection.cursor()
                cur.execute('INSERT INTO candidate_registration(Fname,Lname,Dob,Mobile_NO,Gender,Email,Password,Introduction) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)' ,(Cfname,Clname,Dob,Mobile,Gender,Email,Password,Intro))
                cur.execute('INSERT INTO shortlist_candidate(Fname,Lname,Dob,Email,Gender) VALUES(%s,%s,%s,%s,%s)',(Cfname,Clname,Dob,Email,Gender))
                db.connection.commit()
                flash('Registered successfully')
                return redirect("/cregister")
            else:
                return("Candidate with email "+Email+" already registered")
        return render_template('cregistration.html',bool=bool)
    else:
        return render_template('cregistration.html',data=fetchdate)

@app.route('/vregister' ,methods=['GET','POST'])
def Vregister():
    curl = db.connection.cursor()
    curl.execute('SELECT Cstart,Cend FROM release_election')
    fetchdata = curl.fetchall()
    count1=curl.rowcount
    curl.close()
    if count1==1:
        if request.method=='POST':
            Email=request.form['email']
            exist=db.connection.cursor()
            exist.execute('SELECT * FROM voter_registration WHERE Email=%s',(Email,))
            count=exist.rowcount
            exist.close()
            if count==0:
                Vfname=request.form['Fname']
                Vlname=request.form['Lname']
                Dob=request.form['dob']
                Mobile=request.form['phone']
                Gender=request.form['gender']
                Password=request.form['password']
        
                cur = db.connection.cursor()
                cur.execute('INSERT INTO voter_registration(Fname,Lname,Dob,Mobile_NO,Gender,Email,Password) VALUES(%s,%s,%s,%s,%s,%s,%s)' ,(Vfname,Vlname,Dob,Mobile,Gender,Email,Password))
                cur.execute('INSERT INTO due_voters(fname,lname,Email) VALUES (%s,%s,%s)',(Vfname,Vlname,Email))
                db.connection.commit()
                flash('Registered Successfully')
                return redirect("/vregister")
            else:
                return("Voter with email "+Email+" already registered")
        return render_template('vregistration.html')
    else:
        return render_template("vregistration.html",data=fetchdata)

@app.route('/clogin',methods=['GET','POST'])
def Clogin():
    if request.method=='POST':
        clogin=request.form
        email=clogin['email']
        password=clogin['password']
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM candidate_registration WHERE Email=%s AND Password=%s',(email,password))
        fetchdata = cur.fetchall()
        count=cur.rowcount
        cur.close()
        if count==1:
            session['user1'] = email
            return render_template('candidateProfile.html',data=fetchdata)
        else:
            flash("Invalid Email or Password")
            return render_template('clogin.html')

    return render_template('clogin.html')

@app.route('/vlogin',methods=['GET','POST'])
def Vlogin():
    if request.method=='POST':
        clogin=request.form
        email=clogin['email']
        password=clogin['password']
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM voter_registration WHERE Email=%s AND Password=%s',(email,password))
        fetchdata = cur.fetchall()
        count=cur.rowcount
    
        if count==1:
            session['user3'] = email
            return render_template('voterProfile.html',data=fetchdata)
        else:
            flash("Invalid Email or Password")
            return render_template('vlogin.html')
    return render_template('vlogin.html')  

@app.route('/castvote',methods=['GET','POST'])
def Cast():
    cur = db.connection.cursor()
    cur.execute('SELECT * FROM shortlist_candidate')
    fetchdata = cur.fetchall()
    cur.close()
    return render_template("castVote.html",data=fetchdata)  

@app.route('/voted/<int:id>',methods=['GET','POST'])
def Voted(id):
    if 'user3' in session:
        cur = db.connection.cursor()
        str=session['user3']
        cur.execute('SELECT * FROM due_voters WHERE Email=%s',(str,))
        fetchdata = cur.fetchall()
        count=cur.rowcount
        cur.execute('DELETE FROM due_voters WHERE Email=%s',(str,))
        cur.connection.commit()
        if count==1:
            vote = db.connection.cursor()
            vote.execute("SELECT VoteCount FROM shortlist_candidate WHERE ID='%d'" % id)
            votes=vote.fetchall()
            vote.execute("""UPDATE shortlist_candidate SET VoteCount=%s WHERE ID=%s""",(votes[0][0]+1,id)) 
            db.connection.commit()
            flash("Voted")
            return redirect("/")
            
        else:
            flash("you have already voted")
            return redirect("/")
    else:
        flash("Login in to caste your vote")
        return redirect('/vlogin')
    return redirect("/castvote")

@app.route('/reject/<int:id>')
def Reject(id):
    print(id);
    cur = db.connection.cursor()
    cur.execute("""UPDATE candidate_registration SET Status=%s WHERE ID=%s""",('Rejected',id))
    cur.execute("DELETE FROM shortlist_candidate WHERE ID = '%d'" % (id))
    cur.close()
    db.connection.commit()
    return redirect("/Candidates")
@app.route('/approve/<int:id>')
def Approve(id):
    print(id);
    cur = db.connection.cursor()
    cur.execute("""UPDATE candidate_registration SET Status=%s WHERE ID=%s""",('Approved',id))
    cur.close()
    db.connection.commit()
    return redirect("/Candidates")
@app.route('/result')
def Result():
    if 'user' in session:
        curl = db.connection.cursor()
        curl.execute('SELECT Cstart,Cend FROM release_election')
        fetchdata = curl.fetchall()
        curl.close()
        if fetchdata!=():
            rslt1=db.connection.cursor()
            rslt1.execute('SELECT ID,Fname,Lname,Email,VoteCount FROM shortlist_candidate')
            rsltdata1=rslt1.fetchall()
            rslt1.close()
            rslt2=db.connection.cursor()
            rslt2.execute('SELECT Max(VoteCount) FROM shortlist_candidate')
            rsltdata2=rslt2.fetchall()
            count=rslt2.rowcount
            rslt2.close()
            max=rsltdata2[0][0]
            print(max)
            if  max!=None:
                rslt2=db.connection.cursor()
                rslt2.execute("SELECT ID,Fname, Lname, Email,VoteCount FROM shortlist_candidate WHERE VoteCount ='%d'"%(max))
                rsltdata2=rslt2.fetchall()
                rslt2.close()
                return render_template('resultDeclare.html',data=rsltdata1,data1=rsltdata2,data2=fetchdata)
            else:
                return render_template('resultDeclare.html',data2=fetchdata) 
        else:
            return render_template('resultDeclare.html',data2=fetchdata)
    else:
        return("ACCESS DENIED FOR PROTECTED PAGE")
@app.route('/account')
def Account():
    if 'user1' in session:
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM candidate_registration WHERE Email=%s',(session['user1'],))
        fetchdata = cur.fetchall()
        cur.close()
        return render_template('candidate_profile.html',data=fetchdata)
    elif 'user3' in session:
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM voter_registration WHERE Email=%s',(session['user3'],))
        fetchdata = cur.fetchall()
        cur.close()
        return render_template("voter_profile.html",data=fetchdata)
    else:
        flash('Login to your voter account')
        return redirect('/vlogin')

@app.route('/close')
def Close():
    if 'user' in session:
        obj1=db.connection.cursor()
        obj1.execute('DELETE FROM voter_registration')
        obj1.close()

        obj2=db.connection.cursor()
        obj2.execute('DELETE FROM candidate_registration')
        obj2.close()

        obj3=db.connection.cursor()
        obj3.execute('DELETE FROM shortlist_candidate')
        obj3.close()

        obj2=db.connection.cursor()
        obj2.execute('DELETE FROM candidate_registration')
        obj2.close()

        obj2=db.connection.cursor()
        obj2.execute('DELETE FROM candidate_registration')
        obj2.close()

        obj4=db.connection.cursor()
        obj4.execute('DELETE FROM release_election')
        obj4.close()    
    

        db.connection.commit()
        flash('Election closed successfully')
        bool=True
        return render_template('addElection.html',bool=bool)
    else:
        return("Unathorized Access")   



app.run(debug=True)