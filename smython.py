import hashlib
import urllib2
import json

from datetime import datetime


class Smython:
    """
    A python tool to make client API requests to the Smite API
    Attributes:
        dev_id: Your private developer ID supplied by Hi-rez. Can be requested here: https://fs12.formsite.com/HiRez/form48/secure_index.html
        auth_key: Your authorization key
        response_format: Your preferred response format. Options are 'xml' or 'json' TODO make this a constant since this only works for json
        lang: the language code needed by some queries, defaults to english.
    """

    def __init__(self, dev_id, auth_key, response_format='json', lang='1'):
        self.dev_id = dev_id
        self.auth_key = auth_key
        self.response_format = response_format
        self.lang = lang
        self.session = None
        self.base_url = 'http://api.smitegame.com/smiteapi.svc/'

    def make_request(self, methodname, parameters=None):
        if not self.session or not self._test_session(self.session):
            self.session = self._create_session()

        url = self._build_url(methodname, parameters)
        return json.loads(urllib2.urlopen(url).read())

    def _build_url(self, methodname, parameters=None):
        base = self.base_url
        signature = self._create_signature(methodname)
        timestamp = self._create_now_timestamp()
        session_id = self.session.get("session_id")

        path = [methodname + self.response_format, self.dev_id, signature, session_id, timestamp]
        if parameters:
            path = path + parameters
        return base + '/'.join(path)

    def _create_session(self):
        signature = self._create_signature('createsession')
        url = self.base_url + "createsessionjson/" + self.dev_id + "/%s/" % signature + self._create_now_timestamp()
        return json.loads(urllib2.urlopen(url).read())

    def _create_now_timestamp(self):
        dt = datetime.utcnow()
        return dt.strftime("%Y%m%d%H%M%S")

    def _create_signature(self, methodname):
        now = self._create_now_timestamp()
        return hashlib.md5(self.dev_id + methodname + self.auth_key + now).hexdigest()

    def _test_session(self, session):
        methodname = 'testsession'
        timestamp = self._create_now_timestamp()
        signature = self._create_signature(methodname)
        path = "/".join([methodname + self.response_format, self.dev_id, signature, session.get("session_id"), timestamp])
        url = self.base_url + path
        return "successful" in urllib2.urlopen(url).read()

    def get_data_used(self):
        """
        :return : Returns a dictionary of daily usage limits and the stats against those limits
        """
        return self.make_request('getdataused')

    def get_gods(self):
        """
        :return: Returns all smite Gods and their various attributes
        """
        return self.make_request('getgods', self.lang)

    def get_items(self, lang):
        """
        :param lang: The language id that you want results returned in.
        :return: Returns all Smite items and their various attributes
        """
        return self.make_request('getitems', [lang])

    def get_god_recommended_items(self, god_id, lang):
        """
        :param god_id: ID of god you are quering against. Can be found in get_gods return result.
        :param lang: the language id that you want results returned in
        :return: Returns a dictionary of recommended items for a particular god
        """
        return self.make_request('getgodrecommendeditems', [god_id, lang])

    def get_esports_proleague_details(self):
        """
        :return: Returns the matchup information for each matchup of the current eSports pro league session.
        """
        return self.make_request('getesportsproleaguedetails')

    def get_top_matches(self):
        """
        :return: Returns the 50 most watch or most recent recorded matches
        """
        return self.make_request('gettopmatches')

    def get_match_details(self, match_id):
        """
        :param match_id: The id of the match
        :return: Returns a dictionary of the match and it's attributes.
        """
        return self.make_request('getmatchdetails', [match_id])

    def get_team_details(self, clan_id):
        """
        :param clan_id: The id of the clan
        :return: Returns the details of the clan in a python dictionary
        """
        return self.make_request('getteamdetails', [clan_id])

    def get_team_match_history(self, clan_id):
        """
        :param clan_id: The ID of the clan.
        :return: Returns a history of matches from the given clan.
        """
        return self.make_request('getteammatchhistory', [clan_id])

    def get_team_players(self, clan_id):
        """
        :param clan_id: The ID of the clan
        :return: Returns a list of players for the given clan.
        """
        return self.make_request('getteamplayers', [clan_id])

    def search_teams(self, search_team):
        """
        :param search_team: The string search term to search against
        :return: Returns high level information for clan names containing search_team string
        """
        return self.make_request('searchteams', [search_team])

    def get_player(self, player_name):
        """
        :param player_name: the string name of a player
        :return: Returns league and non-league high level data for a given player name
        """
        return self.make_request('getplayer', [player_name])

    def get_friends(self, player):
        """
        :param player: The player name or a player ID
        :return: Returns a list of friends
        """
        return self.make_request('getfriends', [player])

    def get_god_ranks(self, player):
        """
        :param player: The player name or player ID
        :return: Returns the rank and worshippers value for each God the player has played
        """
        return self.make_request('getgodranks', [player])

    def get_match_history(self, player):
        """
        :param player: The player name or player ID
        :return: Returns the recent matches and high level match statistics for a particular player.
        """
        return self.make_request('getmatchhistory', [player])

    def get_queue_stats(self, player, queue):
        """
        :param player: The player name or player ID
        :param queue: The id of the game mode
        :return: Returns match summary statistics for a player and queue
        """
        return self.make_request('getqueuestats', [player, queue])




