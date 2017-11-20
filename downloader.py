import requests
from bs4 import BeautifulSoup

class DictDownloader:

    def __init__(self, account_data):
        self.session = requests.Session()
        self.account_data = account_data
        # try to login, max 3 times
        succs = False
        trial = 0
        while not succs and trial < 3:
            succs = self.login()
            trial += 1
        if not succs:
            raise Exception("Error: Could not login to dict.cc")

    def login(self):
        login_URL = "https://secure.dict.cc/users/urc_logn.php?next=goto%3Ahttp%3A%2F%2Fwww.dict.cc%2F"
        payload = dict()
        payload["hinz"] = self.account_data["user"]
        payload["kunz"] = self.account_data["pass"]
        payload["rmotc"] = "on"
        p = self.session.post(login_URL, data=payload)
        return p.text.find("Login successful") # True, if login successful

    def download_list(self, remote):
        with self.session as s:
            g = s.get(remote)
            if g.status_code != 200:
                raise Exception("Error while downloading {}.".format(remote))
            return g.content.decode("utf-8")

    def find_all_lists(self):
        with self.session as s:
            g = s.get("http://my.dict.cc")
            if g.status_code != 200:
                raise Exception("Error while reading lists.")
        soup = BeautifulSoup(g.text())
        soup.main.table.tr.find("td")
