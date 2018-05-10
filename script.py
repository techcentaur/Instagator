import requests
import json
import argparse
import urllib.request
from PIL import Image

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
    
    
            return [bio, fullname, name, image]        

def main():

    parser = argparse.ArgumentParser(description='Instagator: Get Display Pic In High Quality')
    parser.add_argument('username', help='Enter the username')
    parser.add_argument('-q', '--quiet', help='Quiet mode', default=False, action="store_true")
    args = parser.parse_args()

    if not args.quiet:
        print('[*] Searching for the username ...')
    insta = Insta(args.username)
    data = insta.data()
    
    if not args.quiet:
        print('[*] Rendering the display image ...')

    urllib.request.urlretrieve(data[3], data[2] + ".jpg")

    if not args.quiet:
        print('[.] Fullname:', data[1])
        print('[.] Username:', data[2])
        print('[.] Bio:', data[0])

    if not args.quiet:
        print('[.] Image:')
    
    Image.open(data[2] + ".jpg").show()

    if not args.quiet:
        print('[!] Made by - Techcentaur')

if __name__=="__main__":
    main()