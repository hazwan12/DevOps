import pandas as pd
from devops import db
from devops.models import Bug, User
from datetime import datetime, timezone
from dateutil import tz
import random

reporter_list = User.query.filter_by(role='Reporter').all()
developer_list = User.query.filter_by(role='Developer').all()
reviewer_list = User.query.filter_by(role='Reviewer').all()

def local_time(time):
    utc = time
    utc = utc.replace(tzinfo=tz.tzutc())
    return utc.astimezone(tz.tzlocal())

bugData = pd.read_csv("500bug.csv")

for i in range(0,500):
   bug = Bug(summary=bugData.iloc[i,0], date_posted=local_time(datetime.utcnow()),
               product=bugData.iloc[i,1], platform=bugData.iloc[i,2],
               whatHappen=bugData.iloc[i,3], howHappen=bugData.iloc[i,4],
               shouldHappen=bugData.iloc[i,5], status=bugData.iloc[i,6], priority=bugData.iloc[i,7],
               user_id=random.choice(reporter_list).id, developer_id=random.choice(developer_list).id, 
               reviewer_id=random.choice(reviewer_list).id)
   db.session.add(bug)

db.session.commit()