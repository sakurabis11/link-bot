import pyrogram
from pyrogram import filters, Client
import requests


def get_repository_info(repository):
    repo_name = repository["full_name"]
    repo_description = repository["description"]
    repo_link = repository["html_url"]
    repo_stars = repository["stargazers_count"]
    repo_commits_url = repository["commits_url"]

    # Try parsing the commits URL and fetching commit count
    try:
        commit_response = requests.get(repo_commits_url.replace("{/sha}", ""))
        if commit_response.status_code == 200:
            commit_data = commit_response.json()
            commits_count = len(commit_data) if isinstance(commit_data, list) else 0
        else:
            commits_count = 0
    except (ValueError, requests.exceptions.RequestException):
        commits_count = 0

    return (
        f"Repository: {repo_name}\n"
        f"Description: {repo_description}\n"
        f"Link: {repo_link}\n"
        f"Stars: {repo_stars}\n"
        f"Commits: {commits_count}\n"
    )

@Client.on_message(filters.command("github"))
async def search_repos(client, message):
    try:
        search_query = message.text.split(maxsplit=1)[1]
        response = requests.get(f"https://api.github.com/search/repositories?q={search_query}")
        response.raise_for_status()  # Check for HTTP errors

        repositories = response.json().get("items", [])

        if repositories:
            message.reply("Found the following repositories on GitHub:")
            for repository in repositories:
                repo_info = get_repository_info(repository)
                message.reply(repo_info)
        else:
            message.reply("No repositories found for the given query.")

    except Exception as e:
        message.reply(f"An error occurred: {str(e)}")
