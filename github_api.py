import requests
import json
import time
import socket

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


def get_organization_repo_ids(base_url, organization_name):
	url = base_url + ('orgs/{0}/repos').format(organization_name)
	response_data = get_json_response(url)
	return [repo['id'] for repo in response_data]


def get_last_url_of_paginated(url):
	response = requests.head(url)
	last_link = response.links.get('last')

	if not last_link: # response.links will be empty dict if only one page, so we manually return url of page 1
		return url + '&page=1'
	return response.links['last']['url']


# creates a generator that yields one page of results at a time
def generate_repo_pull_requests(base_url, repo_id):
	url = base_url + ('repositories/{0}/pulls?state=all').format(repo_id)
	last_url = get_last_url_of_paginated(url)
	page_number = 1

	while True:
		page_url = base_url + ('repositories/{0}/pulls?state=all&page={1}').format(repo_id, page_number)
		print("working on ", page_url)
		yield get_json_response(page_url)
		page_number += 1

		if page_url == last_url:
			return


# returns a list of ALL results
def get_all_repo_pull_requests(base_url, repo_id):
	all_pulls = []
	for page_of_pulls in generate_repo_pull_requests(base_url, repo_id):
		all_pulls.extend(page_of_pulls)
	return all_pulls
