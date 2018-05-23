import json
import pprint
import requests
import argparse


class Instagator:
    
    def __init__(self, **kwargs):
        default_attr = dict(username='')

        allowed_attr = list(default_attr)
        default_attr.update(kwargs)

        for key in default_attr:
            if key in allowed_attr:
                self.__dict__[key] = default_attr.get(key)

    def userpage_scraper(self, usernamelist):
        self.base_url = 'https://www.instagram.com/'

        for user in usernamelist:
            response = requests.get(self.base_url + user)
            raw = response.text
            
            if raw is not None and '_sharedData' in raw:
                jsondata = raw.split("window._sharedData = ")[1].split(";</script>")[0]
                
                datadict = (json.loads(jsondata))

        return(datadict)

    def rootuser_info(self, datadict):

        dict1 = datadict['entry_data']['ProfilePage'][0]['graphql']['user']

        userdict = {}
        keylist = ['username', 'full_name', 'id', 'is_private', 'external_url', 'profile_pic_url', 'profile_pic_url_hd', 'edge_follow', 'edge_followed_by']

        for key in keylist:
            userdict[key] = dict1[key]

        print(userdict)


    def images_url(self, datadict):
        pass

    @staticmethod
    def pretty_print(datadict):

        with open('jsondata.json', 'w') as outfile:
            outfile.write(json.dumps(datadict, sort_keys=True, indent=4))

        outfile.close()


def main():
    parser = argparse.ArgumentParser(description='Instagator : Investigate people on Instagram')
    
    parser.add_argument('username', help='User to be searched', default=None)
    args = parser.parse_args()

    insta = Instagator(**vars(args))
    insta.userpage_scraper([args.username])

if __name__=="__main__":
    main()