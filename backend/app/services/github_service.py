import httpx


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