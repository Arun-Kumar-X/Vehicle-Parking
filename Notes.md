GitHub:
gh auth status
gh auth login

git status
git add .
git commit -m "MESSAGE"
git push origin main

Database Creation (After Models):
>>> from app import *
>>> db.create_all()
(If any issues, just remove the "instance" folder and try again!)

Add Data: 
>>> user = User(username = "Admin", full_name = "Super User", email = "admin@user.com", password = "54321")
>>> db.session.add(user)
>>> db.session.commit()