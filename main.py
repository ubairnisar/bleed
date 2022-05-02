from flask import Flask , render_template , url_for , redirect , flash , request

from flask_sqlalchemy  import SQLAlchemy

from flask_login import UserMixin , login_user , LoginManager , login_required , logout_user , current_user
from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField , SelectField , IntegerField , EmailField
from wtforms.validators import InputRequired , Length , ValidationError , NumberRange ,EqualTo , Email
from datetime import datetime , date
from flask_migrate import Migrate
import sqlite3
from flask_mail import Mail , Message

check = 0

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'bleed'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'bleedthesmartway@gmail.com'
app.config['MAIL_PASSWORD'] = 'admin532'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
migrate = Migrate(app, db , render_as_batch=True)

login_manager =  LoginManager()
login_manager.init_app(app)
login_manager.login_view ="login"

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model , UserMixin ):
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(20) , nullable = False ,  unique = True)
    password = db.Column(db.String(80) , nullable = False)
    email = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer , nullable = False)
    cnic = db.Column(db.String(13) , nullable = False)
    secretof = db.Column(db.String(80) , nullable = False)
    bloodgroup = db.Column(db.String(4) , nullable = False)




class admin( db.Model  ):
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(20) , nullable = False ,  unique = True)
    password = db.Column(db.String(80) , nullable = False)


class donationcenters(db.Model):
    id = db.Column(db.Integer , primary_key = True , autoincrement=True)
    name = db.Column(db.String(30) , nullable = False)
    city = db.Column(db.String(20) , nullable = False )
    Address = db.Column(db.String(60) , nullable = False)

class receivers(db.Model):
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String(20))
    bloodgroup = db.Column(db.String(4) , nullable = False)
    hosname = db.Column(db.String(30) , nullable = False)
    city = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20))


class blooddonors(db.Model):
    id = db.Column(db.Integer, primary_key=True , autoincrement=True)
    username = db.Column(db.String(20) , nullable = False)
    token = db.Column(db.String , nullable = False)
    bloodgroup = db.Column(db.String(4) , nullable = False)
    time = db.Column(db.String(30) )
    date = db.Column(db.String(30))
    stat = db.Column(db.String(10))
    takenby = db.Column(db.String)
    donatedto = db.Column(db.Integer , db.ForeignKey('donationcenters.id'))
    donationcenters = db.relationship("donationcenters", backref=db.backref("donationcenters", uselist=False))


class RegisterForm(FlaskForm):
    username = StringField(validators= [InputRequired(message = "Input required") , Length(min  = 4 ,
                max = 20 , message = "range is (4 - 20)") ] , render_kw= {"placeholder" : "Username"})
    confirm = PasswordField(validators= [InputRequired() , Length(min  = 4 ,
                max = 20) ] ,render_kw= {"placeholder" : "Confirm Password"})
    password = PasswordField(validators= [InputRequired() , Length(min  = 4 ,
                max = 20) , EqualTo('confirm', message='Passwords must match')] ,render_kw= {"placeholder" : "Password"})
    secretof = StringField(validators= [InputRequired(message = "Input required") , Length(min  = 4 ,
                max = 20 , message = "range is (4 - 20)") ] , render_kw= {"placeholder" : "Enter something that you will always going to remember"})
    age = IntegerField(validators= [InputRequired(message = "Input required") , NumberRange(min = 18 , max = 65 , message = "You should be age between 18 to 65")] , render_kw= {"placeholder" : "Age"})
    email = EmailField(validators=[Email(message = "Input required")] , render_kw= {"placeholder" : "Email"})
    cnic = StringField(validators= [InputRequired(message = "Input required") , Length(min = 13 , max = 13 , message = "Invalid CNIC")] , render_kw= {"placeholder" : "CNIC"})
    bloodgroup =  SelectField('Blood Group' , choices =  [ 'A+' , 'A-' , 'B+' ,'B-' , 'AB+' ,'AB-', 'O+','O-'] )
    submit = SubmitField("Become Donor")

    def validate_userncnic(self , username , cnic):
        error =''
        existing_user_username =  User.query.filter_by(username= username.data).first()
        if existing_user_username:
            error = 'username already exist'
        existing_user_cnic = User.query.filter_by( cnic = cnic.data).first()
        if existing_user_cnic:
            error = 'cnic already exist'

        return error

class recverf(FlaskForm):
    token = StringField(validators= [InputRequired(message = "Input required")  ] , render_kw= {"placeholder" : "Receiver Token"})
    submit = SubmitField('Not able to receive blood')



class admincheck(FlaskForm):
    token = StringField(validators= [InputRequired(message = "Input required")] , render_kw= {"placeholder" : "Donor Token"})
    submit = SubmitField('Verify')
