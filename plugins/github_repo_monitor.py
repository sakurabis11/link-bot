# "if anyone forks or contribute your repo bot will send message to your required support group"

from pyrogram import Client
from github import Github
from info import GITHUB_TOKEN, REPO_URL, SUPPORT_GROUP_ID

# Initialize Github and Telegram clients
github = Github(GITHUB_TOKEN)
repo = github.get_repo(REPO_URL)


def check_activity():
  last_fork_count = 0
  last_commit_sha = repo.get_commits()[0].sha
  while True:
    current_fork_count = repo.get_forks_count()
    new_commits = repo.get_commits(since=last_commit_sha)
    if current_fork_count > last_fork_count:
      new_forks = current_fork_count - last_fork_count
      for fork in repo.get_forks()[:new_forks]:
        # Modified message to include fork URL instead of file link
        message = f"✨ New fork by [@{fork.owner.login}]({fork.url}) on {REPO_URL}!"
        Client.send_message(SUPPORT_GROUP_ID, message)
    if new_commits:
      committer = new_commits[0].commit.author.name
      # Modified message to include commit URL instead of file link
      message = f"️ {committer} contributed to {REPO_URL}! See commit details here: {new_commits[0].url}"
      Client.send_message(SUPPORT_GROUP_ID, message)
    last_fork_count = current_fork_count
    last_commit_sha = new_commits[0].sha if new_commits else last_commit_sha
    time.sleep(60)

# Start the monitoring thread
activity_thread = threading.Thread(target=check_activity)
activity_thread.start()

