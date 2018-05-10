import argparse
import requests



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
        self.session.headers = {'user-agent': CHROME_WIN_UA}



def main():
    parser = argparse.ArgumentParser(description='Instagator : Investigate people on Instagram')
    parser.add_argument('username', help='User to be searched', default=None)
    parser.add_argument('-u', '--user-login', '--user_login', help='Instagram Username', default=None, required=True)
    parser.add_argument('-p', '--pass-login', '--pass_login', help='Instagram Password', default=None, required=True)

    args = parser.parse_args()

    insta = Instagator(**vars(args))


if __name__=="__main__":
    main()