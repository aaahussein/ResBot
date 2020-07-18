from resBot import app, base_url
from resBot.models import *
from flask import request
import datetime
import pytz
from resBot import utility
import json

from resBot.utility import get_response



def get_member_from_request(member_request: dict,
                            bot: Bot) -> (Member, list, list):
    missing_required_params = []
    wrong_required_params = []
    try:
        phone = member_request.get('phone').strip()
        phone = utility.change_hindi_numerals_to_arabic(phone)
    except:
        missing_required_params.append('phone')
        phone = None
    try:
        name = member_request.get('name').strip()
    except:
        name = None
        missing_required_params.append('name')
    try:
        branch_name = member_request.get('branch').strip()
        try:
            branch = ResalaBranch.query.filter_by(name=branch_name).first()
            branch_id = branch.id
        except:
            branch_id = None
            wrong_required_params.append('branch: {0}'.format(branch_name))
    except:
        branch_id = None
        missing_required_params.append('branch')
    try:
        committee_name = member_request.get('committee').strip()
        try:
            committee = ResalaCommittee.query.filter_by(name=committee_name, activity_id=bot.activity_id).first()
            committee_id = committee.id
        except:
            committee_id = None
            wrong_required_params.append('committee: {0}'.format(committee_name))
    except:
        committee_id = None
        missing_required_params.append('committee')
    try:
        role_name = member_request.get('role').strip()
        role = MemberRole.query.filter_by(name=role_name).first()
        role_id = role.id
    except:
        role_id = None
    try:
        gender = member_request.get('gender').strip()
        if gender not in ['M', 'F']:
            gender = None
    except:
        gender = None
    try:
        national_number = member_request.get('national_number').strip()
        national_number = utility.change_hindi_numerals_to_arabic(national_number)
        messenger_id = member_request.get('messenger_id').strip()
    except:
        national_number = None
        messenger_id = None
    member = Member(phone=phone, name=name,
                    branch_id=branch_id, committee_id=committee_id,
                    role_id=role_id, gender=gender, national_number=national_number,
                    messenger_id=messenger_id)
    return member, missing_required_params, wrong_required_params


@app.route(base_url + '/bot/<bot_id>/member', methods=['POST'])
def add_member(bot_id):
    bot = Bot.query.get(bot_id)
    if bot is None:
        return get_response("bot {0} is not found".format(bot_id), 404)
    member_request = request.get_json(force=True)

    (member, missing_required_params,
     wrong_required_params) = get_member_from_request(member_request, bot)
    if len(missing_required_params) > 0:
        error_msg = "The following required parameters are missing: " + ", ".join(missing_required_params)
        return get_response(error_msg, 400)
    if len(wrong_required_params) > 0:
        error_msg = "The following parameters couldn't be found in the database:" \
                    + '\n'.join(wrong_required_params)
        return get_response(error_msg, 400)
    member.created_at = datetime.datetime.now(tz=pytz.timezone("Africa/Cairo"))
    existing_member = Member.query.filter_by(phone=member.phone, bot_id=bot_id).first()
    if existing_member:
        return get_response('member {0} is already added to this bot'.format(member.phone), 409)
    bot.members.append(member)
    db.session.add(bot)
    db.session.commit()
    return get_response("member {0} is added to bot {1} successfully".format(member.phone, bot_id), 201)


@app.route(base_url + '/bot/<bot_id>/member/<member_phone>', methods=['PUT'])
def update_member(bot_id, member_phone):
    bot = Bot.query.get(bot_id)
    if bot is None:
        return get_response("bot {0} isn't found".format(bot_id), 404)
    existing_member = Member.query.filter_by(phone=member_phone).first()
    if existing_member is None:
        return get_response("member {0} isn't found for bot {1}".
                            format(member_phone, bot_id), 404)
    member_request = request.get_json(force=True)
    (member, missing_required_parameters,
     missing_required_parameters) = get_member_from_request(member_request, bot)
    if member.name:
        existing_member.name = member.name
    if member.branch_id:
        existing_member.branch_id = member.branch_id
    if member.committee_id:
        existing_member.committee_id = member.committee_id
    if member.role_id:
        existing_member.role_id = member.role_id
    if member.messenger_id:
        existing_member.messenger_id = member.messenger_id
    if member.national_number:
        existing_member.national_number = member.national_number
    if member.gender:
        existing_member.gender = member.gender
    existing_member.edited_at = datetime.datetime.now(tz=pytz.timezone("Africa/Cairo"))
    db.session.commit()
    return get_response("member {0} is updated successfully".format(member_phone), 200)


@app.route(base_url + '/bot/<bot_id>/member/<member_phone>', methods=['DELETE'])
def delete_member(bot_id, member_phone):
    bot = Bot.query.get(bot_id)
    if bot is None:
        return get_response("bot {0} isn't found".format(bot_id), 404)
    member_phone = utility.change_hindi_numerals_to_arabic(member_phone)
    existing_member = Member.query.filter_by(phone=member_phone).first()
    if existing_member is None:
        return get_response("member {0} isn't found for bot {1}".
                            format(member_phone, bot_id), 404)
    db.session.delete(existing_member)
    db.session.commit()
    get_response("member {0} is successfully deleted from bot {1}".
                 format(member_phone, bot_id), 200)


@app.route(base_url + '/bot/<bot_id>/member/<member_phone>', methods=['GET'])
def get_member(bot_id, member_phone):
    bot = Bot.query.get(bot_id)
    if bot is None:
        return get_response("bot {0} isn't found".format(bot_id), 404)
    member_phone = utility.change_hindi_numerals_to_arabic(member_phone)
    existing_member = Member.query.filter_by(phone=member_phone).first()
    if existing_member is None:
        return get_response("member {0} isn't found for bot {1}".
                            format(member_phone, bot_id), 404)
    existing_member_dict = json.dumps(existing_member.get_member_dict(), ensure_ascii=False)
    return existing_member_dict
