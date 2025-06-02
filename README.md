# Telegram Auto Caption Bot

A simple Telegram bot that automatically generates captions for files (documents, videos, audio) based on their metadata and a customizable format.

## Features:
* Automatically captions files based on name and type.
* Supports custom caption formats using variables.
* Easy to deploy.

## Variables Supported:
The bot uses the following variables to format captions:
* `{filename}`: Original file name.
* `{filesize}`: Original file size.
* `{caption}`: Original file caption provided by user (if any).
* `{language}`: Language from file name (requires parsing logic).
* `{year}`: Year from file name (requires parsing logic).
* `{quality}`: Quality from file name (e.g., 720p, 1080p - requires parsing logic).
* `{season}`: Season from file name (requires parsing logic).
* `{episode}`: Episode from file name (requires parsing logic).
* `{duration}`: Duration from video/audio.
* `{height}`: Height of video.
* `{width}`: Width of video.
* `{ext}`: File extension (mp4, mp3, mkv, etc.).
* `{resolution}`: Resolution of video.
* `{mime_type}`: MIME type of video/audio.
* `{title}`: Audio title name.
* `{artist}`: Audio artist name.
* `{wish}`: Dynamic wish (e.g., "Good Morning", "Good Afternoon" - requires time-based logic).

## Setup & Deployment

### 1. Get Your API Keys:
* **Bot Token:** Obtain this from [@BotFather](https://t.me/BotFather) on Telegram.
* **API ID & API Hash:** Get these from [my.telegram.org](https://my.telegram.org/).

### 2. Local Setup (for development/testing):

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YourUsername/TelegramAutoCaptionBot.git](https://github.com/YourUsername/TelegramAutoCaptionBot.git)
    cd TelegramAutoCaptionBot
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Create `.env` file:**
    Copy the contents of `.env.example` into a new file named `.env` in the root of the project.
    ```
    cp .env.example .env
    ```
    Then, open `.env` and fill in your `BOT_TOKEN`, `API_ID`, `API_HASH`, and `ADMINS`.
    ```
    BOT_TOKEN=YOUR_BOT_TOKEN
    API_ID=YOUR_API_ID
    API_HASH=YOUR_API_HASH
    ADMINS=YOUR_TELEGRAM_USER_ID # Your User ID(s), comma-separated if multiple
    ```
5.  **Run the bot:**
    ```bash
    python bot.py
    ```

### 3. Deployment to Cloud Platform (for 24/7 uptime):

#### **A. Deploy to Render (Recommended for simplicity):**

1.  Create an account on [Render.com](https://render.com/).
2.  Go to your Dashboard and click "New" -> "Web Service".
3.  Connect your GitHub account and select this repository.
4.  Configure the service:
    * **Name:** `telegram-auto-caption-bot` (or your preferred name)
    * **Region:** Choose a region close to you.
    * **Branch:** `main` (or `master`)
    * **Root Directory:** (Leave empty if your bot.py is in the root)
    * **Build Command:** `pip install -r requirements.txt`
    * **Start Command:** `python bot.py`
    * **Environment Variables:** Add your `BOT_TOKEN`, `API_ID`, `API_HASH`, `ADMINS`.
        * Key: `BOT_TOKEN`, Value: `YOUR_BOT_TOKEN`
        * Key: `API_ID`, Value: `YOUR_API_ID`
        * Key: `API_HASH`, Value: `YOUR_API_HASH`
        * Key: `ADMINS`, Value: `YOUR_TELEGRAM_USER_ID`
        * You can also add `CUSTOM_CAPTION_FORMAT` here to override the default.
    * **Instance Type:** Free (if available and sufficient) or a paid tier.
5.  Click "Create Web Service" and wait for deployment.

#### **B. Deploy to Heroku:**

1.  Create an account on [Heroku.com](https://www.heroku.com/).
2.  Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).
3.  Login to Heroku CLI: `heroku login`
4.  Create a new Heroku app: `heroku create your-bot-name-unique`
5.  Set environment variables:
    ```bash
    heroku config:set BOT_TOKEN=YOUR_BOT_TOKEN
    heroku config:set API_ID=YOUR_API_ID
    heroku config:set API_HASH=YOUR_API_HASH
    heroku config:set ADMINS=YOUR_TELEGRAM_USER_ID
    # Add other custom variables if needed
    ```
6.  Push your code to Heroku:
    ```bash
    git push heroku main # or master
    ```
7.  Scale your dyno (to keep the bot running):
    ```bash
    heroku ps:scale web=1
    ```

## Customizing Captions:
You can modify the `DEFAULT_CAPTION_FORMAT` and `AUDIO_CAPTION_FORMAT` variables in `config.py` (or as environment variables in your deployment platform) to change how captions are generated. Use the variables listed above.

## Contributing:
Feel free to open issues or submit pull requests.

## License:
This project is open source. (Specify a license like MIT if you want)

