import hashlib
import urllib2
import json
from datetime import datetime


class Smython:
    def __init__(self, dev_id, auth_key, response_format='json'):
        self.dev_id = dev_id
        self.auth_key = auth_key
        self.response_format = response_format
        self.base_url = 'http://api.smitegame.com/smiteapi.svc/'

    def create_session(self):
        signature = self._create_md5_hash('createsession')
        url = self.base_url + "createsessionjson/" + self.dev_id + "/%s/" % signature + self._create_now_timestamp()
        return json.loads(urllib2.urlopen(url).read())


    def _create_now_timestamp(self):
        dt = datetime.utcnow()
        return dt.strftime("%Y%m%d%H%M%S")

    def _create_md5_hash(self, methodname):
        now = self._create_now_timestamp()
        return hashlib.md5(self.dev_id + methodname + self.auth_key + now).hexdigest()