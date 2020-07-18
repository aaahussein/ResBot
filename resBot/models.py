from resBot import db
from resBot import login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return ResAdmin.query.get(int(user_id))


class ResAdmin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


class ResalaBranch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)


class ResalaActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    committees = db.relationship('ResalaCommittee', lazy=True, backref=db.backref('resalaActivity', lazy=True))


class ResalaCommittee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('resala_activity.id'), nullable=False)


class MemberRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)


class Bot(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.Text, nullable=False)
    url = db.Column(db.String)
    activity_id = db.Column(db.Integer, db.ForeignKey('resala_activity.id'), nullable=False)
    members = db.relationship('Member', lazy=True, backref='bot')
    activity = db.relationship('ResalaActivity', lazy=True)
    def get_dict(self):
        bot = {}
        bot['id'] = self.id
        bot['name'] = self.name
        bot['url'] = self.url
        bot['activity_id'] = self.activity_id
        return bot

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(15), nullable=False)
    name = db.Column(db.Text, nullable=False)
    bot_id = db.Column(db.Integer, db.ForeignKey('bot.id'), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('resala_branch.id'), nullable=False)
    committee_id = db.Column(db.Integer, db.ForeignKey('resala_committee.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('member_role.id'))
    messenger_id = db.Column(db.Integer)
    national_number = db.Column(db.String(14))
    gender = db.Column(db.String(1))
    created_at = db.Column(db.DateTime, nullable=False)
    edited_at = db.Column(db.DateTime)
    contributions = db.relationship('Contribution', lazy=True, backref='member')

    def __eq__(self, other):
        return self.phone == other.phone

    def get_member_dict(self):
        member_dict = {}
        member_dict['id'] = self.id
        member_dict['phone'] = self.phone
        member_dict['name'] = self.name
        member_dict['bot_id'] = self.bot_id
        member_dict['branch_id'] = self.branch_id
        member_dict['committee_id'] = self.committee_id
        member_dict['role_id'] = self.role_id
        member_dict['messenger_id'] = self.messenger_id
        member_dict['national_number'] = self.national_number
        member_dict['gender'] = self.gender

        member_dict['created_at'] = self.created_at
        member_dict['edited_at'] = self.edited_at
        if self.created_at:
            member_dict['created_at'] = self.created_at.strftime("%A, %B %Y Time: %H:%M:%S")
        if self.edited_at:
            member_dict['edited_at'] = self.edited_at.strftime("%A, %B %Y Time: %H:%M:%S")
        return member_dict


class ContributionType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    contributions = db.relationship('Contribution', lazy=True, backref='contribution_type')


class Contribution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    contribution_type_id = db.Column(db.Integer, db.ForeignKey('contribution_type.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    details = db.Column(db.Text)
    amount_money = db.Column(db.Integer, default=0)
    did_receive_money = db.Column(db.Boolean, default=True)

    def to_dict(self):
        contribution_dict = {}
        contribution_dict['id'] = self.id
        contribution_dict['contribution_type'] = self.contribution_type.name
        contribution_dict['date'] = self.date.strftime("%d-%m-%Y")
        if self.details:
            contribution_dict["details"] = self.details
        contribution_dict['amount_money'] = self.amount_money
        contribution_dict['did_receive_money'] = self.did_receive_money
        return contribution_dict
