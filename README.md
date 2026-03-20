# WoW Auction Profit Bot 🤖📊

A simple and fast Discord bot that scrapes WoWPriceHub to calculate the current crafting profit for Darkmoon Decks (Void and Blood) on the EU-Drak'thul realm. 

## ✨ Features
* **Real-time scraping:** Fetches the latest auction house prices for individual Darkmoon cards and complete decks.
* **Fast execution:** Uses `ThreadPoolExecutor` to fetch all 18 items in parallel.
* **Custom commands:** Clean and simple output directly in your Discord channel.

## 🛠️ Prerequisites
* Python 3.6 or higher
* Discord Bot Token (from the Discord Developer Portal)

## 🚀 Installation & Setup

**1. Clone the repository**
```bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)
cd YOUR_REPOSITORY_NAME
```

**2. Install required libraries**
```bash
pip3 install discord.py requests beautifulsoup4
```

**3. Set up your Discord Token**
Create a new file named `token.txt` in the main directory and paste your Discord bot token inside.
*Note: Make sure `token.txt` is added to your `.gitignore` to keep your credentials safe!*

**4. Run the bot**
```bash
python3 wow_bot.py
```

## 💬 Commands
* `!profit` - Calculates and displays the current crafting profit for Void and Blood decks.
* `!help` - Displays the bot's help message and available commands.
