import urllib.request
import urllib.error
import urllib.parse
import twurl
import json
import ssl

# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def about_user(user_name, URL, key1='users', status='yes', key2='location',\
                                                      status2='no'):
    """
    (str, str, str, str, str, str) -> (dict)
    take six parameters user name, name of human whose friend or followers you
    want know, key1 and key2 this is that you want know about them, status
    if you want input second key and status1 if you want print data
    url - needs for dowload list of some data of human
    return dict with key like first key and names of this human in value
    """
    TWITTER_URL = URl
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': user_name, 'count': '5'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()
    js = json.loads(data)
    print('\n')
    if status2 == 'yes':
        print('Retrieving', url)
        headers = dict(connection.getheaders())
        print('\n')
        print('Remaining', headers['x-rate-limit-remaining'])
        print('\n')
    k = 0
    output_dict = dict()
    if key1 in js:
        for key in js[key1]:
            if status == 'yes':
                if key2 in key:
                    keys = key[key2]
                    try:
                        types = type(output_dict[keys])
                        if type(output_dict[keys]) == list:
                            lst = []
                            for i in output_dict[keys]:
                                lst.append(i)
                            lst.append(output_dict[keys])
                            output_dict[keys] = lst
                    except:
                        output_dict[keys] = key["name"]
                    k += 1
                else:
                    print('second key does not exist')
                    k += 1
            if k == 0:
                return key
        return output_dict
    else:
        print('first key does not exist')


if __name__ == '__main__':
    user_name = input('Enter Twitter Account:')
    while (len(user_name) < 1):
        user_name = input('Enter Twitter Account: ')
    print('If you dont input something program will work without your')
    print('parameters')
    key1 = input('Input first key: ')
    status = input('if you want input second key input yes: ')
    key2 = input('Input second key: ')
    status2 = input('if you want to know all data input yes: ')
    if key2 != '' and status != '' and key1 == '' and status2 == '':
        print(about_user(user_name, TWITTER_URL, key1, status, key2, status2))
    else:
        print(about_user(user_name, TWITTER_URL))
