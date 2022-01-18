# Flask Login System

This is a login system based on Flask. It has some features like email confirmation and reset password.

to run this project open your terminal and write these commands:
```

python -m venv venv
venv\Scripts\activate.bat

```
Linux
```

source venv/Scripts/activate

```

```

pip install -r requirements.txt

```
Windows
```

set FLASK_APP=auth_app.py
set FLASK_DEBUG=1 #optional
set ADMIN_EMAIL=admin_email
set SECRET_KEY=your_secret_key
set MAIL_USERNAME=email_address_to_send_emails_to_user
set MAIL_PASSWORD=email_password

```

Linux
```

export FLASK_APP=auth_app.py
export FLASK_DEBUG=1 #optional
exprot ADMIN_EMAIL=admin_email
export SECRET_KEY=your_secret_key
export MAIL_USERNAME=email_address_to_send_emails_to_user
export MAIL_PASSWORD=email_password

```

now create DB:
```
flask shell

```
```
db.create_all()
fake.g_user() #your can also generate users like this

```

```

flask run

```
Done

note: you need to turn on (google setting) less secure app access to send emails.
