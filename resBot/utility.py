from flask import jsonify


def change_hindi_numerals_to_arabic(num_str: str):
    new_num_str = []
    for char in num_str:
        char_unicode = ord(char)
        if ord('٠') <= char_unicode <= ord('٩'):
            char_diff = ord('٠') - ord('0')
            new_num_str.append(chr(char_unicode - char_diff))
        else:
            new_num_str.append(char)
    return "".join(new_num_str)


def get_response(msg, status: int):
    msg_json = jsonify({"msg": msg})
    msg_json.status_code = status
    return msg_json