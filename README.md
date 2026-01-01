# AstroQuant Day Planner

A daily automated Telegram report for XAUUSD combining astrology, ICT concepts, and market news, with bilingual output and advanced analytics.

## Features
- Aspect-wise modular reporting: astrology, ICT/AI, news, summary, forecast
- Robust error handling and fallback messages
- User-configurable report time, language, and aspects (see `user_config.yaml`)
- Daily scheduling with APScheduler
- Logging of all actions and errors
- Feedback mechanism for report users

## Setup
1. Clone the repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure your Telegram bot token and chat ID in `config.py`.
3. Edit `user_config.yaml` to set your preferred report time, language, and aspects.

## Usage
- To run once:
  ```bash
  python3 daily_astro_telegram.py
  ```
- To enable daily scheduling (default):
  ```bash
  python3 daily_astro_telegram.py
  ```
  The report will be sent at the time specified in `user_config.yaml`.

## Troubleshooting
- Check `astroquantdayplanner.log` for errors and actions.
- Ensure all API keys and dependencies are set up.
- For feedback, reply to the Telegram report or use `/feedback` command.

## Extending
- Expand AI/ICT analytics in `daily_astro_telegram.py`.
- Add new news sources or astrology modules as needed.

## License
MIT