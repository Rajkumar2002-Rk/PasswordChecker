import requests
import hashlib
import sys


def req_api_data(query_char): #getting password api 
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200: 
        raise RuntimeError(f'Error Fecting: {res.status_code}, Check the API')
    return res


def get_password_leaks_count(hashes, hash_to_check): # Checking password if ti exists in API reponse
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def api_passcheck(password):
    sha1pass = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1pass[:5], sha1pass[5:]
    response = req_api_data(first5_char)
    return get_password_leaks_count(response, tail)


def main(args):
    for password in args:
        count = api_passcheck(password)
        if count:
            print(f'{password} was found {count} times... you should change the password!')
        else:
            print(f'{password} was NOT found! your\'s is strong carry on buddy!')
    return 'done!'


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
