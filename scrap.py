import time
import requests

GRAPHQL_URL = "https://leetcode.com/graphql"
QUERY = """
query recentAcSubmissions($username: String!, $limit: Int!) {
  recentAcSubmissionList(username: $username, limit: $limit) {
    title
    timestamp
  }
}
"""


def scrap_user(user):
    headers = {
        "Content-Type": "application/json",
        "Referer": f"https://leetcode.com/{user}/",
        "User-Agent": "Mozilla/5.0",
    }
    payload = {
        "query": QUERY,
        "variables": {"username": user, "limit": 20},
    }

    try:
        resp = requests.post(GRAPHQL_URL, json=payload, headers=headers, timeout=20)
        if not resp.ok:
            print(f"Failed scraping user {user}'s Leetcode status")
            return None

        data = resp.json().get("data", {})
        submissions = data.get("recentAcSubmissionList")
        if submissions is None:
            print(f"Failed scraping user {user}'s Leetcode status")
            return None
    except Exception:
        print(f"Failed scraping user {user}'s Leetcode status")
        return None

    now = int(time.time())
    ret = []
    for item in submissions:
        title = item.get("title")
        ts = item.get("timestamp")
        if title is None or ts is None:
            continue
        minutes_ago = max(0, (now - int(ts)) // 60)
        ret.append((title, "Accepted", minutes_ago))

    print(f"Retrieved user {user}'s Leetcode status:", ret)
    return ret