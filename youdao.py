import re
import sys

import requests

username = ''
password = ''
HEADERS = {
    'Content-type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.4 ' +
                  '(KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4'
}
TIMEOUT = 10


def _get_login_cookies():
    login_url = 'https://reg.163.com/logins.jsp'
    params = {
        'url': 'http://account.youdao.com/login' +
               '?service=dict&back_url=http%3A%2F%2Fdict.youdao.com&success=1',
        'product': 'search',
        'type': 1,
        'username': username,
        'password': password,
        'savelogin': 1
    }
    resp = requests.post(login_url, headers=HEADERS, params=params,
                         timeout=TIMEOUT)
    return resp.cookies.get_dict()


def _add_word(word):
    cookies = _get_login_cookies()
    add_word_url = 'http://dict.youdao.com/wordbook/ajax'
    params = {
        'action': 'addword',
        'q': word
    }
    resp = requests.post(add_word_url, headers=HEADERS, params=params,
                         cookies=cookies, timeout=TIMEOUT)
    if resp.status_code == 200 and resp.content == '{"message":"adddone"}':
        print('ok')
    elif resp.status_code == 409:
        pass


def fail_to_cache(word):
    # TODO
    pass


def main(text):
    m = re.match(u'[a-zA-Z]+', text)
    if m:
        _add_word(m.group())


if __name__ == '__main__':
    main(sys.argv[1])
