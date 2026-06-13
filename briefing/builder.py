import json
from datetime import date


def build_prompt(snapshots: dict) -> str:
    today = date.today().strftime("%A, %B %d %Y")
    sections = [_header(today)]

    builders = {
        "github":           _github,
        "todoist":          _todoist,
        "gmail":            _gmail,
        "outlook":          _outlook,
        "google_calendar":  _calendar,
        "outlook_calendar": _calendar,
        "slack":            _slack,
        "google_sheets":    _sheets,
        "plaid":            _plaid,
        "geoip":            _geoip,
        "apple_health":     _health,
    }

    for source, builder_fn in builders.items():
        if source in snapshots:
            sections.append(builder_fn(snapshots[source]))

    sections.append(_instructions())
    return "\n\n".join(sections)


# --- Header ---

def _header(today: str) -> str:
    return f"You are preparing a morning briefing for {today}. Below is a structured summary of the user's day and recent activity. Analyze it and produce a prioritized, actionable briefing."


# --- Per-source builders ---

def _github(data: dict) -> str:
    today = data.get("today", {})
    yesterday = data.get("yesterday", {})
    lines = ["## GitHub"]

    prs = today.get("open_prs", [])
    lines.append(f"Open PRs: {len(prs)}")
    for pr in prs:
        lines.append(f"  - [{pr['repo']}] {pr['title']}")

    reviews = today.get("review_requested", [])
    if reviews:
        lines.append(f"Review requested ({len(reviews)}):")
        for r in reviews:
            lines.append(f"  - [{r['repo']}] {r['title']}")

    issues = today.get("open_issues_assigned", [])
    if issues:
        lines.append(f"Assigned issues ({len(issues)}):")
        for i in issues:
            lines.append(f"  - [{i['repo']}] {i['title']}")

    notifications = today.get("unread_notifications", [])
    lines.append(f"Unread notifications: {len(notifications)}")

    commits = today.get("recent_commits", [])
    if commits:
        lines.append("Recent commits (suggest improvements):")
        for repo in commits:
            lines.append(f"  Repo: {repo['repo']} — {repo.get('description', 'no description')}")
            for c in repo["commits"]:
                lines.append(f"    - {c['message']} ({c['date'][:10]})")

    if yesterday:
        prev_prs = len(yesterday.get("open_prs", []))
        curr_prs = len(prs)
        if prev_prs != curr_prs:
            lines.append(f"delta: open PRs {prev_prs} → {curr_prs}")

    return "\n".join(lines)


def _todoist(data: dict) -> str:
    today = data.get("today", {})
    yesterday = data.get("yesterday", {})
    lines = ["## Tasks (Todoist)"]

    overdue = today.get("overdue", [])
    due_today = today.get("due_today", [])
    completed = today.get("completed_yesterday", [])

    lines.append(f"Overdue: {len(overdue)}")
    for t in overdue:
        lines.append(f"  - {t}")

    lines.append(f"Due today: {len(due_today)}")
    for t in due_today:
        lines.append(f"  - {t}")

    lines.append(f"Completed yesterday: {len(completed)}")

    if yesterday:
        prev_overdue = len(yesterday.get("overdue", []))
        curr_overdue = len(overdue)
        if prev_overdue != curr_overdue:
            lines.append(f"delta: overdue tasks {prev_overdue} → {curr_overdue}")

    return "\n".join(lines)


def _gmail(data: dict) -> str:
    today = data.get("today", {})
    lines = ["## Gmail"]
    lines.append(f"Unread: {today.get('unread_count', 0)}")
    for email in today.get("important", []):
        lines.append(f"  - From: {email['from']} | Subject: {email['subject']}")
    return "\n".join(lines)


def _outlook(data: dict) -> str:
    today = data.get("today", {})
    lines = ["## Outlook"]
    lines.append(f"Unread: {today.get('unread_count', 0)}")
    for email in today.get("important", []):
        lines.append(f"  - From: {email['from']} | Subject: {email['subject']}")
    return "\n".join(lines)


def _calendar(data: dict) -> str:
    today = data.get("today", {})
    lines = ["## Calendar"]
    events = today.get("events", [])
    if not events:
        lines.append("No events today.")
    for e in events:
        lines.append(f"  - {e['time']} | {e['title']} ({e.get('duration', '?')} min)")
    return "\n".join(lines)


def _slack(data: dict) -> str:
    today = data.get("today", {})
    lines = ["## Slack"]
    lines.append(f"Unread messages: {today.get('unread_count', 0)}")
    mentions = today.get("mentions", [])
    if mentions:
        lines.append(f"Mentions ({len(mentions)}):")
        for m in mentions:
            lines.append(f"  - [{m['channel']}] {m['user']}: {m['text'][:100]}")
    return "\n".join(lines)


def _sheets(data: dict) -> str:
    today = data.get("today", {})
    lines = ["## Google Sheets"]
    for sheet in today.get("sheets", []):
        lines.append(f"  - {sheet['name']}: {sheet['summary']}")
    return "\n".join(lines)


def _plaid(data: dict) -> str:
    today = data.get("today", {})
    yesterday = data.get("yesterday", {})
    lines = ["## Finances (Plaid)"]
    lines.append(f"Transactions yesterday: {today.get('transaction_count', 0)}")
    lines.append(f"Total spent yesterday: ${today.get('total_spent', 0):.2f}")
    flagged = today.get("flagged", [])
    if flagged:
        lines.append("Flagged transactions:")
        for t in flagged:
            lines.append(f"  - {t['merchant']} ${t['amount']:.2f}")
    if yesterday:
        prev_spent = yesterday.get("total_spent", 0)
        curr_spent = today.get("total_spent", 0)
        if abs(prev_spent - curr_spent) > 20:
            lines.append(f"delta: spend ${prev_spent:.2f} → ${curr_spent:.2f}")
    return "\n".join(lines)


def _geoip(data: dict) -> str:
    today = data.get("today", {})
    lines = ["## Location"]
    lines.append(f"  {today.get('city', '?')}, {today.get('region', '?')} — {today.get('timezone', '?')}")
    return "\n".join(lines)


def _health(data: dict) -> str:
    today = data.get("today", {})
    yesterday = data.get("yesterday", {})
    lines = ["## Apple Health"]
    lines.append(f"Steps yesterday: {today.get('steps', '?')}")
    lines.append(f"Sleep: {today.get('sleep_hours', '?')} hrs")
    lines.append(f"Active calories: {today.get('active_calories', '?')}")
    if yesterday:
        prev_sleep = yesterday.get("sleep_hours", 0)
        curr_sleep = today.get("sleep_hours", 0)
        if prev_sleep and curr_sleep:
            diff = round(curr_sleep - prev_sleep, 1)
            if abs(diff) >= 0.5:
                lines.append(f"delta: sleep {prev_sleep} → {curr_sleep} hrs ({'+' if diff > 0 else ''}{diff})")
    return "\n".join(lines)


# --- Instructions ---

def _instructions() -> str:
    return """## Instructions
- Prioritize by urgency and impact
- Flag anything overdue or time-sensitive first
- For GitHub commits, suggest one concrete next step per active repo
- Note any deltas from yesterday that deserve attention
- Keep the briefing concise and actionable
- End with a single recommended first task to start the day"""