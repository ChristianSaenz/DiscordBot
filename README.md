# Discord Weather Bot

A Discord bot that provides weather-related updates for **Portland**, **Houston**, **San Antonio**, and **Orlando**. The bot includes commands for retrieving weather information, automated daily reports, and real-time alert notifications. Managed by PM2 for reliability and scalability.

## Features

### Commands
The bot supports the following commands in Discord channels:

1. **`!weather`**  
   - Sends a **daily weather report** for the specified cities.

2. **`!current`**  
   - Provides the **current weather conditions** for the specified cities.

3. **`!humidity`**  
   - Displays the **temperature and humidity** levels for the current day in the specified cities.

### Automated Features
#### Daily Reports
The bot automatically sends weather updates twice daily:
- **Morning Report**: Sent at **8:00 AM**.
- **Evening Report**: Sent at **10:00 PM**.

#### Alert Notifications
- Monitors weather alerts for the specified cities.
- Sends alert messages to the Discord channel in real-time.
- Utilizes a set to store alerts, ensuring duplicates are not sent, preventing channel spam.

### PM2 Integration
The bot is managed using **PM2**, which provides:
1. **Reliable command handling** for all bot features.
2. **Scheduled execution** of daily reports and alert notifications.

