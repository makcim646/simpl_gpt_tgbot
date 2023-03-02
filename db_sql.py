import sqlite3 as sql
import json
import configparser
import os


def creat_db():
    con = sql.connect('client.db')
    with con:
        con.execute("""
                CREATE TABLE IF NOT EXISTS CLIENT(
                id_user INTEGER RPRIMARY KEY AUTO_INCREMENT,
                message TEXT);""")


def chek_user(id_user):
    con = sql.connect('client.db')
    with con:
        data = con.execute("SELECT message FROM CLIENT WHERE id_user=?",
                           [id_user])
        if data.fetchall() == []:
            return False
        return True


def get_message(id_user):
    if chek_user(id_user):
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
    pass
