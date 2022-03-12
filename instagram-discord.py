#!/usr/bin/env python3
# SOURCE: https://github.com/fernandod1/Instagram-to-discord/blob/master/instagram-discord.py

import json
import requests
import os
import time
import dotenv

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
TIME_INTERVAL = os.getenv("TIME_INTERVAL")
LAST_IMAGE_ID = os.getenv("LAST_IMAGE_ID")

def get_user_fullname(html):
    return html.json()["graphql"]["user"]["full_name"]

def get_total_photos(html):
    return int(html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["count"])

def get_last_publication_url(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["shortcode"]

def get_last_photo_url(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["display_url"]

def get_last_thumb_url(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["thumbnail_src"]

def get_description_photo(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]

def webhook(webhook_url, html):
    """
    for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook and https://discordapp.com/developers/docs/resources/channel#embed-object
    """
    data = {}
    data["embeds"] = []
    embed = {}
    embed["color"] = 15467852
    embed["title"] = f"@{INSTAGRAM_USERNAME} posted a new image"
    embed["url"] = "https://www.instagram.com/p/" + \
        get_last_publication_url(html)+"/"
    embed["description"] = get_description_photo(html)
    embed["image"] = {"url":get_last_thumb_url(html)}
    data["embeds"].append(embed)
    result = requests.post(webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Image successfully posted, code {}.".format(result.status_code))

def get_instagram_html(INSTAGRAM_USERNAME):
    headers = {
        "Host": "www.instagram.com",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
    html = requests.get("https://www.instagram.com/" + INSTAGRAM_USERNAME + "/feed/?__a=1", headers=headers)
    return html

def main():
    global last_image_id
    try:
        html = get_instagram_html(INSTAGRAM_USERNAME)
        if(LAST_IMAGE_ID == get_last_publication_url(html)):
            print("No new image found.")
        else:
            dotenv.set_key(dotenv_file, "LAST_IMAGE_ID", get_last_publication_url(html))
            print("Found new image.")
            webhook(WEBHOOK_URL,
                    get_instagram_html(INSTAGRAM_USERNAME))
    except Exception as e:
        print(e)

if __name__ == "__main__":
    if INSTAGRAM_USERNAME != None and WEBHOOK_URL != None:
        while True:
            main()
            time.sleep(float(TIME_INTERVAL or 600))
    else:
        print("Faulty environment variables!")