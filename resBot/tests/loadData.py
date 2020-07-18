import requests
bot_id = 'd479be6675ffe66023c58d2f86d06e77'


def load_members():
    members_file_path = 'data\\members.txt'
    with open(members_file_path, 'r', encoding='utf-8') as members_file:
        all_lines = members_file.readlines()
        for line in all_lines[1:]:
            (name, phone, branch, committee, role) = line.strip().split('\t')
            request_data = {'phone': phone, 'name': name, 'branch': branch,
                            'committee': committee, 'role': role}
            url = 'http://127.0.0.1:5000/v1/bot/{0}/member'.format(bot_id)
            r = requests.post(url, json=request_data)
            if not r.status_code == 201:
                print("{0} wasn't added\n the returned response {1}".format(name, r.text))

def load_contributions():
    contribution_file_path = 'data\\contributions.txt'
    with open(contribution_file_path, 'r', encoding='utf-8') as contributions_file:
        all_lines = contributions_file.readlines()
        for line in all_lines[1:]:
            (phone, cont_date, cont_type, details, amount_money, did_receive_money) = line.split('\t')
            did_receive_money = did_receive_money.strip()
            request_data = { 'contribution_type': cont_type, 'date': cont_date,
                            'details': details, 'amount_money': amount_money,
                             'did_receive_money': did_receive_money}
            url = 'http://127.0.0.1:5000/v1/bot/{0}/member/{1}/contribution'.format(bot_id, phone)
            r = requests.post(url, json=request_data)
            if not r.status_code == 201:
                print("{0} wasn't added\n the returned response {1}".format(phone, r.text))
