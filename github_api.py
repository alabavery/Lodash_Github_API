import requests
import json

def get_json_response(url):
	response = requests.get(url)
	response.raise_for_status()
	return json.loads(response.text)


def get_organization_repo_names(base_url, organization_name):
	url = base_url + ('orgs/{0}/repos').format(organization_name)
	response_data = get_json_response(url)
	return [repo['name'] for repo in response_data]


def get_repo_pull_request_data(base_url, owner_name, repo_name):
	url = base_url + ('repos/{0}/{1}/pulls?state=all').format(owner_name, repo_name)
	return get_json_response(url)


def get_pull_request_by_id(repo_pull_request_data, request_id):
	record_as_list = [record for record in repo_pull_request_data if record['id'] == request_id]
	try:
		return record_as_list[0] # this is a dict
	except IndexError:
		return {} # caller expects dict, so give it to them even though no record
