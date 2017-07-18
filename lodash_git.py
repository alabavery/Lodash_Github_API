import requests
import json
import pprint
from datetime import datetime

def get_lodash_pull_requests(repository_name):
	url = 'https://api.github.com/repos/lodash/{0}/pulls?state=all'.format(repository_name)
	response_text = requests.get(url).text
	return json.loads(response_text)


# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(get_lodash_pull_requests('lodash'))


def timestamp_to_datetime(timestamp_string):
	return datetime.strptime(timestamp_string,"%Y-%m-%dT%H:%M:%SZ")


dt = timestamp_to_datetime("2011-01-26T19:01:12Z")