from resBot import app, db, bcrypt, base_url
from resBot.forms import *
from resBot.models import *
from flask import redirect, url_for, render_template, request, jsonify
from flask_login import login_user, current_user, login_required
import datetime
import secrets
import pytz



@app.route(base_url +'/resAdminLogin', methods=['GET', 'POST'])
def login():
    loginForm = ResAdminLogin()
    if loginForm.validate_on_submit():
        resAdmin = ResAdmin.query.filter_by(username=loginForm.userName.data).first()
        if resAdmin and bcrypt.check_password_hash(resAdmin.password, loginForm.password.data):
            login_user(resAdmin, remember=True)
            return redirect(url_for('home'))
    return render_template('login.html', form=loginForm)


@app.route('/home')
@app.route('/')
def home():
    curr_time = datetime.datetime.now(tz=pytz.timezone("Africa/Cairo")).strftime("%A, %B %Y Time: %H:%M:%S")
    return render_template('home.html', curr_time=curr_time)



@app.route(base_url + '/branch/add', methods=['GET', 'POST'])
@login_required
def add_resala_branch():
    add_branch_form = SimpleForm()
    if add_branch_form.validate_on_submit():
        resala_branch = ResalaBranch(name=add_branch_form.name.data.strip())
        db.session.add(resala_branch)
        db.session.commit()
        return redirect(url_for("show_resala_branches"))
    return render_template("simpleForm.html", title='Add a Resala Branch', form=add_branch_form)



@app.route(base_url +'/branch/', methods=['GET'])
@login_required
def show_resala_branches():
    branches = ResalaBranch.query.all()
    return render_template("simpleList.html", title='Stored Resala Branches', items=branches)



@app.route(base_url +'/activity/add', methods=['GET', 'POST'])
@login_required
def add_resala_activity():
    add_activity_form = SimpleForm()
    if add_activity_form.validate_on_submit():
        resala_activity = ResalaActivity(name=add_activity_form.name.data.strip())
        db.session.add(resala_activity)
        db.session.commit()
        return redirect(url_for('show_resala_activity'))
    return render_template("simpleForm.html", title='Add a Resala Activity', form=add_activity_form)



@app.route(base_url +'/activity/', methods=['GET'])
@login_required
def show_resala_activity():
    resalaActivities = ResalaActivity.query.all()
    return render_template('activities.html',activities=resalaActivities)



@app.route(base_url +'/committee/add', methods=['GET', 'POST'])
@login_required
def add_committee():
    add_committee_form = AddResalaCommittee()
    add_committee_form.activity_id.choices = [(x.id, x.name) for x in ResalaActivity.query.all()]
    if add_committee_form.validate_on_submit():
        resala_committee = ResalaCommittee(name=add_committee_form.name.data.strip(),
                                           activity_id=add_committee_form.activity_id.data)
        db.session.add(resala_committee)
        db.session.commit()
        return redirect(url_for('show_resala_committees', activity_id=resala_committee.activity_id))
    return render_template('add_committee.html', form=add_committee_form)



@app.route(base_url +'/committee/', methods=['GET'])
@login_required
def show_resala_committees():
    activity_id = request.args.get('activity_id')
    activity = None
    title = None
    committees = []
    if activity_id:
        activity = ResalaActivity.query.get(int(activity_id))
        title =  'لجان ' + activity.name
        if activity:
            committees = ResalaCommittee.query.filter_by(activity_id=activity.id)
    else:
        committees = ResalaCommittee.query.all()

    return render_template('simpleList.html',title=title, items=committees)



@app.route(base_url +'/memberRole/add', methods=['GET', 'POST'])
@login_required
def add_member_role():
    add_member_role_form = SimpleForm()
    if add_member_role_form.validate_on_submit():
        member_role = MemberRole(name=add_member_role_form.name.data.strip())
        db.session.add(member_role)
        db.session.commit()
        return redirect(url_for('show_member_roles'))
    return render_template('simpleForm.html', title='Add a Member Role', form=add_member_role_form)



@app.route(base_url +'/memberRole/', methods=['GET'])
@login_required
def show_member_roles():
    member_roles = MemberRole.query.all()
    return render_template('simpleList.html', title='Stored Member Roles', items=member_roles)



@app.route(base_url +'/contributionType/add', methods=['GET', 'POST'])
@login_required
def add_contribution_type():
    add_contribution_type_form = SimpleForm()
    if add_contribution_type_form.validate_on_submit():
        contribution_type = ContributionType(name=add_contribution_type_form.name.data.strip())
        db.session.add(contribution_type)
        db.session.commit()
        return redirect(url_for('show_contribution_types'))
    return render_template('simpleForm.html', title='Add a Contribution Type', form=add_contribution_type_form)



@app.route(base_url +'/contributionType/', methods=['GET'])
@login_required
def show_contribution_types():
    contribution_types = ContributionType.query.all()
    return render_template('simpleList.html', title='Stored Contribution Types', items=contribution_types)





@app.route(base_url +'/bot/add_bot/', methods=['GET', 'POST'])
@login_required
def add_bot():
    add_bot_form = AddBot()
    add_bot_form.activity_id.choices = [(x.id, x.name) for x in ResalaActivity.query.all()]
    if add_bot_form.validate_on_submit():
        generated_id = secrets.token_hex(16)
        while Bot.query.get(generated_id):
            generated_id = secrets.token_hex(16)
        bot = Bot(id=generated_id, name=add_bot_form.name.data.strip(),
                  activity_id=add_bot_form.activity_id.data, url=add_bot_form.url.data)
        db.session.add(bot)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_bot.html', form=add_bot_form)


@app.route(base_url +'/bot/', methods=['GET'])
@login_required
def show_all_bots():
    bots = Bot.query.all()
    return render_template('bots.html', bots = bots)


@app.route(base_url +'/bot/<bot_id>', methods=['GET'])
@login_required
def show_bot(bot_id):
    bot_dict = {}
    if bot_id:
        bot = Bot.query.get(bot_id)
        bot_dict = bot.get_dict()
    return jsonify(bot_dict)