import argparse
import requests
import json


class Instagator:
    
    def __init__(self, **kwargs):
        default_attr = dict(username='', user_login='', pass_login='')

        allowed_attr = list(default_attr)
        default_attr.update(kwargs)

        for key in default_attr:
            if key in allowed_attr:
                self.__dict__[key] = default_attr.get(key)

        print(self.__dict__)

        self.session = requests.Session()
        self.login()


    def login(self):
        base_url = 'https://www.instagram.com/'
        login_url = base_url + 'accounts/login/ajax/'

        user_agent = ''
        self.session.headers = {'user-agent' : user_agent}
        self.session.headers.update({'Referer': base_url})

        req = self.session.get(base_url)

        self.session.headers.update({'X-CSRFToken': req.cookies['csrftoken']})
        login_data = {'username': user_login, 'password': pass_login}

        login = self.session.post(login_url, )


def main():
    parser = argparse.ArgumentParser(description='Instagator : Investigate people on Instagram')
    parser.add_argument('username', help='User to be searched', default=None)
    parser.add_argument('-u', '--user-login', '--user_login', help='Instagram Username', default=None, required=True)
    parser.add_argument('-p', '--pass-login', '--pass_login', help='Instagram Password', default=None, required=True)

    args = parser.parse_args()

    insta = Instagator(**vars(args))


if __name__=="__main__":
    main()