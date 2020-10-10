import requests
import git
import os


class Cloner:
    def __init__(self, token, username):
        self.token = token
        self.hed = {'Authorization': 'Bearer ' + self.token}
        self.base_url = "https://gitlab.com/api/v4/"
        self.user_id = 0
        self.username = username

    def get_user_id(self):
        response = requests.get(self.base_url + 'users?username=' + str(self.username), json={}, headers=self.hed)
        self.user_id = response.json()[0]['id']

    def get_project_list(self, user_id=None):
        if user_id is None:
            self.get_user_id()
            user_id = self.user_id

        response = requests.get(self.base_url + 'users/' + str(user_id) + '/projects', json={}, headers=self.hed)
        for repo in response.json():
            print(repo['http_url_to_repo'])
            os.mkdir(repo['name'])
            git.Git(repo['name']).clone(repo['ssh_url_to_repo'])

    def get_groups(self):
        os.mkdir('groups')
        response = requests.get(self.base_url + 'groups', json={}, headers=self.hed)
        print(response.json())
        for group in response.json():

            os.mkdir('groups/' + group['name'])
            repo_response = requests.get(self.base_url + 'groups/' + str(group['id']) + '/projects', json={},
                                         headers=self.hed)
            for repo in repo_response.json():
                try:
                    print(repo['name'])
                    os.mkdir('groups/' + group['name'] + '/' + repo['name'])
                    git.Git('groups/' + group['name'] + '/' + repo['name']).clone(repo['ssh_url_to_repo'])
                except Exception as e:
                    print("================>", repo['name'])


token = ''
your_username = ""
cloner = Cloner(token, your_username)
cloner.get_project_list()
cloner.get_groups()