class donateform(FlaskForm):
    city = SelectField('City' , choices =  [ 'Islamabad' , 'Lahore' , 'Peshawar' ,'Karachi' ] )
    submit = SubmitField("Search")
class forgetform(FlaskForm):
    username = StringField(validators= [InputRequired(message = "Input required")  ] , render_kw= {"placeholder" : "Username"})
    sec = StringField(validators=[InputRequired(message="Input required")], render_kw={"placeholder": "Security key"})
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    username = StringField(validators= [InputRequired(message = "Input required")  ] , render_kw= {"placeholder" : "Username"})
    password = PasswordField(validators= [InputRequired(message = "Input required")] ,render_kw= {"placeholder" : "Password"})
    submit = SubmitField("Login")

class adminForm(FlaskForm):
    username = StringField(validators= [InputRequired(message = "Input required")  ] , render_kw= {"placeholder" : "Username"})
    password = PasswordField(validators= [InputRequired(message = "Input required")] ,render_kw= {"placeholder" : "Password"})
    submit = SubmitField("Login")


class receiveqeury(FlaskForm):
    city = SelectField('City', choices=['Islamabad', 'Lahore', 'Peshawar', 'Karachi'])
    bloodgroup =  SelectField('Blood Group' , choices =  [ 'A+' , 'A-' , 'B+' ,'B-' , 'AB+' ,'AB-', 'O+','O-'] )
    email = EmailField(validators=[Email(message="Input required")], render_kw={"placeholder": "Email"})
    submit = SubmitField("Search")



@app.route('/')
def home():
    conn = get_db_connection()
    top_donors = conn.execute('select username,count() from blooddonors where stat = "Approved" group by username order by count() desc ')

    return render_template('home.html' , top = top_donors)

@app.route('/who')
def who():
    return render_template('who.html')

@app.route('/donationprocess')
def donpro():
    return render_template('bloddtest.html')

@app.route('/why')
def why():
    return render_template('why.html')

@app.route('/login' ,methods = ['GET' ,'POST'])
def login():

    form = LoginForm()
    err = ''
    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()
        # print(form.username.data , user.username , user.password , form.password.data)

        if user :
            if user.password ==  form.password.data:
                # print("not same")
                login_user(user)
                # print("pohch gya idhar")
                return redirect(url_for('dashboard'))
            err = 'Invalid password'
        elif not user:
            err = 'Invalid Username'


    return render_template('login.html'  , form = form , error = err)

@app.route('/dashboard' ,methods = ['GET' ,'POST'])
@login_required
def dashboard():
    data=blooddonors.query.filter_by(username =  current_user.username)
    send = []
    for i in data:
        hos = donationcenters.query.filter_by(id=i.donatedto).first()
        send.append((i.token , i.time , i.date , hos.name ,hos.city , hos.Address , i.stat))



    return render_template('dashboard.html' , name = current_user.username , send = send)

@app.route('/logout' ,methods = ['GET' ,'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register' , methods = ['GET' ,'POST'])
def register():
    error = ''
    form = RegisterForm()
    if form.validate_on_submit():
        error = form.validate_userncnic(form.username, form.cnic)
        if  error == '':
            new_user = User(username = form.username.data , password = form.password.data , email = form.email.data
                        , age = form.age.data , cnic = form.cnic.data , secretof = form.secretof.data ,
                        bloodgroup = form.bloodgroup.data)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))

    return render_template('reg.html' , form = form , error = error)



@app.route('/donateblood' , methods = ['GET' ,'POST'])
@login_required
def donateblood():
    form = donateform()
    data = []
    show = 'invisible'
    ids = []
    if form.validate_on_submit():
        show = ''
        centers = donationcenters.query.filter_by(city=form.city.data)
        for i in centers:
            data.append((i.name , i.Address , i.id))
    if request.method == "POST":
        if request.form.get('selectedhos'):
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            now = str(now)
            now = now[: now.find('.')]
            now = now.replace(' ', '')
            now = now.replace('-', '')
            now = now.replace(':', '')
            tok = current_user.username + now
            hospitalid = request.form['selectedhos']
            new_user = blooddonors(username = current_user.username , token = tok , bloodgroup =  current_user.bloodgroup ,
                            time = current_time ,date = str(date.today()), stat = 'NotApproved'  , donatedto = hospitalid)
            db.session.add(new_user)
            db.session.commit()
            return redirect('dashboard')

    return render_template('donateblood.html', form=form , data = data , show = show   )
@app.route('/forgpass' , methods = ['GET' ,'POST'])
def forgotpass():
    form = forgetform()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data , secretof =  form.sec.data).first()
        if user:
            flash(f"Your password was {user.password}")
        else:
            flash(f"Invalid credentials")
    return render_template('forg.html' , form = form)

