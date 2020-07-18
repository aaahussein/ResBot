# -*- coding: utf-8 -*-
from resBot import app, db, bcrypt, base_url
from resBot.models import *
from flask import redirect, url_for, render_template, request, jsonify, Response
import datetime
import pytz
from resBot import utility
import json
from resBot.utility import get_response




def get_contribution_from_request(contribution_request: dict,
                                  member_id: int) -> (Contribution, list, list):
    missing_required_params = []
    wrong_required_params = []
    try:
        contribution_type_name = contribution_request.get("contribution_type").strip()
        try:
            contribution_type = ContributionType.query.filter_by(
                name=contribution_type_name).first()
            contribution_type_id = contribution_type.id
        except:
            wrong_required_params.append("contribution_type: {0}".format(contribution_type_name))
            contribution_type_id = None
    except:
        missing_required_params.append("contribution_type")
        contribution_type_id = None
    try:
        date_str = contribution_request.get('date').strip()
        if date_str == "امس":
            date = datetime.date.today() - datetime.timedelta(days=1)
        elif date_str == "قبل امس":
            date = datetime.date.today() - datetime.timedelta(days=2)
        else:
            date = datetime.date.today()
    except:
        date = datetime.date.today()
    try:
        details = contribution_request.get('details').strip()
    except:
        details = None
    try:
        amount_money = contribution_request.get('amount_money')
        if not isinstance(amount_money, int):
            amount_money = contribution_request.get('amount_money').strip()
            amount_money = int(amount_money)
    except:
        amount_money = 0
    try:
        did_receive_money_str = contribution_request.get('did_receive_money').strip()
        if did_receive_money_str == "مستلمتش":
            did_receive_money = False
        else:
            did_receive_money = True
    except:
        did_receive_money = True
    contribution = Contribution(member_id=member_id, contribution_type_id=contribution_type_id,
                                date=date, details=details, amount_money=amount_money,
                                did_receive_money=did_receive_money)
    return contribution, missing_required_params, wrong_required_params


@app.route(base_url + '/bot/<bot_id>/member/<member_phone>/contribution', methods=['POST'])
def create_contribution(bot_id, member_phone):
    bot = Bot.query.get(bot_id)
    if bot is None:
        return get_response("bot {0} is not found".format(bot_id), 404)
    member_phone = utility.change_hindi_numerals_to_arabic(member_phone)
    member = Member.query.filter_by(phone=member_phone).first()
    if member is None:
        return get_response("member {0} is not found for bot {1}".
                            format(member_phone, bot_id), 404)
    contribution_request = request.get_json(force=True)
    (contribution, missing_required_params, wrong_required_params) = \
        get_contribution_from_request(contribution_request, member)
    if len(missing_required_params) > 0:
        error_msg = "The following required parameters are missing: " + ", ".join(missing_required_params)
        return get_response(error_msg, 400)
    if len(wrong_required_params) > 0:
        error_msg = "The following parameters couldn't be found in the database:" \
                    + '\n'.join(wrong_required_params)
        return get_response(error_msg, 400)
    member.contributions.append(contribution)
    db.session.add(member)
    db.session.commit()
    response = {"messages": [{"text": "تم تسجيل المشاركة بنجاح"}]}
    response = jsonify(response)
    response.status_code = 201
    return response


@app.route(base_url + '/bot/<bot_id>/member/<member_phone>/contribution/', methods=['GET'])
def get_contributions(bot_id, member_phone):
    bot = Bot.query.get(bot_id)
    if bot is None:
        return get_response("bot {0} is not found".format(bot_id), 404)
    member_phone = utility.change_hindi_numerals_to_arabic(member_phone)
    member = Member.query.filter_by(phone=member_phone).first()
    if member is None:
        return get_response("member {0} is not found for bot {1}".
                            format(member_phone, bot_id), 404)
    contributions = Contribution.query.filter_by(member_id=member.id)
    try:
        start_date_str = request.args.get("start_date")
        start_date = datetime.datetime.strptime(start_date_str, "%d-%m-%Y").date()
        contributions = contributions.filter(Contribution.date >= start_date)
    except:
        pass
    try:
        end_date_str = request.args.get("end_date")
        end_date = datetime.datetime.strptime(end_date_str, "%d-%m-%Y").date()
        contributions = contributions.filter(Contribution.date <= end_date)
    except:
        pass
    contributions_dict = [x.to_dict() for x in contributions]
    response_dict = {"contributions": contributions_dict}
    response_json = json.dumps(response_dict, ensure_ascii=False)
    return response_json
