import httpx

def get_repositories(username: str):
    url = f"https://api.github.com/users/{username}/repos"

    try:
        response = httpx.get(url, timeout=10)

        if response.status_code == 404:
            return {"error": "GitHub user not found."}

        response.raise_for_status()

        repos = response.json()

        repository_list = []

        for repo in repos:
            repository_list.append({
                "name": repo.get("name"),
                "language": repo.get("language"),
                "stars": repo.get("stargazers_count"),
                "forks": repo.get("forks_count"),
                "created_at": repo.get("created_at"),
                "updated_at": repo.get("updated_at"),
                "html_url": repo.get("html_url"),
                "description": repo.get("description"),
            })

        return repository_list

    except httpx.RequestError:
        return {"error": "Unable to connect to GitHub."}

    except httpx.HTTPStatusError:
        return {"error": "GitHub returned an unexpected error."}

def get_profile(username: str):
    url = f"https://api.github.com/users/{username}"

    try:
        response = httpx.get(url, timeout=10)

        if response.status_code == 404:
            return {
                "error": "GitHub user not found."
            }

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
        return {
            "error": "Unable to connect to GitHub."
        }

    except httpx.HTTPStatusError:
        return {
            "error": "GitHub returned an unexpected error."
        }