import requests
import json
import time


# my wifi can sometimes cut off and back on, would hate to lose progress due to that
def wait_until_wifi_is_connected():
	while True:
		try:
			host = socket.gethostbyname('www.google.com')
			s = socket.create_connection((host, 80), 2)
			return
		except:
			time.sleep(30)
	

def get_json_response(url):
	wait_until_wifi_is_connected()
	response = requests.get(url, headers={'User-Agent': 'alabavery'})
	
	if response.headers.get('status') == '403 Forbidden':
		print("Rate limit exceeded... waiting one hour :(")
		time.sleep(3600) # Wait 3600 seconds (one hour) before making request again
		return get_json_response(url)

	response.raise_for_status()
	return json.loads(response.text)


def get_organization_repo_names(base_url, organization_name):
	url = base_url + ('orgs/{0}/repos').format(organization_name)
	response_data = get_json_response(url)
	return [repo['name'] for repo in response_data]


def get_last_url_of_paginated(url):
	response = requests.head(url)
	last_link = response.links.get('last')

	if not last_link: # response.links will be empty dict if only one page, so we manually return url of page 1
		return url + '&page=1'
	return response.links['last']['url']


# creates a generator that yields one page of results at a time
def generate_repo_pull_requests(base_url, owner_name, repo_name):
	url = base_url + ('repos/{0}/{1}/pulls?state=all').format(owner_name, repo_name)
	last_url = get_last_url_of_paginated(url)
	page_number = 1

	while True:
		page_url = base_url + ('repos/{0}/{1}/pulls?state=all&page={2}').format(owner_name, repo_name, page_number)
		yield get_json_response(page_url)
		page_number += 1

		if page_url == last_url:
			return


# returns a list of ALL results
def get_all_repo_pull_requests(base_url, owner_name, repo_name):
	all_pulls = []
	for page_of_pulls in generate_repo_pull_requests(base_url, owner_name, repo_name):
		all_pulls.extend(page_of_pulls)
	return all_pulls
