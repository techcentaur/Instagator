import json
import pprint
import requests
import argparse
from collections import OrderedDict

class Instagator:
    
    def __init__(self, **kwargs):
        """initialises the constructor of the class"""
        
        default_attr = dict(username='')

        allowed_attr = list(default_attr)
        default_attr.update(kwargs)

        for key in default_attr:
            if key in allowed_attr:
                self.__dict__[key] = default_attr.get(key)

    def userpage_scraper(self, user):
        """scrapes user json data from instagram response"""

        self.base_url = 'https://www.instagram.com/'

        response = requests.get(self.base_url + user)
        raw = response.text
        
        if raw is not None and '_sharedData' in raw:
            jsondata = raw.split("window._sharedData = ")[1].split(";</script>")[0]
            
            datadict = (json.loads(jsondata))

        return (datadict)

    def rootuser_info(self, datadict):
        """returns user basic information in a dictionary"""

        dict1 = OrderedDict()
        dict1 = datadict['entry_data']['ProfilePage'][0]['graphql']['user']

        userdict = OrderedDict()
        keylist = ['id', 'username', 'full_name', 'biography', 'edge_follow', 'edge_followed_by', 'is_private', 'external_url', 'profile_pic_url_hd']

        for key in keylist:
            if key is 'edge_follow':
                userdict['following'] = dict1[key]
            elif key is 'edge_followed_by':
                userdict['followers'] = dict1[key]
            else:
                userdict[key] = dict1[key]

        userdict['platform'] = datadict['platform']

        return (json.dumps(userdict, indent=4))


    def user_images_url(self, datadict):
        """returns all posts information in dictionary with keys as is_video, url, and caption"""

        dict1 = datadict['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']
        no_of_posts = dict1['count']

        posts = dict1['edges']

        posts_info = {}
        for count, post in enumerate(posts):
            tempdict = {}

            tempdict['url'] = "https://www.instagram.com/p/" + post['node']['shortcode']
            tempdict['is_video'] = post['node']['is_video']
            tempdict['caption'] = post['node']['edge_media_to_caption']['edges'][0]['node']


            posts_info[count] = tempdict

        return (posts_info)


    def crawling_images_url(self, data_dict, output_choice, commentors = False, tagged = True):
        """returns username list of all people in comments and tags"""

        content = []
        usernamelist = []

        for key in data_dict:
            data = self.json_url(data_dict[key]['url'])
            tempdict = data['entry_data']['PostPage'][0]['graphql']['shortcode_media']
            
            if commentors:
                for comment in tempdict['edge_media_to_comment']['edges']:
                    newuser = comment['node']['owner']['username']
                    if newuser not in usernamelist and newuser != self.username:
                        usernamelist.append(newuser)
                        data1 = self.rootuser_info(self.userpage_scraper(newuser))
                        if output_choice[0]:
                            print(data1)
                        elif output_choice[1]:
                            content.append(data1)

            if tagged:
                for tag in tempdict['edge_media_to_tagged_user']['edges']:
                    newuser = tag['node']['user']['username']
                    if newuser not in usernamelist and newuser != self.username:
                        usernamelist.append(newuser)
                        data1 = self.rootuser_info(self.userpage_scraper(newuser))
                        if output_choice[0]:
                            print(data1)
                        elif output_choice[1]:
                            content.append(data1)

        if output_choice[1]:
            self.pretty_print({'content': content}, False)


    @staticmethod
    def json_url(url):
        """returns json data of response from requesting an url"""
        
        response = requests.get(url)
        raw = response.text

        if raw is not None and '_sharedData' in raw:
            data = raw.split("window._sharedData = ")[1].split(";</script>")[0]
            
            datadict = (json.loads(data))        

        return datadict

    @staticmethod
    def pretty_print(datadict, do_print=True):
        """prints or saves in a file, json data mainpulation functions"""
        
        if do_print:
            print(json.dumps(datadict, sort_keys=True, indent=4))
        else:
            with open('jsondata.json', 'w') as outfile:
                outfile.write(json.dumps(datadict, sort_keys=True, indent=4))
            outfile.close()

        return 0

    def maincall(self, usernamelist, output_choice, tag_bool, com_bool):
        """makes calls to functions as it should"""
        
        dict1 = self.userpage_scraper(usernamelist)
        dict2 = self.user_images_url(dict1)

        self.crawling_images_url(dict2, output_choice, com_bool, tag_bool)


def main():
    parser = argparse.ArgumentParser(description='Instagator : Investigate people on Instagram')
    
    parser.add_argument('username', help='User to be searched', default=None)
    parser.add_argument('-t', '--tagged', help='Include people who are tagged in photos (default=True)', default=True, action="store_true")
    parser.add_argument('-c', '--commentors', help='Include people who have commented on photos (default=False)', default=False, action="store_true")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-p', '--print', help='Print the output (default)', action="store_true")
    group.add_argument('-f', '--file', help='Save in file in JSON format', action="store_true")

    args = parser.parse_args()

    insta = Instagator(**vars(args))
    insta.maincall(args.username, [args.print, args.file], args.tagged, args.commentors)


if __name__=="__main__":
    main()