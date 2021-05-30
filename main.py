import flaskr
import yaml
import time
import threading
import requests
import json

with open('./config/server.yml') as f:
    config_server = yaml.load(f, Loader=yaml.FullLoader)

stop_flag = 0


class AskMasterThread(threading.Thread):
    def askWorkerAddress(self, url, data):
        try:
            response = requests.post(url, data)
        except:
            global stop_flag
            stop_flag = 1
            print(' * thread: ask master failed')

    def run(self):
        print(' * thread: start ask master')
        while not stop_flag:
            url = config_server['master-address'] + \
                '/api/worker/ask/worker-address'
            data = json.dumps({
                'from':  {
                    'name': 'assistant-school-automate-captcha',
                    'address': config_server['address']
                },
                'asks': ['assistant-school-automate-captcha']
            })
            # print(data)
            self.askWorkerAddress(url, data)
            time.sleep(10)
        print(' * thread: stop ask master')


thread = AskMasterThread()
thread.start()

app = flaskr.create_app()
print(' * listen: ' + config_server['address'])
app.run(host='0.0.0.0', port=config_server['port'])
