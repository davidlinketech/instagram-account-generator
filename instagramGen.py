import requests
import threading
import names
from secrets import randbelow
import random
import time
import json

#generate random password
def gen_ran_passw():
    letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    chars = ["!","?","=","&","$","#"]
    random_password = ""
    for x in range(17):
        value = randbelow(3)
        if value == 0:
            if randbelow(2) == 0:
                random_password += letters[randbelow(len(letters))].upper()
            else:
                random_password += letters[randbelow(len(letters))]
        elif value == 1:
            random_password += chars[randbelow(len(chars))]
        elif value == 2:
            random_password += str(randbelow(10))
    validcheck = False
    for letter in letters:
        if letter.upper() in random_password:
            validcheck = True
            break
    if validcheck == False:
        random_password += letters[randbelow(len(letters))].upper()
    else:
        validcheck = False
    for letter in letters:
        if letter in random_password:
            validcheck = True
            break
    if validcheck == False:
        random_password += letters[randbelow(len(letters))]
    else:
        validcheck = False
    for char in chars:
        if char in random_password:
            validcheck = True
            break
    if validcheck == False:
        random_password += chars[randbelow(len(chars))]
    else:
        validcheck = False
    for num in ["0","1","2","3","4","5","6","7","8","9"]:
        if num in random_password:
            validcheck = True
            break
    if validcheck == False:
        random_password += str(randbelow(10))
    
    return random_password

#opening proxyfile and deleting used proxy
def get_session_proxy():
    with open('files/proxies.txt', 'r') as proxy_file:
        read_proxies = proxy_file.read()
    if len(read_proxies) < 2:
        return
    proxies = read_proxies.splitlines()
    if len(proxies[0]) > 1:
        proxy = proxies[0]
        del proxies[0]
        with open('files/proxies.txt', 'w') as new_proxy_file:
            new_proxy_file.write('\n'.join(proxies))
    
    proxy_info = proxy.split(':')
    final_proxies = {
        "http": f"http://{proxy_info[2]}:{proxy_info[3]}@{proxy_info[0]}:{proxy_info[1]}",
        "https": f"http://{proxy_info[2]}:{proxy_info[3]}@{proxy_info[0]}:{proxy_info[1]}"
    }
    return final_proxies

#generates random client id
def gen_client_id():
    letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    ran4letters = ""
    for a in range(4):
        if random.randint(0,1) == 0:
            ran4letters += letters[random.randrange(0,len(letters))]
        else:
            ran4letters += letters[random.randrange(0,len(letters))].upper()
    ran15chars = ""
    for b in range(15):
        if random.randint(0,1) == 0:
            if random.randint(0,1) == 0:
                ran15chars += letters[random.randrange(0,len(letters))]
            else:
                ran15chars += letters[random.randrange(0,len(letters))].upper()
        else:
            ran15chars += str(random.randint(0,9))

    client_id = f'Yf{ran4letters}ALAAG{letters[random.randrange(0,len(letters))].upper() + ran15chars}'
    return client_id

