import requests
from connectors.base import BaseConnector
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