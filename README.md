# Instagator
Sneaking people on Instagram.

## Usage

- Run `pip3 install -r requirements.txt` to install modules.
- Run `python3 app.py -h` for help.

#### Help Usage

```console
gavy42@jarvis:~/Instagator$ python3 app.py -h
usage: app.py [-h] [-t] [-c] (-p | -f) username

Instagator : Investigate people on Instagram

positional arguments:
  username          User to be searched

optional arguments:
  -h, --help        show this help message and exit
  -t, --tagged      Include people who are tagged in photos (default=True)
  -c, --commentors  Include people who have commented on photos
                    (default=False)
  -p, --print       Print the output (default)
  -f, --file        Save in file in JSON format
```
#### Format

- User info shall be printed in the format for my username, i.e., 'ank.it42':
	 ```json
		{
		    "id": "3429974417",
		    "username": "ank.it42",
		    "full_name": "Ankit Solanki \u26a1",
		    "biography": "Existentialist | INTP | IITDelhi-CS&E",
		    "following": {
		        "count": 256
		    },
		    "followers": {
		        "count": 1325
		    },
		    "is_private": false,
		    "external_url": null,
		    "profile_pic_url_hd": "https://instagram.fdel1-3.fna.fbcdn.net/vp/53362075b376150e63193b2e7e949410/5B8E9CAD/t51.2885-19/s320x320/30077638_416573142146336_6519968261809897472_n.jpg",
		    "platform": "web"
		}

	 ```
- Format for a post of an username:
	 ```json
			{
				"url": "https://www.instagram.com/p/BjDX9nJnI5Q",
				"is_video": "False", 
				"caption": {"text": "Absence."}
			}
	```
#### Functions Usage

- `userpage_scraper(<username>)` : Scrapes user json data from instagram response
- `rootuser_info(<output of userpage_scraper | userinfodict>)` : Returns user basic information in a dictionary.
- `user_images_url(<userinfodict>)` : Returns all posts information in dictionary with keys as is_video, url, and caption.
- `crawling_images_url(<userinfodict>, [args.print | args.file], args.commentors, <args.tagged>)` : Returns username list of all people in comments and tags.

- Static methods
	- `json_url(<url>)` : Returns json data of response from requesting an url.
	- `pretty_print(<userinfodict>, do_print)` : Prints or saves in a file, json data mainpulation functions.

## Repository Naming Ideas

- Sneastagram : Sneaking Instagram Accounts.
- Crawlins : Crawl through Insta Accouts.
