# Telegram conversation-flow prototype

An early Python prototype exploring callback-driven conversation steps, CSV state and scheduled reminders. `main_0.5.py` is the latest numbered study; earlier versions remain for historical context. This is not a financial product, investment recommendation or guarantee of results.

## Configuration

Use Python 3.12 and `pip install -r requirements.txt` in a virtual environment. Set your own `TELEGRAM_BOT_TOKEN`; the scripts fail before startup when it is missing. `.env.example` is documentation, not an automatically loaded file. Provider polling and reminder delivery are real side effects: review the historical message content, image paths and retention behavior before using a separate test bot.

## Offline verification

`python -m unittest discover -s tests -v`

Checks exercise environment validation, safe errors and accidental credential literals without Telegram calls. They are configuration regressions, not a claim that every historical conversation/reminder path has been tested.

## Boundaries

CSV state is local and ignored by Git. The prototype is not designed for concurrent workers, protected personal data or production scheduling. Keep real subscriber records and provider values outside source control. See [SECURITY.md](SECURITY.md); removing current-source values does not revoke historical ones.
