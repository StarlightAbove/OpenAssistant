import requests
from services.base import BaseConnector
from db.queries import save_snapshot, get_yesterday_snapshot


class GitHubConnector(BaseConnector):

    def __init__(self, token: str, username: str):
        self.token = token
        self.username = username
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        }

    def fetch(self) -> dict:
        today_data = {
            "open_prs": self._get_open_prs(),
            "review_requested": self._get_review_requests(),
            "open_issues_assigned": self._get_assigned_issues(),
            "unread_notifications": self._get_notifications(),
            "recent_commits": self._get_recent_commits(),  
        }

        yesterday_data = get_yesterday_snapshot("github")
        save_snapshot("github", today_data)

        return {"today": today_data, "yesterday": yesterday_data}

    def _get_open_prs(self) -> list:
        resp = requests.get(
            "https://api.github.com/search/issues",
            headers=self.headers,
            params={"q": f"is:pr is:open author:{self.username}"},
        )
        resp.raise_for_status()
        return [
            {"title": pr["title"], "repo": pr["repository_url"].split("/")[-1], "url": pr["html_url"]}
            for pr in resp.json().get("items", [])
        ]

    def _get_review_requests(self) -> list:
        resp = requests.get(
            "https://api.github.com/search/issues",
            headers=self.headers,
            params={"q": f"is:pr is:open review-requested:{self.username}"},
        )
        resp.raise_for_status()
        return [
            {"title": pr["title"], "repo": pr["repository_url"].split("/")[-1], "url": pr["html_url"]}
            for pr in resp.json().get("items", [])
        ]

    def _get_assigned_issues(self) -> list:
        resp = requests.get(
            "https://api.github.com/search/issues",
            headers=self.headers,
            params={"q": f"is:issue is:open assignee:{self.username}"},
        )
        resp.raise_for_status()
        return [
            {"title": issue["title"], "repo": issue["repository_url"].split("/")[-1], "url": issue["html_url"]}
            for issue in resp.json().get("items", [])
        ]

    def _get_notifications(self) -> list:
        resp = requests.get(
            "https://api.github.com/notifications",
            headers=self.headers,
        )
        resp.raise_for_status()
        return [
            {"title": n["subject"]["title"], "repo": n["repository"]["full_name"], "reason": n["reason"]}
            for n in resp.json()
        ]
    
    def _get_recent_commits(self, days: int = 1, max_repos: int = 5) -> list:
        repos_resp = requests.get(
            f"https://api.github.com/users/{self.username}/repos",
            headers=self.headers,
            params={"sort": "pushed", "direction": "desc", "per_page": max_repos},
        )
        repos_resp.raise_for_status()

        result = []
        for repo in repos_resp.json():
            commits_resp = requests.get(
                f"https://api.github.com/repos/{self.username}/{repo['name']}/commits",
                headers=self.headers,
                params={"author": self.username, "since": since, "per_page": 10},
            )
        commits_resp.raise_for_status()
        commits = commits_resp.json()

        if commits:
            result.append({
                "repo": repo["name"],
                "description": repo.get("description"),
                "commits": [
                    {
                        "message": c["commit"]["message"],
                        "sha": c["sha"][:7],
                        "date": c["commit"]["author"]["date"],
                        "url": c["html_url"],
                    }
                    for c in commits
                ],
            })

        return result