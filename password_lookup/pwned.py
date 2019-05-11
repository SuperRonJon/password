import requests
import hashlib
import sys


def hash_split(password):
    hashed = hashlib.sha1(password.encode()).hexdigest().upper()
    print(f'Hashed: {hashed.lower()}')
    return hashed[:5], hashed[5:]


def get_matches(search_range):
    url = f'https://api.pwnedpasswords.com/range/{search_range}'
    results_text = requests.get(url).text
    return results_text.split('\r\n')


def password_count(results, real_suffix):
    for result in results:
        suffix, count = result.split(':')
        if suffix == real_suffix:
            return count

    return None


if __name__ == '__main__':
    assert len(sys.argv) == 2, "Must have 1 argument"
    password = sys.argv[1]

    search_range, my_suffix = hash_split(password)
    results = get_matches(search_range)
    count = password_count(results, my_suffix)
    if count:
        print(f'Password found {count} times.')
    else:
        print('Password not found!')
