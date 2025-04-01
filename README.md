# Zyn Telegram Bot

A Telegram bot to track and summarize your daily and weekly Zyn usage. This bot uses MongoDB to store usage data and provides commands to view daily and weekly summaries.
The bot is hosted on MongoDB and Render. You can find it here: https://web.telegram.org/k/#@zyn_tracker_bot

## Features

- Track daily Zyn usage with the `/zyn` command.
- Get a summary of today's Zyn usage with the `/daily` command.
- Get a summary of the last 7 days' Zyn usage with the `/weekly` command.
- Get a summary of the last 30 days' Zyn usage with the `/30days` command.
- Delete the most recent entry with the `/removeRecent` command.
- Delete all entries with the `/deleteAll` command.
- Get help with `/help`.

## Prerequisites

- Python 3.11 or higher
- MongoDB instance
- Telegram bot token from BotFather

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/zyn-telegram-bot.git
   cd zyn-telegram-bot
   ```
2. **Create a virtual environment":
   ```bash
   python -m venv myvenv
   source myvenv/bin/activate # For MacOS or Linux
   myvenv\Scripts\activate # For Windows
   ```
3. **Create a `.env` file** in the project directory and add your environment variables:
   ```bash
   TELEGRAM_BOT_TOKEN=your_actual_bot_token
   MONGO_URI=your_mongodb_uri
   ```
## Usage
1. **Run the Bot**
   ```bash
   python bot.py
   ```
2. **Interact with the bot** on Telegram with the following commands:
   - `/zyn`: Track your Zyn usage for the today.
   - `/daily`: Get today's Zyn usage summary.
   - `/weekly`: Get the last 7 days' Zyn usage summary.
## Project Structure
```
  zyn-telegram-bot/
  │
  ├── bot.py               # Main bot script
  ├── requirements.txt     # Python dependencies
  ├── .env                 # Environment variables (not included in the repo)
  ├── README.md            # Project documentation
  └── zyn_usage.json       # Local storage for usage data (if not using MongoDB)
```
## Contributing
Contributions are welcome! Please follow these steps to contribute:
1. **Fork the repository.**
2. **Create a new branch.**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes.**
4. **Commit your changes.**
   ```bash
   git commit -m "Add commit message"
   ```
5. **Push to the branch.**
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Open a pull request.**
## License
This project is licensed under the Apache 2.0 License. See the LICENSE file for details.
## Acknowledgements
- python-telegram-bot
- MongoDB
- dotenv
---
Happy tracking! 😊
