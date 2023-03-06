import sqlite3 as sql
import json
import configparser
import time
import os


def creat_db():
    con = sql.connect('client.db')
    with con:
        con.execute("""
                CREATE TABLE IF NOT EXISTS CLIENT(
                id_user INTEGER RPRIMARY,
                status BOOL,
                gift BOOL,
                time REAL,
                day INTEGER,
                message TEXT);""")


def add_in_db(id_user):
    con = sql.connect('client.db')
    with con:
        con.execute('UPDATE CLIENT set time=?, day=31, status=True, gift=False WHERE id_user=?',
                    [time.time(), id_user])
    return True


def extend(id_user):
    con = sql.connect('client.db')
    with con:
        con.execute('UPDATE CLIENT set time=?, day=day + 31 WHERE id_user=?',
                    [time.time(), id_user])
    return True


def add_gift(id_user):
    con = sql.connect('client.db')
    with con:
        con.execute('INSERT INTO CLIENT (id_user, status, gift, time, day, message) values(?, ?, ?, ?, ?, ?)',
                    [id_user, False, True, time.time(), 0, ''])
    return True


def close_gift(id_user):
    con = sql.connect('client.db')
    with con:
        con.execute('UPDATE CLIENT set gift=? WHERE id_user=?',
                    [False, id_user])
    return True


def check_gift(id_user):
    con = sql.connect('client.db')
    with con:
        data = con.execute("SELECT gift FROM CLIENT WHERE id_user=?",
                           [id_user])
        return True if data.fetchall()[0][0] == 1 else False


def check_client(id_user):
    con = sql.connect('client.db')
    with con:
        data = con.execute("SELECT * FROM CLIENT WHERE id_user=?",
                           [id_user])
        return True if len(data.fetchall()) > 0 else False


def deactive_user_db(id_user):
    con = sql.connect('client.db')
    with con:
        con.execute('UPDATE CLIENT set time=?, day=0, status=False WHERE id_user=?',
                    [time.time(), id_user])
    return True


def check_msg(id_user):
    con = sql.connect('client.db')
    with con:
        data = con.execute("SELECT message FROM CLIENT WHERE id_user=?",
                           [id_user])
        if data.fetchall()[0][0] == '':
            return False
        return True


def get_message(id_user):
    if check_msg(id_user):
        con = sql.connect('client.db')
        with con:
            data = con.execute("SELECT message FROM CLIENT WHERE id_user=?",
                               [id_user])
            message = json.loads(data.fetchall()[0][0])["message"]
            return message
    else:
        con = sql.connect('client.db')
        with con:
            message = {'message': [{"role": "system", "content": "You are a helpful assistant."}]}
            msg_text = json.dumps(message, ensure_ascii=False)
            con.execute('INSERT INTO CLIENT (id_user, message) values(?, ?)', [id_user, msg_text])
        return [{"role": "system", "content": "You are a helpful assistant."}]


def save_message(id_user, message):
    data = get_message(id_user)
    data.append(message)
    con = sql.connect('client.db')
    with con:
        message = {'message': data}
        msg_text = json.dumps(message, ensure_ascii=False)
        con.execute('UPDATE CLIENT SET message=? WHERE id_user=?', [msg_text, id_user])
    return True


def clean_message(id_user):
    con = sql.connect('client.db')
    with con:
        message = {'message': [{"role": "system", "content": "You are a helpful assistant."}]}
        msg_text = json.dumps(message, ensure_ascii=False)
        con.execute('UPDATE CLIENT SET message=? WHERE id_user=?', [msg_text, id_user])
    return True


def get_all():
    con = sql.connect('client.db')
    with con:
        data = con.execute("SELECT * FROM CLIENT")
        print(data.fetchall())


def create_config(path='setting.ini', bot_token='', api_key=''):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("setting")
    config.set("setting", "bot_token", f'{bot_token}')
    config.set("setting", "api_key", f'{api_key}')

    with open(path, "w") as config_file:
        config.write(config_file)


def get_config(path='setting.ini'):
    """
    Returns the config object
    """
    if not os.path.exists(path):
        bot_token = str(input('Input telegram bot token: '))
        api_key = str(input('Input API openai: '))
        create_config(path, bot_token, api_key)

    config = configparser.ConfigParser()
    config.read(path)
    out = {}
    for key in config['setting']:
        out[key] = config['setting'][key]
    return out

if __name__ == "__main__":
    creat_db()
    id_user = 12121
    add_in_db(id_user)
    #add_gift(id_user)
