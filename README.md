# Repo_insight


A Python script that analyzes a GitHub user's public repositories, summarizes descriptions, computes a simple efficiency score, and highlights the best project.

## Features
- Fetches all public repositories of a GitHub user (ignores forks)
- Summarizes repository descriptions
- Scores repositories based on:
  - Presence of description
  - Programming language used
  - Number of stars
  - Recency of last update
- Highlights the best project
- Outputs results directly in the CLI

## Installation
Make sure you have Python 3 installed. Install the required package:
```bash
pip install requests

