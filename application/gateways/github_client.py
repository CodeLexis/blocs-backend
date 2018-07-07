from github import Github


def create_client(username, password):
    return Github(username, password)


def get_user_repositories(client):
    for repo in client.get_user().get_repos():
        print(repo.name)


if __name__ == '__main__':
    g = create_client('CodeLexis', 'MY_PASSWORD')
    get_user_repositories(g)
