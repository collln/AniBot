import requests
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

# URL for the AniList API
url = 'https://graphql.anilist.co'

# Here we define our query as a multi-line string
query = '''
query ($search: String) {
  Media(search: $search) {
    id
    title{ english }
    nextAiringEpisode{
      episode
      airingAt
    }
  }
}
'''


def userQuery(search):
    # Define our query variables and values that will be used in the query request
    variables = {
        'search': search
    }

    # Make the HTTP Api request
    response = requests.post(url, json={'query': query, 'variables': variables})
    json_response = response.json()

    media = json_response['data']['Media']
    if media is None:
        return None, None

    # Grabbing the Title and the Release Date from the response
    anime_title = media['title']['english']

    next_episode = media['nextAiringEpisode']
    if next_episode:
        release_date = next_episode['airingAt']
        dt_utc = datetime.fromtimestamp(release_date, tz=timezone.utc)
        dt_eastern = dt_utc.astimezone(ZoneInfo("US/Eastern"))
    else:
        dt_eastern = None

    return anime_title, dt_eastern


# Printing the Output (only when running this file directly, not on import)
if __name__ == "__main__":
    title, air_date = userQuery('Liar Game')
    print(f'The title of the anime that you have Queried is: {title} \n')
    if air_date:
        print(f'The anime has an upcoming release at: {air_date}')
    else:
        print('There is no upcoming release scheduled for this anime.')
