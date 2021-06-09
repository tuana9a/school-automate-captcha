import requests


def ask_worker_address(url, data):
    try:
        response = requests.post(url, data)
        return response
    except:
        print(' * thread: ask master failed')
        return 'Err: ask master failed'
