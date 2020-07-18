from resBot import db, bcrypt
from resBot.models import *
import os

db.drop_all()
db.create_all()
myPass = bcrypt.generate_password_hash(os.getenv('resAdminPassword')).decode('utf-8')
user = ResAdmin(username='resAdmin', password=myPass)
db.session.add(user)
resala_branches = [
    ResalaBranch(name='المعادي'),
    ResalaBranch(name='اكتوبر'),
    ResalaBranch(name='فيصل'),
    ResalaBranch(name='اسكندرية'),
    ResalaBranch(name='حلوان'),
    ResalaBranch(name='مصر الجديدة'),
    ResalaBranch(name='المهندسين'),
    ResalaBranch(name='مدينة نصر')
]
db.session.add_all(resala_branches)
resala_activities = [
    ResalaActivity(name='قوافل داخلية')
]
db.session.add_all(resala_activities)
resala_committees = [
    ResalaCommittee(resalaActivity=resala_activities[0], name='HR'),
    ResalaCommittee(resalaActivity=resala_activities[0], name='HR متطوعين'),
    ResalaCommittee(resalaActivity=resala_activities[0], name='اسقف'),
    ResalaCommittee(resalaActivity=resala_activities[0], name='مياه وبنا'),
    ResalaCommittee(resalaActivity=resala_activities[0], name='مجددون'),
    ResalaCommittee(resalaActivity=resala_activities[0], name='براعم'),
    ResalaCommittee(resalaActivity=resala_activities[0], name='استكشاف'),
    ResalaCommittee(resalaActivity=resala_activities[0], name='توعية'),
    ResalaCommittee(resalaActivity=resala_activities[0], name='عيني'),
    ResalaCommittee(resalaActivity=resala_activities[0], name='مسنين'),
    ResalaCommittee(resalaActivity=resala_activities[0], name='اطعام'),
    ResalaCommittee(resalaActivity=resala_activities[0], name='محو امية'),
    ResalaCommittee(resalaActivity=resala_activities[0], name='دعايا وميديا'),
    ResalaCommittee(resalaActivity=resala_activities[0], name='خدمات')
]
db.session.add_all(resala_committees)

member_roles = [
    MemberRole(name='ادارة'),
    MemberRole(name='مدير تنفيذي'),
    MemberRole(name='تيم ليدر'),
    MemberRole(name='ليدر لجنة'),
    MemberRole(name='مسئول'),
    MemberRole(name='ضيوف')
]
db.session.add_all(member_roles)

contribution_types = [
    ContributionType(name='البيت'),
    ContributionType(name='الفرع'),
    ContributionType(name='الخارج')
]
db.session.add_all(contribution_types)

bots = [
    Bot(id='d479be6675ffe66023c58d2f86d06e77', name='salaheldin', activity=resala_activities[0])
]
db.session.add_all(bots)
db.session.commit()
