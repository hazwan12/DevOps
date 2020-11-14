import pandas as pd
from devops import db, bcrypt
from devops.models import User

userData = pd.read_csv("50user.csv")

for i in range(0,50):
   hashed_password = bcrypt.generate_password_hash(userData.iloc[i,2]).decode('utf-8')
   user = User(username=userData.iloc[i,0], email=userData.iloc[i,1], password=hashed_password,
                        role=userData.iloc[i,3])
   db.session.add(user)

db.session.commit()