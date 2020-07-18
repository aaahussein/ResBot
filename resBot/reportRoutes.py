from resBot import db, base_url, app
from resBot.models import Member, Contribution, ContributionType
from sqlalchemy import func, and_
from flask import request, render_template
import pandas as pd
import datetime

def get_member_contribution_df(bot_id:str, start_date:datetime.datetime=None,
                               end_date:datetime.datetime=None) ->pd.DataFrame:
    count_label = 'count_label'
    contribution_type_label = "contribution_type"
    query = db.session.query(Member.phone, ContributionType.name.label(contribution_type_label),
                             Member.name, func.count(ContributionType.id).label(count_label)).\
        filter(Member.bot_id == bot_id).\
        filter(and_(Member.id == Contribution.member_id,
                    Contribution.contribution_type_id == ContributionType.id)).\
        group_by(Member.phone, Member.name, ContributionType.id)
    if start_date:
        query = query.filter(Contribution.date >= start_date)
    if end_date:
        query = query.filter(Contribution.date <= end_date)
    df = pd.read_sql(query.statement, query.session.bind)
    df = df.pivot_table(index=[Member.phone.key, Member.name.key], columns=contribution_type_label,
                  values=count_label).fillna(value=0)
    df["total"] = df.sum(axis=1)
    return df

@app.route(base_url + '/bot/<bot_id>/report/member_contributions', methods=['GET'])
def get_member_contributions_report(bot_id):
    start_date = None
    end_date = None
    try:
        start_date_str = request.args.get("start_date")
        start_date = datetime.datetime.strptime(start_date_str, "%d-%m-%Y")
    except:
        pass
    try:
        end_date_str = request.args.get("end_date")
        end_date = datetime.datetime.strptime(end_date_str, "%d-%m-%Y")
    except:
        pass
    contributions_df = get_member_contribution_df(bot_id, start_date, end_date)
    return render_template("members_contributions_report.html",
                           contributions_df = contributions_df.to_html(escape=False),
                           start_date = start_date, end_date = end_date)

