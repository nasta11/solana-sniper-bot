# Solana Real-time Monitor with Telegram Alerts

Graduation project for the **OTUS "Solidity Developer"** program.

A Python bot that connects to the **Solana** blockchain over WebSocket, watches transaction logs in real time, filters key instructions and sends formatted alerts to **Telegram**. Trading is only simulated: the bot monitors and logs, it does not send transactions.

## Features
- WebSocket connection to Solana (Helius / QuickNode), `logsSubscribe` on Devnet
- Filters key instructions: `MintTo`, `Swap`, `Create`, `NewClaim`
- Telegram alerts with instruction, program and a Solscan link
- Logs every match to `logs.json`, `targets.txt`, `snipes.txt`
- Automatic ping on timeout and reconnect after errors

## Setup
```bash
git clone https://github.com/nasta11/solana-sniper-bot.git
cd solana-sniper-bot
pip install -r requirements.txt
cp .env.example .env   # then put your own keys into .env
python bot.py
```

## Tech
Python, asyncio, websockets, aiogram, Solana JSON-RPC
