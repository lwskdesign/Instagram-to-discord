# Instagram to discord post images
[![status: archive](https://github.com/GIScience/badges/raw/master/status/archive.svg)](https://github.com/GIScience/badges#archive)
Forked version of @fernandod1's excellent [Instagram-to-Discord](https://github.com/fernandod1/Instagram-to-discord)-Bot.

This script executes 3 actions:

1. Monitors for new image posted in a instagram account.
2. If found new image, a bot posts new instagram image in a discord channel.
3. Repeat after set interval.

## Usage:

Set environment variables in the `.env`-file:

- Set IG_USERNAME to username account you want to monitor.
- Set WEBHOOK_URL to Discord account webhook url.
- Set TIME_INTERVAL to the time in seconds in between each check for a new post.
- DONT TOUCH THE `LAST_IMAGE_ID`-KEY.