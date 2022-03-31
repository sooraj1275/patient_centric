import csv
import os

from flask import Flask,render_template,request,redirect
from flask.globals import session
from  DBConnection import Db

app = Flask(__name__)
app.secret_key="kk"




# ...............................admin...........................................................................................

@app.route('/u_panel')
def u_panel():
    if session['lin'] == "lin":
        return render_template("user/home.html")
    else:
        return render_template("login.html")


@app.route('/')
def login():
    return render_template("login.html")

@app.route('/login_pst',methods=['POST'])
def login_pst():
    usernam=request.form["email"]
    passwor=request.form["pass"]
    db=Db()
    qry=db.selectOne("SELECT * FROM login WHERE username='"+usernam+"' AND password='"+passwor+"' ")
    if qry is not None:
        if qry["type"]=="admin":
            session['lin']="lin"
            return ''' <script> alert('login success');window.location="/adm_home"; </script> '''

        elif(qry["type"]=="user"):
            q=db.selectOne("SELECT * FROM user WHERE user.login_id='"+str(qry["login_id"])+"'")
            if q is not None:
                session["userid"]=qry["login_id"]
                session['lin'] = "lin"
                return ''' <script>alert('login success');window.location="/u_panel"; </script> '''
            else:
                return ''' <script>alert('Invalid Username or Password');window.location="/"; </script> '''
    else:
        return ''' <script>alert('Invalid Username or Password');window.location="/"; </script> '''

@app.route('/adm_home')
def adm_home():
    if session['lin'] == "lin":
        return render_template("admin/AdminHome.html")
    else:
        return render_template("login.html")


@app.route('/adm_vcomt')
def adm_vcomt():
    if session['lin']=="lin":
        obj=Db()
        qry="select user.fname,user.email,complaint.* from user ,complaint where complaint.user_id=user.login_id"
        res=obj.select(qry)
        return render_template("admin/viewcomplaint.html",data=res)
    else:
        return render_template("login.html")






@app.route('/reply/<id>')
def reply(id):
    if session['lin'] == "lin":
        session['com']=id
        print(session)
        db = Db()
        qry="select * from complaint where c_id='"+id+"' "
        res=db.selectOne(qry)
        return render_template('admin/reply.html',data=res)
    else:
        return render_template("login.html")



@app.route('/adm_reply_post',methods=["post"])
def adm_reply_post():
    if session['lin'] == "lin":
        obj1=Db()
        reply=request.form['r']
        qry= "update complaint set reply='"+reply+"',reply_date=curdate(),status='replied' where c_id='"+str(session['com'])+"'"
        obj1.update(qry)
        return ''' <script> alert('replyed succesfully');window.location="/adm_vcomt"; </script> '''
    else:
        return render_template("login.html")






@app.route('/adm_vfbk')
def adm_vfbk():
    if session['lin'] == "lin":
        obj = Db()
        qry = "select user.fname,user.email,feedback.feedback,feedback.create_at from user,feedback where feedback.user_id=user.login_id"
        res = obj.select(qry)
        return render_template("admin/viewfeedbk.html",data=res)
    else:
        return render_template("login.html")







@app.route('/adm_vuser')
def adm_vuser():
    if session['lin'] == "lin":
        obj = Db()
        qry = "select * from user"
        res = obj.select(qry)
        return render_template("admin/viewuser.html", data=res)
    else:
        return render_template("login.html")

@app.route('/delt_user/<id>')
def delt_user(id):
    if session['lin'] == "lin":
        obj = Db()
        qry = "delete from user where user_id='" + id + "'"
        obj.delete(qry)
        return adm_vuser()
    else:
        return render_template("login.html")




@app.route('/adm_reply')
def adm_reply():
    if session['lin'] == "lin":
        return render_template("admin/reply.html")
    else:
        return render_template("login.html")


@app.route('/logout')
def logout():
    session['lin']="lout"
    return render_template("login.html")


# .................................user................................................................................................

@app.route('/userhome')
def userhome():
    return render_template("userhome.html")

#..........................................main......................................................................................






@app.route('/user_fbk')
def user_fbk():
    if session['lin'] == "lin":
        return render_template("user/feedback.html")
    else:
        return render_template("login.html")


@app.route('/user_fdbk_post',methods=["post"])
def user_fdbk_post():
    if session['lin'] == "lin":
        obj1=Db()
        feedback=request.form['fb']
        qry= "insert into feedback (f_id,user_id,feedback,create_at)values (null,'"+str( session["userid"])+"','"+feedback+"',curdate())"
        obj1.insert(qry)

        return ''' <script> alert('send succesfully');window.location="/u_panel"; </script> '''
    else:
        return render_template("login.html")




@app.route('/user_vcomt')
def user_vcomt():
    if session['lin'] == "lin":
        obj = Db()
        x=session['userid']
        qry = "select created_at,subject,complaint,reply,reply_date from complaint where user_id='"+str(x)+"'"
        res = obj.select(qry)
        return render_template("user/viewcmplt.html",data=res)
    else:
        return render_template("login.html")

