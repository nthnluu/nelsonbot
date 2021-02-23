import datetime

import boto3
import logging
from src.nelson_bot import NelsonBot

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')


def lambda_handler(event, context):
    if 'botType' not in event:
        logger.error("The bot could not run because no bot type was specified!")
        raise Exception("No bot type specified!")

    if event['botType'] == 'nelson':
        logger.info('Initializing Nelson Bot...')
        if ('username' in event) and ('password' in event) and ('duoBypass' in event) and (
                'slotPreferences' in event):
            nelson_bot = NelsonBot()
            today = datetime.datetime.today() + datetime.timedelta(days=4)
            logger.info(f'Starting Nelson Bot for {today.month}/{today.day}/{today.year}...')
            refresh_count = 300

            if 'refreshCount' in event:
                refresh_count = event['refreshCount']

            nelson_bot.start(month=today.month, day=today.day, year=today.year, username=event['username'],
                             password=event['password'],
                             duo_bypass=event['duoBypass'],
                             slot_preferences=event['slotPreferences'], refresh_count=refresh_count, refresh_interval=2)
            nelson_bot.close()
        else:
            logger.error("Missing required values!")
    else:
        return "Hello!"
