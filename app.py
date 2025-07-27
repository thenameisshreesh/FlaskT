import random
from flask import Flask, render_template, request, redirect ,url_for
import sqlite3
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__, static_folder="../static", template_folder="../templates")


# Initialize DB
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS contacts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  email TEXT NOT NULL,
                  message TEXT NOT NULL)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)",
              (name, email, message))
    

        # Random confirmation messages
    confirmations = [
        "Thanks for reaching out to us!",
        "We've received your message and will reply shortly.",
        "Your form has been submitted successfully!",
        "Our team will connect with you soon.",
        "Thanks, we'll be in touch soon!"
    ]
    random_msg = random.choice(confirmations)

    # Email sending logic
    sender_email = "shreeshpitambare084@gmail.com"
    sender_password = "untk duvx aisq ssuq"
    receiver_email = email

    subject = "Form Submission Received"
    body = f"Hi {name},\n\n{random_msg}\n\nYour message:\n\"{message}\"\n\n— Team Shreesh"

    # Email content setup
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print("Email failed:", e)



    conn.commit()
    conn.close()

    return redirect(url_for("thankyou"))


@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')



def handler(environ, start_response):
    return app(environ, start_response)



if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)

