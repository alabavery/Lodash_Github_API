import pprint
import github_api as gapi

BASE_URL = 'https://api.github.com/'

lodash_repo_names = gapi.get_organization_repo_names(BASE_URL, 'lodash')
lodash_pull_request_data = [gapi.get_repo_pull_request_data(BASE_URL, 'lodash', repo) for repo in lodash_repo_names]

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(lodash_pull_request_data[0]) # print a lodash repo as an example