def instagen(thread_id, smsapi=None, country_code=None, webhook=None):
    if not smsapi or not country_code or smsapi == "YOUR_SMS_API_KEY":
        print(f'[error in task{thread_id}] check if you specified all information correctly')
        return

    #creating session + appending proxies to session
    s = requests.Session()
    s.proxies = get_session_proxy()

    #getting device_id and csrf token
    while True:
        try:
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
            }
            res = s.get('https://www.instagram.com/accounts/emailsignup/', headers=headers)
            device_id = res.text.split('"device_id":"')[1].split('"')[0]
            headers = {
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9',
                'referer': 'https://www.instagram.com/accounts/emailsignup/',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
                'x-asbd-id': '198387',
                'x-ig-app-id': '936619743392459',
                'x-ig-www-claim': '0',
                'x-requested-with': 'XMLHttpRequest',
                'x-web-device-id': device_id
            }
            res = s.get('https://www.instagram.com/data/shared_data/', headers=headers)
            csrf = res.text.split('csrf_token":"')[1].split('"')[0]
            break
        except:
            print(f'[error in task{thread_id}] couldnt get device_id...getting new proxy and session')
            s = requests.Session()
            s.proxies = get_session_proxy()
            time.sleep(2)

    time.sleep(0.2)

    password = gen_ran_passw() 
    client_id = gen_client_id()
    name = names.get_full_name()
    month = str(random.randint(1,12))
    day = str(random.randint(10,25))
    year = str(random.randint(1960,2000))
    username = name.split()[0] + str(random.randint(111,999)) + '_' + name.split()[1]
    
    #creation flow:
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.instagram.com',
        'referer': 'https://www.instagram.com/accounts/emailsignup/',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
        'x-asbd-id': '198387',
        'x-csrftoken': csrf,
        'x-ig-app-id': '936619743392459',
        'x-ig-www-claim': '0',
        'x-instagram-ajax': 'c35f58698901',
        'x-requested-with': 'XMLHttpRequest'
    }
    
    #getting phonenumber and sms code

    for x in range(3):
        if country_code == "DE":
            res = s.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key={smsapi}&action=getNumber&service=ig&country=43')
        elif country_code == "IT":
            res = s.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key={smsapi}&action=getNumber&service=ig&country=86')
        elif country_code == "ES":
            res = s.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key={smsapi}&action=getNumber&service=ig&country=56')
        elif country_code == "FR":
            res = s.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key={smsapi}&action=getNumber&service=ig&country=78')
        try:
            phonenum = res.text.split(':')[2]
            phone_id = res.text.split(':')[1]
        except:
            print(f'[error in task{thread_id}] no numbers/no balance')
            return
        #making first creation attempt
        while True:
            body = {
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
                'phone_number': phonenum,
                'client_id': client_id,
                'username': username,
                'first_name': name,
                'seamless_login_enabled': '1',
                'opt_into_one_tap': 'false'
            }
            res = s.post('https://www.instagram.com/accounts/web_create_ajax/attempt/', headers=headers, data=body)
            #checking for error
            try:
                if not res.json()["status"]:
                    print(f'[error in task{thread_id}] acc creation failed')
                    return
            except:
                print(f'[error in task{thread_id}] acc creation failed')
                return
            #checking if username is not available
            if "username" in res.json()["errors"]:
                print(f'[error in task{thread_id}] username taken...getting new one')
                username = res.json()["username_suggestions"][0]
            break
        time.sleep(0.4)
        #sending sms to phone number
        body = {          
            'client_id': client_id,
            'phone_number': phonenum,
            "phone_id": "",
            "big_blue_token": ""
        } 
        res = s.post('https://www.instagram.com/accounts/send_signup_sms_code_ajax/', headers=headers, data=body)
        print(f'[task{thread_id}] getting sms code')
        #receiving sms code
        for k in range(15):
            res = requests.get(f'https://api.sms-activate.org/stubs/handler_api.php?api_key={smsapi}&action=getStatus&id={phone_id}')
            try:
                sms_code = res.text.split(':')[1]
                print(f'[task{thread_id}] got sms code')
                break
            except:
                time.sleep(3)
            sms_code = False
            time.sleep(3)
        if sms_code:
            #accept sms code on sms-activate
            res = requests.get(f'https://api.sms-activate.org/stubs/handler_api.php?api_key={smsapi}&action=setStatus&status=6&id={phone_id}')
            #validating sms code
            body = {
                'client_id': client_id,
                'phone_number': phonenum,
                'sms_code': sms_code
            }
            res = s.post('https://www.instagram.com/accounts/validate_signup_sms_code_ajax/', headers=headers, data=body)
            break
        else:
            #cancel number
            print(f'[error in task{thread_id}] couldnt get sms code...getting new phone number')
            requests.get(f'https://api.sms-activate.org/stubs/handler_api.php?api_key={smsapi}&action=setStatus&status=8&id={phone_id}')
            time.sleep(1)
    
    body = {
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
        'phone_number': phonenum,
        'client_id': client_id,
        'username': username,
        'first_name': name,
        'sms_code': sms_code,
        'seamless_login_enabled': '1'
    }
    res = s.post('https://www.instagram.com/accounts/web_create_ajax/attempt/', headers=headers, data=body)
    time.sleep(0.5)

    #final request
    body["month"] = month
    body["day"] = day
    body["year"] = year
    body["tos_version"] = 'eu'
    res = s.post('https://www.instagram.com/accounts/web_create_ajax/', headers=headers, data=body)
    if res.status_code == 200:
        print(f'[success in task{thread_id}] successfully created account')

    #sleeping then checking if acc got clipped
    print(f'[task{thread_id}] sleeping 50 seconds then checking if acc got clipped')
    time.sleep(30)                      #you can play with this delay and make it lower

    #headers for the last requests
    def genHeaders(csrf, claim):
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-length': '0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.instagram.com',
            'referer': 'https://www.instagram.com/',
            'sec-ch-ua':'" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
            'x-asbd-id': '198387',
            'x-csrftoken': csrf,
            'x-ig-app-id': '936619743392459',
            'x-ig-www-claim': claim,
            'x-instagram-ajax': '6ab3c34e0025',
            'x-requested-with': 'XMLHttpRequest'
        }
        return headers

    for x in range(5):
        #getting first csrf token
        res = s.get('https://www.instagram.com/accounts/login/')
        csrf = res.text.split('csrf_token":"')[1].split('"')[0]
        insta_claim = "0"

        #payload for login
        payload = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }

        #trying to login
        headers = genHeaders(csrf, insta_claim)
        clipurl = False
        res = s.post('https://www.instagram.com/accounts/login/ajax/', headers=headers, data=payload)
        try:
            if res.json()["authenticated"]:
                #successfull logged in
                print(f'[task{thread_id}] logged in')
                insta_claim = res.headers["x-ig-set-www-claim"]
                csrf = s.cookies.get_dict()["csrftoken"]
                headers = genHeaders(csrf, insta_claim)
                time.sleep(1)
                res = s.post(f'https://www.instagram.com/web/friendships/6860189/follow/', headers=headers, data={})
                try:
                    #account got clipped
                    if res.json()["message"]:
                        print(f'[error in task{thread_id}] acc got clipped')
                        clipurl = res.json()["checkpoint_url"]
                        with open('files/clipped_accounts.txt', 'a') as acc_file:
                            acc_file.write(f'{username}:{password}\n')
                except:
                    #account is not clipped!
                    print(f'[success in task{thread_id}] acc not clipped')
                    with open('files/working_accounts.txt', 'a') as acc_file:
                        acc_file.write(f'{username}:{password}\n')
                    #sending message to discord webhook if specified
                    if webhook:
                        webhook_body = {
                            "content": None,
                            "embeds": [
                                {
                                    "title": "Successfully Instragram Account Created",
                                    "color": 720640,
                                    "fields": [
                                        {
                                            "name": "username",
                                            "value": f"||{username}||",
                                            "inline": True
                                        },
                                        {
                                            "name": "Password",
                                            "value": f"||{password}||",
                                            "inline": True
                                        }
                                    ],
                                    "thumbnail": {
                                        "url": "https://cdn.discordapp.com/attachments/938484202704355328/938900345080414278/Instagram-logo.png"
                                    }
                                }
                            ],
                            "username": "Instagram Gen",
                            "avatar_url": "https://cdn.discordapp.com/attachments/938484202704355328/938900345080414278/Instagram-logo.png"
                        }
                        res = requests.post(webhook, data=json.dumps(webhook_body), headers={"Content-Type":"application/json"})
                break
            else:
                #the login failed, it will now get a new session and try it again
                #change the retry delay to what you like
                print(f'[error in task{thread_id}] login failed')
                print(f'[task{thread_id}] switching proxies, creating new session and retrying in 50 seconds again')
                s = requests.Session()
                s.proxies = get_session_proxy()
                time.sleep(50)
        except Exception as e:
            #the login failed, it will now get a new session and try it again
            #change the retry delay to what you like
            print(f'[error in task{thread_id}] login failed')
            print(f'[task{thread_id}] switching proxies, creating new session and retrying in 50 seconds again')
            s = requests.Session()
            s.proxies = get_session_proxy()
            time.sleep(50)
with open('files/proxies.txt', 'r') as proxy_file:
    read_proxies = proxy_file.read()
if len(read_proxies) < 2:
    print('[warning] empty proxy-file...proceding without proxy')
print('how many accounts to gen?')
ts = int(input('-->'))
threadlist = []
for i in range(ts):
    #change the following params
    t = threading.Thread(target=lambda h=i:instagen(h, smsapi="YOUR_SMS_API_KEY", country_code="DE", webhook="YOUR_DC_WEBHOOK"))
    threadlist.append(t)
    print(f'[starting thread {str(i)}]')
    t.start()
    time.sleep(0.5)
