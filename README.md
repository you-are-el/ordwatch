# OrdWatch <img src="logo.svg" alt="OrdWatch Logo" height="20">

**OrdWatch** is a simple Telegram notification service that tracks Bitcoin addresses for new transactions in the mempool. It's designed to connect to your own Bitcoin node via your local Mempool API or the public Mempool API to send notifications when new transactions appear or get confirmed.

## Features
- Track multiple Bitcoin addresses.
- Get notifications for unconfirmed and confirmed transactions via Telegram.
- Connect to your own Bitcoin node or use the public Mempool API.
- Customizable cron job frequency for transaction checks.

---

## Setup Guide

### Prerequisites
- Docker installed on your local machine or server.
- A Telegram bot (we’ll show you how to create one).
- A Bitcoin address to monitor.
- (Optional) Access to your own Mempool API or node.

---

### Step 1: Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/ordwatch.git
cd ordwatch
```

---

### Step 2: Create a Telegram Bot

To send notifications via Telegram, you need to create your own Telegram bot:

1. Open Telegram and search for **BotFather**.
2. Start a chat with **BotFather** and type `/newbot`.
3. Follow the instructions to name your bot and get a **Telegram Bot Token**.
   - BotFather will give you a token in this format: `123456789:ABCdefGhIJKlmNO4567PqrsTuVWxyZ12-34`.

---

### Step 3: Get Your Telegram User ID

To receive notifications, you need your **Telegram User ID**:

1. Start a chat with [userinfobot](https://t.me/userinfobot) on Telegram.
2. Type `/start` and the bot will reply with your user information, including your **Telegram User ID**.
   - Example: `123456789`.

---

### Step 4: Configure Your Environment Variables

1. Copy the `.env.example` file to a new `.env` file:
   
   ```bash
   cp .env.example .env
   ```

2. Open the `.env` file and fill in the necessary values:
   - `TELEGRAM_BOT_TOKEN`: The token you got from **BotFather**.
   - `TELEGRAM_USER_ID`: Your personal Telegram user ID.
   - `BITCOIN_ADDRESS_1`: The Bitcoin address you want to monitor.
   - (Optional) `BITCOIN_ALIAS_1`: A friendly name or alias for the first Bitcoin address, used in notifications (e.g., "Main Wallet").
   - (Optional) `MEMPOOL_API_URL`: If you're using your own node, replace this with the URL of your own Mempool API.

---

### Step 5: Edit the Cron Job (Optional)

If you want to control how often OrdWatch checks for new transactions, you'll need to modify the `cronjob` file:

1. Open the `cronjob` file in the repository:
   
   ```bash
   nano cronjob
   ```

2. Edit the schedule to your desired frequency using cron syntax. For example, to run every 5 minutes:

   ```bash
   */1 * * * * /usr/local/bin/python /app/ordwatch.py > /proc/1/fd/1 2>/proc/1/fd/2
   ```

   **Note**: The default cron job checks for new transactions every minute. You can adjust this to any interval based on your needs. However, more frequent checks might result in rate limits if you are using the public Mempool API. For further info check: https://mempool.space/docs/api/rest.

---

### Step 6: Build and Run the Docker Container

#### Building the Docker Image

After editing the `cronjob` file, build the Docker image:

```bash
docker build -t ordwatch .
```

#### Running the Docker Container

Once the image is built, you can run the container:

```bash
docker run -d --env-file .env ordwatch
```

This will start the service and begin monitoring your Bitcoin addresses.

---

## Additional Configuration

- **Tracking Multiple Bitcoin Addresses**: You can monitor as many addresses as you want by adding more variables in your `.env` file (e.g., `BITCOIN_ADDRESS_2`, `BITCOIN_ALIAS_2`). Just beware of rate limits when using too many addresses at once.
- **Running with Your Own Mempool API**: If you’re running a Bitcoin node and Mempool API, replace the `MEMPOOL_API_URL` in the `.env` file with the URL of your Mempool instance.

---

## Troubleshooting

- **Not Receiving Notifications?** Make sure your bot is running and that you’ve entered the correct `TELEGRAM_BOT_TOKEN` and `TELEGRAM_USER_ID`.
- **Error Fetching Transactions?** Double-check that the `MEMPOOL_API_URL` is accessible and correct.

---

## License

This project is licensed under the MIT License with an additional non-commercial clause. You may use, modify, and distribute this software for personal use. However, commercial use is not permitted without the express permission of the copyright holder.

For more details, see the [LICENSE](./LICENSE) file.


---

## Questions and Feedback

If you have any questions or feedback, feel free to [contact me on X](https://x.com/you_are_el). You're welcome to DM me for any clarifications or suggestions regarding OrdWatch.