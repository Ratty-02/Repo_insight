import requests
import pandas as pd
import re
import math

def fetch_repos(username: str):
    """Fetch repos (ignores forks)."""
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{username}/repos?per_page=100&page={page}"
        r = requests.get(url, timeout=20)
        if r.status_code != 200:
            print(f"Error: {r.status_code}")
            break
        data = r.json()
        if not data:
            break
        for repo in data:
            if repo.get("fork"):  # skip forked repos
                continue
            repos.append({
                "name": repo["name"],
                "description": repo["description"] or "",
                "language": repo.get("language") or "",
                "stars": repo.get("stargazers_count", 0),
                "forks": repo.get("forks_count", 0),
                "updated": repo.get("updated_at"),
                "url": repo["html_url"]
            })
        page += 1
    return repos

def summarize_repo(repo):
    """Make a short 2–3 line summary."""
    desc = repo["description"].strip() if repo["description"] else "No description provided."
    summary = re.sub(r"\s+", " ", desc)
    lines = []
    if summary:
        lines.append(summary[:200])
    if repo["language"]:
        lines.append(f"Built mainly with {repo['language']}.")
    return " ".join(lines)

def score_repo(repo):
    """Compute efficiency score 0–100% based on stars, recency, description, language."""
    score = 0
    if repo["description"]:
        score += 30
    if repo["language"]:
        score += 20
    if repo["stars"] > 0:
        score += min(20, repo["stars"])  # up to +20 for stars
    # recent updates boost
    if repo["updated"]:
        score += 20
    return min(100, score)

def analyze(username):
    repos = fetch_repos(username)
    if not repos:
        print("No repos found.")
        return

    best_repo = None
    best_score = -1

    print(f"\n📂 Projects by {username}\n")
    for repo in repos:
        summary = summarize_repo(repo)
        score = score_repo(repo)
        print(f"➡️ {repo['name']}")
        print(f"   {summary}")
        print(f"   Efficiency Score: {score}%\n")

        if score > best_score:
            best_score = score
            best_repo = repo

    if best_repo:
        print("🏆 Best Project:")
        print(f"   {best_repo['name']} ({best_score}%)")
        print(f"   {summarize_repo(best_repo)}")
        print(f"   {best_repo['url']}")

if __name__ == "__main__":
    username = input("Enter GitHub username: ").strip()
    analyze(username)
