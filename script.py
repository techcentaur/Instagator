import requests
import json
import argparse
import urllib.request
from PIL import Image
import os

class Insta:
    def __init__(self, username):
        self.username = username

    def data(self):
        base_url = 'https://www.instagram.com/'
        url = base_url + self.username

        session = requests.Session()
        r = requests.get(url)

        r = r.text
        if r is not None:
            sd = r.split("window._sharedData = ")[1].split(";</script>")[0]

            data = (json.loads(sd))

            bio = (data['entry_data']['ProfilePage'][0]['graphql']['user']['biography'])
            fullname = (data['entry_data']['ProfilePage'][0]['graphql']['user']['full_name'])
            image = (data['entry_data']['ProfilePage'][0]['graphql']['user']['profile_pic_url_hd'])
            name = (data['entry_data']['ProfilePage'][0]['graphql']['user']['username'])
    
            urllib.request.urlretrieve(image, name + ".jpg")
    
            return [bio, fullname, name]        


def main():

    parser = argparse.ArgumentParser(description='Investigate Instagram')
    parser.add_argument('username', help='Enter the username')
    parser.add_argument('-q', '--quiet', help='Quiet mode', default=False)
    args = parser.parse_args()

    print('[*] Searching for the username ...')
    insta = Insta(args.username)
    
    print('[*] Rendering the display image ...')
    data = insta.data()

    print('[.] Fullname:', data[1])
    print('[.] Username:', data[3])
    print('[.] Bio:', data[0])

    print('[.] Image:')
    Image.open(data[3] + ".jpg").show()

    print('[!] Made by - Techcentaur')

if __name__=="__main__":
    main()