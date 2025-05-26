# 🧠 Solana Sniper Bot

🎓 Дипломный проект — интеллектуальный бот для автоматического отслеживания событий в сети **Solana** и оповещения через **Telegram**.

## 🚀 Возможности

- Подключение к Solana через WebSocket (QuickNode / Helius)
- Отслеживание ключевых инструкций: `MintTo`, `Swap`, `Create`, `NewClaim`
- Фильтрация событий
- Уведомления с расшифровкой и ссылкой на Solscan
- Хранение логов: `logs.json`, `snipes.txt`, `targets.txt`

## 🛠️ Установка

```bash
git clone https://github.com/nasta11/solana-sniper-bot.git
cd solana-sniper-bot
pip install -r requirements.txt

