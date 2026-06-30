import httpx


def get_profile(username: str):
    url = f"https://api.github.com/users/{username}"

    try:
        response = httpx.get(url, timeout=10)

        if response.status_code == 404:
            return {"error": "GitHub user not found."}

        response.raise_for_status()

        data = response.json()

        return {
            "username": data.get("login"),
            "name": data.get("name"),
            "bio": data.get("bio"),
            "avatar_url": data.get("avatar_url"),
            "followers": data.get("followers"),
            "following": data.get("following"),
            "public_repos": data.get("public_repos"),
            "profile_url": data.get("html_url"),
        }

    except httpx.RequestError:
        return {"error": "Unable to connect to GitHub."}

    except httpx.HTTPStatusError:
        return {"error": "GitHub returned an unexpected error."}

def get_repositories(username: str):
    url = f"https://api.github.com/users/{username}/repos"

    try:
        response = httpx.get(url, timeout=10)

        if response.status_code == 404:
            return {"error": "GitHub user not found."}

        response.raise_for_status()

        repos = response.json()

        repository_list = []

        total_stars = 0
        total_forks = 0
        total_commits = 0

        language_count = {}

        top_repository = None
        max_stars = -1

        for repo in repos:

            repo_name = repo.get("name")
            commit_url = f"https://api.github.com/repos/{username}/{repo_name}/commits"

            try:
                commit_response = httpx.get(commit_url, timeout=10)

                if commit_response.status_code == 200:
                    commits = commit_response.json()

                    if isinstance(commits, list):
                        commit_count = len(commits)
                    else:
                        commit_count = 0
                else:
                    commit_count = 0

            except Exception:
                commit_count = 0

            total_commits += commit_count

            # Repository details
            repository_list.append({
                "name": repo.get("name"),
                "description": repo.get("description"),
                "language": repo.get("language"),
                "stars": repo.get("stargazers_count"),
                "forks": repo.get("forks_count"),
                "commits": commit_count,
                "html_url": repo.get("html_url"),
                "created_at": repo.get("created_at"),
                "updated_at": repo.get("updated_at"),
            })

            # Total stars
            total_stars += repo.get("stargazers_count", 0)

            # Total forks
            total_forks += repo.get("forks_count", 0)

            # Count languages
            language = repo.get("language")

            if language:
                language_count[language] = (
                    language_count.get(language, 0) + 1
                )

            # Find top repository by stars
            if repo.get("stargazers_count", 0) > max_stars:
                max_stars = repo.get("stargazers_count", 0)
                top_repository = repo.get("name")

        # Most used language
        most_used_language = None

        if language_count:
            most_used_language = max(
                language_count,
                key=language_count.get
            )

        # Top 5 repositories
        top_repositories = sorted(
            repository_list,
            key=lambda repo: repo["stars"],
            reverse=True
        )[:5]

        return {
            "statistics": {
                "total_repositories": len(repos),
                "total_stars": total_stars,
                "total_forks": total_forks,
                "total_commits": total_commits,
                "most_used_language": most_used_language,
                "top_repository": top_repository,
            },
            "language_distribution": language_count,
            "top_repositories": top_repositories,
            "repositories": repository_list,
        }

    except httpx.RequestError:
        return {"error": "Unable to connect to GitHub."}

    except httpx.HTTPStatusError:
        return {"error": "GitHub returned an unexpected error."}