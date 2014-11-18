import hashlib
import urllib2
import json

from datetime import datetime, timedelta


class Smython:
    """
    A python tool to make client API requests to the Smite API
    Attributes:
        dev_id: Your private developer ID supplied by Hi-rez. Can be requested here: https://fs12.formsite.com/HiRez/form48/secure_index.html
        auth_key: Your authorization key
        response_format: Your preferred response format. Options are 'xml' or 'json'
    """

    def __init__(self, dev_id, auth_key, response_format='json'):
        self.dev_id = dev_id
        self.auth_key = auth_key
        self.response_format = response_format
        self.session = None
        self.base_url = 'http://api.smitegame.com/smiteapi.svc/'

    def make_request(self, methodname, parameter=None):
        if not self.session or not self._test_session():
            self.session = self._create_session()

        signature = self._create_md5_hash(methodname)
        timestamp = self._create_now_timestamp()
        session = self.session.get("session_id", None)

        url = self.base_url + methodname + self.response_format + "/" + self.dev_id + "/" + signature + "/" + session + "/" + timestamp
        if parameter:
            url = url + "/" + parameter
        return json.loads(urllib2.urlopen(url).read())

    def _create_session(self):
        signature = self._create_md5_hash('createsession')
        url = self.base_url + "createsessionjson/" + self.dev_id + "/%s/" % signature + self._create_now_timestamp()
        return json.loads(urllib2.urlopen(url).read())

    def _create_now_timestamp(self):
        dt = datetime.utcnow()
        return dt.strftime("%Y%m%d%H%M%S")

    def _create_md5_hash(self, methodname):
        now = self._create_now_timestamp()
        return hashlib.md5(self.dev_id + methodname + self.auth_key + now).hexdigest()

    def _test_session(self, session):
        methodname = 'testsession'
        timestamp = self._create_now_timestamp()
        signature = self._create_md5_hash(methodname)
        url = self.base_url + methodname + self.response_format + "/" + self.dev_id + "/" + signature + "/" + session.get("session_id") + "/" + timestamp
        return "successful" in urllib2.urlopen(url).read()

    def get_player(self, player_name):
        return self.make_request('getplayer', player_name)





