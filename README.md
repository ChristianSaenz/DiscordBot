# DiscordBot
This Discord bot updates the weather for four cities: Portland, Houston, San Antonio, and Orlando. It offers three primary commands and automated reporting features, all managed by a PM2 process for reliability.

Commands
	1.	!weather
	•	Sends a daily weather report for the specified cities.
	2.	!current
	•	Provides the current weather conditions for the specified cities.
	3.	!humidity
	•	Displays the temperature and humidity levels for the current day in the specified cities.

Automated Features

	•Daily Reports
	The bot automatically sends weather updates to a designated channel twice a day:
	•	Morning Report: Sent at 8:00 AM.
	•	Evening Report: Sent at 10:00 PM.
	•	Alert Notifications
The send_alerts function monitors weather alerts for the specified cities and sends them to the Discord channel.
	•	Alerts are stored in a set to prevent duplicate messages and spamming.
	•	This ensures that only new alerts are sent, keeping the channel concise and informative.

PM2 Integration

The bot is managed using PM2, which enables:
	1.	Reliable response handling for the commands mentioned above.
	2.	Scheduled execution of the daily reports and alert notifications.
