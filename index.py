import github_api as gapi
import json
import os


def save_as_json_file(file_path, data):
	json_to_save = json.dumps(data)
	file = open(file_path,'w')
	file.write(json_to_save)
	file.close()


BASE_URL = 'https://api.github.com/'
#lodash_repo_ids = gapi.get_organization_repo_names(BASE_URL, 'lodash')
lodash_repo_ids = ['57350423']
base_path = os.path.dirname(os.path.realpath(__file__))

for i, repo in enumerate(lodash_repo_ids):
	file_path = os.path.join(base_path, repo) + '.json'
	
	if not os.path.isfile(file_path): # check if we've already saved this repo (this might not be the first time we've run program)
		pulls = gapi.get_all_repo_pull_requests(BASE_URL, repo)
		save_as_json_file(file_path, pulls)
	print(str(i+1) + " repo(s) down...")