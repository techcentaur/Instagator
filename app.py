import argparse
import requests
import json
import pprint


class Instagator:
    
    def __init__(self, **kwargs):
        default_attr = dict(username='', user_login='', pass_login='')

        allowed_attr = list(default_attr)
        default_attr.update(kwargs)

        for key in default_attr:
            if key in allowed_attr:
                self.__dict__[key] = default_attr.get(key)

        self.session = requests.Session()
        self.login()


    def login(self):
        base_url = 'https://www.instagram.com/'
        login_url = base_url + 'accounts/login/ajax/'

        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
        self.session.headers = {'user-agent' : user_agent}
        self.session.headers.update({'Referer': base_url})

        req = self.session.get(base_url)

        self.session.headers.update({'X-CSRFToken': req.cookies['csrftoken']})
        login_data = {'username': self.user_login, 'password': self.pass_login}

        login = self.session.post(login_url, data=login_data, allow_redirects=True)
        self.session.headers.update({'X-CSRFToken': login.cookies['csrftoken']})

        cookies = login.cookies
        login_text = json.loads(login.text)

        # print(json.dumps(login_text))

        resp = self.session.get(base_url + self.username)
        resp = resp.text
        if resp is not None and '_sharedData' in resp:
            sd = resp.split("window._sharedData = ")[1].split(";</script>")[0]
            
            data = (json.loads(sd))

            # print(data['config']['viewer']['biography'])
            print(data['entry_data']['ProfilePage'][0]['graphql']['user']['biography'])
            print(data['entry_data']['ProfilePage'][0]['graphql']['user']['full_name'])
            print(data['entry_data']['ProfilePage'][0]['graphql']['user']['profile_pic_url_hd'])
            print(data['entry_data']['ProfilePage'][0]['graphql']['user']['username'])


def main():
    parser = argparse.ArgumentParser(description='Instagator : Investigate people on Instagram')
    parser.add_argument('username', help='User to be searched', default=None)
    parser.add_argument('-u', '--user-login', '--user_login', help='Instagram Username', default=None, required=True)
    parser.add_argument('-p', '--pass-login', '--pass_login', help='Instagram Password', default=None, required=True)

    args = parser.parse_args()

    insta = Instagator(**vars(args))
    # var() method takes only one parameter. It takes an object as parameter and returns the __dict__ module


if __name__=="__main__":
    main()