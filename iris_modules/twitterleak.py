import cfscrape, requests, json
from iris_modules import emailguess
from bs4 import BeautifulSoup as bs
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
from fake_headers import Headers
from colorama import Fore
from re import findall

def look(target):
    if '@' in target:
        target = target.split('@')[0]
    url = "https://api.twitter.com/graphql/P8ph10GzBbdMqWZxulqCfA/UserByScreenName?variables=%7B%22screen_name%22%3A%22" + target + "%22%2C%22withHighlightedLabel%22%3Atrue%7D"
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,bn;q=0.8",
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        "content-type": "application/json",
        "dnt": "1",
        'origin': 'https://twitter.com',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Mobile Safari/537.36',
        'x-twitter-active-user': 'yes',
        'x-twitter-client-language': 'en'
        }
    resp  = json.loads(requests.get(url, headers=headers).text)
    try:
        if resp["data"]["user"]["id"] in resp:
            pass
    except:
        try:
            err = resp["errors"][0]["message"]
            if "Not found" == err:
                print(f'{Fore.RED}•{Fore.RESET} Username Not Found On Twitter')
            else:
                print(err)
        except:
            print(f'{Fore.RED}•{Fore.RESET} Username Not Found On Twitter')
            
    bio = resp["data"]["user"]["legacy"]["description"]
    followers = resp["data"]["user"]["legacy"]["followers_count"]
    location = resp["data"]["user"]["legacy"]["location"]
    name = resp["data"]["user"]["legacy"]["name"]
    Id = resp["data"]["user"]["id"]
    created = resp["data"]["user"]["legacy"]["created_at"]

    if location == '':
        location = 'Unknown'
    if bio == '':
        bio = 'Unknown'

    print(f'{Fore.GREEN}•{Fore.RESET} Infomation Grabbed')
    print(f'''    {Fore.BLUE}•{Fore.RESET} Username       : {target}
    {Fore.BLUE}•{Fore.RESET} User Identify  : {Id}
    {Fore.BLUE}•{Fore.RESET} Full Name      : {name}
    {Fore.BLUE}•{Fore.RESET} Followers      : {followers}
    {Fore.BLUE}•{Fore.RESET} Location       : {location}
    {Fore.BLUE}•{Fore.RESET} Account Bio    : {bio}
    
    {Fore.BLUE}•{Fore.RESET} Active Since   : {created}
''')

def run(account):
    look(account)
    class CustomAdapter(HTTPAdapter):
        def init_poolmanager(self, *args, **kwargs):
            ctx = create_urllib3_context()
            super(CustomAdapter, self).init_poolmanager(
                *args, ssl_context=ctx, **kwargs
            )
    try:
        url = 'https://twitter.com/account/begin_password_reset'
        header = Headers(browser='chrome', os='win', headers=True)
        scraper = cfscrape.create_scraper()

        scraper.mount('https://', CustomAdapter())
        req = scraper.get(url, headers=header.generate())
        soup = bs(req.text, 'html.parser')
        authenticity_token = soup.input.get('value')
        data = {'authenticity_token': authenticity_token, 'account_identifier': account}
        cookies = req.cookies
        response = scraper.post(url, cookies=cookies, data=data, headers=header.generate())
        soup2 = bs(response.text, 'html.parser')

        try:
            if (
                soup2.find('div', attrs={'class': 'is-errored'}).text
                == 'Please try again later.'
            ):
                return f'{Fore.YELLOW}•{Fore.RESET} Rate Limit'
        except:
            pass

        try:
            info = soup2.find('ul', attrs={'class': 'Form-radioList'}).findAll('strong')
        except:
            return 'Not email or phone'

        try:
            phone = int(info[0].text)
            email = str(info[1].text)
        except:
            email = str(info[0].text)
            phone = 'None'

        print(f'''
    {Fore.BLUE}•{Fore.RESET} Phone Number   : {phone}
    {Fore.BLUE}•{Fore.RESET} Email Address  : {email}
    ''')

    except Exception:
        print(f'{Fore.RED}•{Fore.RESET} Failed To Extract Email : Rate Limit')
