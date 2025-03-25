from flask import Flask, render_template, request
import requests
from post import Post
import smtplib

app = Flask(__name__)

all_blogs = requests.get("https://api.npoint.io/486a92c9266e0d7becf2").json()
all_posts = []

for blog in all_blogs:
    post = Post(blog['id'],blog['title'],blog['subtitle'],blog['body'])
    all_posts.append(post)

@app.route('/')
def home():
    return render_template('index.html',  all_posts=all_posts)

@app.route('/about')
def get_about():
    return render_template('about.html')

@app.route('/contact')
def get_contact():
    return render_template('contact.html')

@app.route('/post/<int:index>')
def show_post(index):
    requested_post = None
    for blog_post in all_posts:
        if blog_post.id == index:
            requested_post = blog_post
    return render_template('post.html', post = requested_post)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template('contact.html', msg_sent= True)
    return render_template('contact.html', msg_sent= False)


OWN_EMAIL = "YOUR OWN EMAIL ADDRESS"
OWN_PASSWORD = "YOUR EMAIL ADDRESS PASSWORD"
def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as connection:
            connection.starttls()
            connection.login(OWN_EMAIL, OWN_PASSWORD)
            connection.sendmail(from_addr=OWN_EMAIL, to_addrs=OWN_EMAIL, msg=email_message.encode('utf-8'))
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


if __name__ == "__main__":
    app.run(debug=True)