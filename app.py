from flask import Flask, render_template, request, redirect,session,flash
import pyotp
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = 'my-secret-key'
def send_otp(to_email):
    # generate a new OTP
    otp = pyotp.TOTP(pyotp.random_base32()).now()
    #string
    # create a message object
    msg = MIMEMultipart()

    msg['From'] = '##SENDEREMAIL##'
    msg['To'] = to_email
    msg['Subject'] = 'One-Time Password'

    # create the message body
    body = f'Your one-time password is: {otp}'
    msg.attach(MIMEText(body, 'plain'))

    # send the message
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login('##SENDEREMAIL##', 'APP_PASSWORD') 
        smtp.send_message(msg)
    
    return otp
        
        
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    password = request.form['password']
    session["otp"]=send_otp("email")
    return redirect("/otp")

@app.route('/otp', methods=["GET",'POST'])
def otp():
    if request.method == "POST":
        otp_string = ""
        for i in range(6):
            otp_string += request.form[str(i)]
        
        if otp_string == session["otp"]:
            flash('Thank you for signing up!', 'success')
            session["otp"] = None
        else:
            flash('Incorrect OTP', 'danger')
    return render_template("otp.html")
if __name__ == '__main__':
    app.run(debug=True)