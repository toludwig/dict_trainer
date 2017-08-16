import requests

class DictDownloader:

    def __init__(self, account_data):
        self.session = requests.Session()
        self.account_data = account_data
        self.login()

    def login(self):
        # TODO login to dict.cc
        login_URL = "https://secure.dict.cc/users/urc_logn.php?next=goto%3Ahttp%3A%2F%2Fwww.dict.cc%2F"
        payload = dict()
        payload["hinz"] = self.account_data["user"]
        payload["kunz"] = self.account_data["pass"]
        payload["rmotc"] = "on"
        p = self.session.post(login_URL, data=payload)
        print(p)

    def download_list(self, remote):
        with self.session as s:
            g = s.get(remote)
            if g.status_code != 200:
                raise Exception("Error while downloading {}.".format(remote))
            return g.content.decode("utf-8")
