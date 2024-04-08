from flask import Flask, render_template, request
from email.message import EmailMessage
import ssl
import smtplib
import time

app = Flask(__name__)

def send_email(sender, password, receiver, subject, body):
    em = EmailMessage()
    em['From'] = sender
    em['To'] = receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    success = False
    attempts = 0
    max_attempts = 3
    
    while not success and attempts < max_attempts:
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(sender, password)
                smtp.sendmail(sender, receiver, em.as_string())
            success = True
            return True
        except Exception as e:
            attempts += 1
            print(f"An error occurred while attempting to send the email: {e}")
            time.sleep(5)
    
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        
        sender = 'holopo567@gmail.com'
        password = 'wrxx zejv tpyq wwbf'
        receiver = 'mohamadjalim50@gmail.com'
        subject = "Test"
        body = f"Hello {name}, this is a test email from Flask."

        if send_email(sender, password, receiver, subject, body):
            return render_template('success.html')
        else:
            return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)