@app.route('/receiververf' , methods = ['GET' ,'POST'])
def receiververf():
    form =recverf()
    if form.validate_on_submit():
        take = blooddonors.query.filter_by(takenby=form.token.data).first()
        if take:
            rectk = receivers.query.filter_by(id=form.token.data).first()
            take.takenby= None
            rectk.status = 'Not'
            flash('Sorry for that!! we will contact you soon and will investigate the issue')
            db.session.commit()
        else:
            flash('No record found')
    return render_template('receiververf.html' , form = form)


@app.route('/adminlogin'  , methods = ['GET' , 'POST'])
def adminlogin():
    global check
    form = adminForm()
    err = ''
    adminu = admin.query.filter_by(username=form.username.data).first()
    if adminu:
        if adminu.password == form.password.data:
            check = 1
            return redirect(url_for('adminpanel'))
        err = 'invalid username or password'
    return  render_template('adminlogin.html' , form = form , error = err)

@app.route('/adminpanel' , methods = ['GET' , 'POST'])
def adminpanel():
    global check
    form = admincheck()
    if check == 1:
        error = ''
        if form.validate_on_submit():
            print(form.token.data)
            tok = blooddonors.query.filter_by(token=form.token.data).first()
            print(tok)
            if tok:
                tok.stat = 'Approved'
                flash('Donation is Approved!!')
                db.session.commit()
                check = 0
            else:
                flash('No record found')
                check = 0
        return render_template('adminpanel.html' , form = form )
    else:
        check = 1
        return render_template('adminpanel.html', form=form)


bloodtemp = ''
citytemp = ''
emailtemp = ''
display = ''