@app.route('/user_cmpt')
def user_cmpt():
    if session['lin'] == "lin":
        return render_template("user/complaints.html")
    else:
        return render_template("login.html")


@app.route('/user_cmplt_post',methods=["post"])
def user_cmplt_post():
    if session['lin'] == "lin":
        obj1=Db()
        Subject=request.form['subject']
        complaint=request.form['cmp']
        qry= "insert into complaint(user_id,subject,complaint,created_at,status) values('"+str( session["userid"])+"','"+Subject+"','"+complaint+"',curdate(),'pending')"
        obj1.insert(qry)

        return ''' <script> alert('send succesfully');window.location="/u_panel"; </script> '''
    else:
        return render_template("login.html")







@app.route('/user_profile')
def user_profile():
    if session['lin'] == "lin":
        obj=Db()
        x=session['userid']
        qry="select fname,lname,gender,dob,email from user where login_id='"+str(x)+"' "
        res=obj.selectOne(qry)
        return render_template("user/profile.html",data=res)
    else:
        return render_template("login.html")




@app.route('/user_history')
def user_history():
    if session['lin'] == "lin":
        obj = Db()
        x = session['userid']
        qry = "select created_at,song_file,status,song_id from song where user_id='" + str(x) + "' "
        res = obj.select(qry)
        return render_template("user/history.html",data=res)
    else:
        return render_template("login.html")



@app.route('/d_history/<id>')
def d_history(id):
    if session['lin'] == "lin":
        obj1=Db()
        qry1="delete from song where song_id='"+id+"'"
        obj1.delete(qry1)
        return user_history()
    else:
        return render_template("login.html")


# .........................common............................................




@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/user_reg_post',methods=["post"])
def user_reg_post():
    print('KKKKKKKKKK')
    obj=Db()
    fname=request.form['firstname']
    lname=request.form['lastname']
    Gender=request.form['Gender']
    DOB=request.form['dob']
    Email=request.form['email']
    Password=request.form['paswd']
    confirmPassword=request.form['cpaswd']
    if confirmPassword==Password:
        qry1 = "insert into login(username,password,type)values('"+Email+"','"+confirmPassword+"','user')"
        res=obj.insert(qry1)
        qry2="insert into user(login_id,fname,lname,Gender,dob,email)values('"+str(res)+"','"+fname+"','"+lname+"','"+Gender+"','"+DOB+"','"+Email+"')"
        obj.insert(qry2)
        return ''' <script>alert('signup success');window.location="/"; </script> '''
    else:
        "error"
        return redirect('/')








@app.route('/cpswd')
def cpswd():
    if session['lin'] == "lin":
        return render_template("changepswd.html")
    else:
        return render_template("login.html")


@app.route('/pchange',methods=["post"])
def pchange():
    if session['lin'] == "lin":
        obj1=Db()
        crpswd=request.form['cpsw']
        newpswd=request.form['newpsw']
        cnfpswd = request.form['cpswd']

        if newpswd == cnfpswd:
            qry= "select password from login where login_id='"+str(session["userid"])+"'"
            res=obj1.selectOne(qry)
            if res is not None:
                if res['password']==crpswd:
                    q="update login set password='"+newpswd+"' where login_id='"+str( session["userid"])+"'"
                    obj1.update(q)
                    return userhome()
                else:
                    return '''<script>alert('incorrect current password');window.location='/cpswd';</script>'''
        else:
            return '''<script>alert(' passwords not matching ');window.location='/cpswd';</script>'''
    else:
        return render_template("login.html")


@app.route('/exsummarize')
def exsummarize():
    return render_template('/user/extractivesummarization.html')



@app.route('/extsummarizepost',methods=['post'])
def extsummarizepost():
    a=request.form["txt"]

    from sums import ext

    s=ext(a)

    return render_template('/user/extractivesummarization.html',p=s)

    
@app.route('/summarize')
def summarize():
    return render_template('/user/summarize.html')


@app.route('/summarizepost',methods=['POST'])
def summarizepost():
    a=request.form["txt"]
    import torch
    from models.model_builder import ExtSummarizer
    from ext_sum import summarize

    # Load model
    model_type = 'mobilebert' #@param ['bertbase', 'distilbert', 'mobilebert']
    checkpoint = torch.load(f'checkpoints/{model_type}_ext.pt', map_location='cpu')
    model = ExtSummarizer(checkpoint=checkpoint, bert_type=model_type, device='cpu')

    # Run summarization
    input_fp = a
    result_fp = r'D:\2020 2021\MesTextSummarisation\static\summary.txt'
    summary = summarize(input_fp, result_fp, model, max_length=3)
    print(summary)



    return render_template('/user/summarize.html',p=summary)


@app.route('/sa')
def sa():
    return render_template('sa.html')



if __name__ == '__main__':
    app.run(debug=True)
