import discord
import requests
import asyncio
from datetime import datetime, timedelta
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import logging
import traceback

logging.basicConfig(level=logging.INFO)

load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID').split(',')
CHANNEL_ID_1 = int(os.getenv('CHANNEL_ID_1'))
CHANNEL_ID_2 = int(os.getenv('CHANNEL_ID_2'))

# Convert CHANNEL_IDS to a list of integers
CHANNEL_ID = [int(channel_id.strip()) for channel_id in CHANNEL_ID]


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

sent_alerts = {
    CHANNEL_ID_1: set(),
    CHANNEL_ID_2: set()
}


async def fetch_weather(lat, lon):
    url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly&appid={WEATHER_API_KEY}&units=imperial'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


async def send_weather_report(channel):
    try:
        locations = {
            "Houston": {"lat": 29.7604, "lon": -95.3698},
            "Portland": {"lat": 45.5152, "lon": -122.6784},
            "Orlando": {"lat": 28.5384, "lon": -81.3789},
            "San Antonio": {"lat": 29.4252, "lon": -98.4946}
        }
        for city, coords in locations.items():
            weather = await fetch_weather(coords["lat"], coords["lon"])
            description = weather['current']['weather'][0]['description']
            temp = weather['current']['temp']
            await channel.send(f'Weather in {city}: {description}, {temp}°F')
    except Exception as e:
        logging.error(f"Error sending weather report: {e}")
        traceback.print_exc()


async def send_daily_report(channel):
    full_report = ""
    try:
        locations = {
            "Houston": {"lat": 29.7604, "lon": -95.3698},
            "Portland": {"lat": 45.5152, "lon": -122.6784},
            "Orlando": {"lat": 28.5384, "lon": -81.3789},
            "San Antonio": {"lat": 29.4252, "lon": -98.4946}
        }
        for city, coords in locations.items():
            weather = await fetch_weather(coords["lat"], coords["lon"])
            current_description = weather['current']['weather'][0]['description']
            current_temp = weather['current']['temp']
            daily_summary = weather['daily'][0]['weather'][0]['description']
            min_temp = weather['daily'][0]['temp']['min']
            max_temp = weather['daily'][0]['temp']['max']

            formatted_message = (
                f"Todays report in {city}\n\n"
                f"Current weather: {current_description}, {current_temp:.1f}°F\n"
                f"Daily summary: {daily_summary}, Min: {min_temp:.1f}°F, Max: {max_temp:.1f}°F\n"
                f"\n"
            )

            full_report += formatted_message

        # Send the complete report after building it
        await channel.send(full_report)
        
    except Exception as e:
        logging.error(f"Error sending daily report: {e}")
        traceback.print_exc()


async def send_alert_report(channel):
    try:
        locations = {
            "Houston": {"lat": 29.7604, "lon": -95.3698},
            "Portland": {"lat": 45.5152, "lon": -122.6784},
            "Orlando": {"lat": 28.5384, "lon": -81.3789},
            "San Antonio": {"lat": 29.4252, "lon": -98.4946}
        }
        for city, coords in locations.items():
            weather = await fetch_weather(coords["lat"], coords["lon"])
            if 'alerts' in weather:
                for alert in weather['alerts']:
                    event = alert['event']
                    description = alert['description']
                    start = datetime.fromtimestamp(alert['start']).strftime('%Y-%m-%d %H:%M:%S')
                    end = datetime.fromtimestamp(alert['end']).strftime('%Y-%m-%d %H:%M:%S')
                    alert_id = f"{event}--{start}"
                    if alert_id not in sent_alerts[channel.id]:
                        embed = discord.Embed(
                            title=f"Weather Alert for {city}: {event}",
                            description=f"{description[:3997]}..." if len(description) > 4000 else description, 
                            color=0xff0000
                        )
                        embed.add_field(name="Start", value=start, inline=True)
                        embed.add_field(name="End", value=end, inline=True)

                        logging.info(f"Sending alert to channel {channel.id} for {city}: {event}")
                        await channel.send(embed=embed)

                        sent_alerts[channel.id].add(alert_id)
                        logging.info(f"Alert {alert_id} sent to channel {channel.id} and added to sent_alerts.")
                    else:
                        logging.info(f"Alert {alert_id} already sent to channel {channel.id}.")
    except Exception as e:
        logging.error(f"Error sending alert report to channel {channel.id}: {e}")
        traceback.print_exc()


async def send_humidity_report (channel):
    full_report = ""
    try:
        locations = {
            "Houston": {"lat": 29.7604, "lon": -95.3698},
            "Portland": {"lat": 45.5152, "lon": -122.6784},
            "Orlando": {"lat": 28.5384, "lon": -81.3789},
            "San Antonio": {"lat": 29.4252, "lon": -98.4946}
        }
        for city, coords in locations.items():
            weather = await fetch_weather(coords["lat"], coords["lon"])
            current_humidity = weather['current']['humidity']
            current_description = weather['current']['weather'][0]['description']
            daily_humidity = weather['daily'][0]['humidity']
            daily_uvi = weather['daily'][0]['uvi']
            daily_summary = weather['daily'][0]['weather'][0]['description']

            formatted_message = (
                f"Current weather in {city:<13}: {current_description}, Humidity: {current_humidity:.1f}%\n"
                f"Daily summary: {daily_summary}, Daily Humidity: {daily_humidity:.1f}%, Daily UVI: {daily_uvi:.1f}\n\n"
            )

            full_report  += formatted_message

        await channel.send(full_report)
    except Exception as e:
        logging.error(f"Error sending humaity report: {e}")
        traceback.print_exc()

#Loops or events that occuer automatically
@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user}')
    weather_report_loop.start()
    weather_alert_loop.start()
    clear_sent_alerts.start()


@tasks.loop(minutes=1)
async def weather_report_loop():
    now = datetime.now()
    logging.info(f"Checking weather report loop at {now}")
    if now.hour == 8 and now.minute == 0:
        for channel_id in CHANNEL_ID:
            channel = bot.get_channel(channel_id)
            if channel:
                logging.info("Sending Morning Report")
                await send_daily_report(channel)
            else:
                logging.error("Channel not found")
    elif now.hour == 20 and now.minute == 0:
        for channel_id in CHANNEL_ID:
            channel = bot.get_channel(channel_id)
            if channel:
                logging.info("Sending Nightly Report")
                await send_daily_report(channel)
            else:
                logging.error("Channel not found")


@tasks.loop(hours=1)
async def weather_alert_loop():
    now = datetime.now()
    logging.info(f"Checking weather alert loop at {now}")
    for channel_id in CHANNEL_ID:
        channel = bot.get_channel(channel_id)
        if channel:
            logging.info(f"Attempting to send weather alerts to channel: {channel_id}")
            await send_alert_report(channel)
        else:
            logging.error("Channel not found")


@tasks.loop(hours=24)
async def clear_sent_alerts():
    sent_alerts.clear()
    logging.info("Cleared sent alerts")

#Discord Commands 

@bot.command(name='weather')
async def weather(ctx):
    await send_weather_report(ctx.channel)


@bot.command(name='daily')
async def daily(ctx):
    await send_daily_report(ctx.channel)


@bot.command(name='humidity')
async def humidity(ctx):
    await send_humidity_report(ctx.channel)


bot.run(TOKEN)