@app.route('/receiveblood'  , methods = ['GET' , 'POST'])
def receiveblood():
    global display
    global bloodtemp
    global citytemp
    global emailtemp
    data = []
    use = []
    show = 'invisible'
    form1 = receiveqeury()
    if form1.validate_on_submit():
        print('hello')
        show = ''
        bloodtemp = form1.bloodgroup.data
        citytemp = form1.city.data
        emailtemp = form1.email.data
        conn = get_db_connection()
        if bloodtemp == 'A+':
            data=conn.execute(f"select d.name , d.Address ,count(name) from donationcenters d , blooddonors b where b.donatedto == d.id and b.bloodgroup in ('A+' , 'A-' , 'O+' , 'O-') and d.city == '{citytemp}' and b.stat = 'Approved' and b.takenby is null group by name;").fetchall()
        elif bloodtemp == 'A-':
            data = conn.execute( f"select d.name , d.Address ,count(name) from donationcenters d , blooddonors b where b.donatedto == d.id and b.bloodgroup in ('A-' , 'O-') and d.city == '{citytemp}' and b.stat = 'Approved' and b.takenby is null group by name;").fetchall()
        elif bloodtemp == 'B+':
            data = conn.execute(
                f"select d.name , d.Address ,count(name) from donationcenters d , blooddonors b where b.donatedto == d.id and b.bloodgroup in ('B+' , 'B-' , 'O+' , 'O-') and d.city == '{citytemp}' and b.stat = 'Approved' and b.takenby is null group by name;").fetchall()
        elif bloodtemp == 'B-':
            data = conn.execute(
                f"select d.name , d.Address ,count(name) from donationcenters d , blooddonors b where b.donatedto == d.id and b.bloodgroup in ('B-'  , 'O-') and d.city == '{citytemp}' and b.stat = 'Approved' and b.takenby is null group by name;").fetchall()
        elif bloodtemp == 'AB+':
            data = conn.execute(
                f"select d.name , d.Address ,count(name) from donationcenters d , blooddonors b where b.donatedto == d.id and d.city == '{citytemp}' and b.stat = 'Approved' and b.takenby is null group by name;").fetchall()
        elif bloodtemp == 'AB-':
            data = conn.execute(
                f"select d.name , d.Address ,count(name) from donationcenters d , blooddonors b where b.donatedto == d.id and b.bloodgroup in ('AB-' , 'A-' , 'B-' , 'O-') and d.city == '{citytemp}' and b.stat = 'Approved' and b.takenby is null group by name;").fetchall()
        elif bloodtemp == 'O+':
            data = conn.execute(
                f"select d.name , d.Address ,count(name) from donationcenters d , blooddonors b where b.donatedto == d.id and b.bloodgroup in ('O+' , 'O-') and d.city == '{citytemp}' and b.stat = 'Approved' and b.takenby is null group by name;").fetchall()
        elif bloodtemp == 'O-':
            data = conn.execute(
                f"select d.name , d.Address ,count(name) from donationcenters d , blooddonors b where b.donatedto == d.id and b.bloodgroup in ('O-') and d.city == '{citytemp}' and b.stat = 'Approved' and b.takenby is null group by name;").fetchall()
        conn.close()
        if not data:
            flash("Sorry!! Not Available yet")

    if request.method == "POST":

        if request.form.get('selectedhos'):
            now = datetime.now()
            now = str(now)
            now = now[: now.find('.')]
            now = now.replace(' ', '')
            now = now.replace('-', '')
            now = now.replace(':', '')
            tok = emailtemp + now
            conn = get_db_connection()
            if bloodtemp == 'A+':
                use =conn.execute(f"select b.id from blooddonors b , donationcenters d  where b.donatedto == d.id  and b.bloodgroup in ('A+' , 'A-' , 'O+' , 'O-') and d.name == '{request.form['selectedhos']}' and b.stat = 'Approved' and  b.takenby is null;").fetchone()

            elif bloodtemp == 'A-':
                use = conn.execute(
                    f"select b.id from blooddonors b , donationcenters d  where b.donatedto == d.id  and b.bloodgroup in ('A-' , 'O-') and d.name == '{request.form['selectedhos']}' and b.stat = 'Approved' and  b.takenby is null;").fetchone()

            elif bloodtemp == 'B+':
                use = conn.execute(
                f"select b.id from blooddonors b , donationcenters d  where b.donatedto == d.id  and b.bloodgroup in ('B+' , 'B-' , 'O+' , 'O-') and d.name == '{request.form['selectedhos']}' and b.stat = 'Approved' and  b.takenby is null;").fetchone()

            elif bloodtemp == 'B-':
                use = conn.execute(
                f"select b.id from blooddonors b , +donationcenters d  where b.donatedto == d.id  and b.bloodgroup in ('B-'  , 'O-') and d.name == '{request.form['selectedhos']}' and b.stat = 'Approved' and  b.takenby is null;").fetchone()
            elif bloodtemp == 'AB+':
                use = conn.execute(
                f"select b.id from blooddonors b , donationcenters d  where b.donatedto == d.id  and d.name == '{request.form['selectedhos']}' and b.stat = 'Approved' and  b.takenby is null;").fetchone()
            elif bloodtemp == 'AB-':
                use = conn.execute(
                f"select b.id from blooddonors b , donationcenters d  where b.donatedto == d.id  and b.bloodgroup in ('AB-' , 'A-' , 'B-' , 'O-') and d.name == '{request.form['selectedhos']}' and b.stat = 'Approved' and  b.takenby is null;").fetchone()
            elif bloodtemp == 'O+':
                use = conn.execute(
                f"select b.id from blooddonors b , donationcenters d  where b.donatedto == d.id  and b.bloodgroup in ('O+' , 'O-') and d.name == '{request.form['selectedhos']}' and b.stat = 'Approved' and  b.takenby is null;").fetchone()
            elif bloodtemp == 'O-':
                use = conn.execute(
                f"select b.id from blooddonors b , donationcenters d  where b.donatedto == d.id  and b.bloodgroup in ('O-') and d.name == '{request.form['selectedhos']}' and b.stat = 'Approved' and  b.takenby is null;").fetchone()\

            new_user = receivers(id = tok , email = emailtemp  , bloodgroup = bloodtemp , hosname = request.form['selectedhos'] , city = citytemp  , status = 'Done')
            db.session.add(new_user)
            db.session.commit()
            if tok and use:
                conn.execute(f"UPDATE blooddonors SET takenby = '{tok}' WHERE id = {use[0]};")
                display = f"You are successfully register for blood recieving your unique code is  {tok} , this will be used for your identification at blood donation center (Email has also been sent) "
                msg = Message('Hello from bleed the smart way!', sender='bleedthesmartway@gmail.com', recipients=[f"{emailtemp}"])
                msg.body = f"Hey , this is your unique token {tok} you can verify using this token on webiste if you " \
                           f"have recieved blood or not "
                mail.send(msg)
                flash(display ,  "warning")
                conn.commit()


    return render_template('receiveblood.html', form=form1, data=data, show=show )










if __name__ == '__main__':
    app.run(debug = True , host = "0.0.0.0" , port = 443 , threaded=True)
    #
    # id = db.Column(db.Integer, primary_key=True , autoincrement=True)
    # username = db.Column(db.String(20) , nullable = False)
    # token = db.Column(db.String(20) , nullable = False)
    # bloodgroup = db.Column(db.String(4) , nullable = False)
    # time = db.Column(db.String(20) )
    # date = db.Column(db.String(20))
    # staus = db.Column(db.String(10) , nullable = False)
    # donatedto = db.Column(db.Integer , db.ForeignKey('donationcenters.id'))

# INSERT INTO donationcenters (name,city ,Address)
# VALUES( 'Ali Hospital',	'Peshawar' ,'Pakistan monument road peshawar');