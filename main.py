from prometheus_client import start_http_server, Gauge
import os
import git
import time
import yaml

git_repo_dir = "/repos/"

# Create Prometheus metrics
commits_not_pushed = Gauge('git_commits_not_pushed', 'Number of unpushed commits in Git repositories', ['repository'])

def check_unpushed_commits(repo_path):
    try:
        repo = git.Repo(repo_path)
        local_branch = repo.active_branch
        remote_branch = repo.remote().refs[f"{local_branch}"]
        unpushed_commits = list(repo.iter_commits(f"{remote_branch}..{local_branch}"))
        return len(unpushed_commits)
    except Exception as e:
        print(f"Error checking unpushed commits for {repo_path}: {str(e)}")
        return 0

def read_config(config_file):
    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Config file '{config_file}' not found.")
        config = {}

    # Load the default configuration
    default_config_file = "default.yml"
    with open(default_config_file, 'r') as default_file:
        default_config = yaml.safe_load(default_file)

    # Merge the custom configuration with the default configuration
    config = {**default_config, **config}

    return config

def main():
    config_file = "custom.yml"

    # Read the default configuration
    config = read_config(config_file)

    interval_time = config['interval_time']

    # Start the Prometheus HTTP server
    http_port = int(os.environ.get('HTTP_PORT', 8085))
    start_http_server(http_port)

    # Iterate through subdirectories (Git repositories) in the specified directory
    while True:
        for repo_name in os.listdir(git_repo_dir):
            repo_path = os.path.join(git_repo_dir, repo_name)
            if os.path.isdir(repo_path):
                unpushed_commits = check_unpushed_commits(repo_path)
                commits_not_pushed.labels(repository=repo_name).set(unpushed_commits)
        time.sleep(interval_time)

if __name__ == '__main__':
    main()
