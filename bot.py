import asyncio
import json
import traceback
import websockets
from aiogram import Bot
import os
from datetime import datetime, timezone

TELEGRAM_TOKEN = "7804602601:AAFh0KU9RQX9iSL9hQvf22P52GdznUolTik"
TELEGRAM_CHAT_ID = "1184092097"
QUICKNODE_WS = "wss://rpc.helius.xyz/?api-key=a0967632-6a68-4270-b17b-607702e200af"

bot = Bot(token=TELEGRAM_TOKEN)

# Известные программы
program_labels = {
    "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA": "SPL Token Program",
    "11111111111111111111111111111111": "System Program",
    "MErKy6nZVoVAkryxAejJz2juifQ4ArgLgHmaJCQkU7N": "Bubblegum (Compression)"
}

# Важные инструкции
IMPORTANT_INSTRUCTIONS = ["mint", "swap", "create", "newclaim"]

async def send_telegram(text):
    try:
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text, parse_mode="Markdown")
        print("[LOG] ✅ Сообщение отправлено в Telegram")
    except Exception:
        print("[ERROR] ❌ Ошибка при отправке:")
        print(traceback.format_exc())

async def listen_to_solana():
    await send_telegram("✅ Бот запущен и готов слушать события в Solana Devnet...")

    while True:
        try:
            async with websockets.connect(QUICKNODE_WS) as ws:
                print("[LOG] ✅ WebSocket подключён")
                await send_telegram("🔌 Подключение к Solana установлено. Ожидаю события...")

                await ws.send(json.dumps({
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "logsSubscribe",
                    "params": [
                        {
                            "mentions": ["11111111111111111111111111111111"]
                        },
                        {
                            "commitment": "confirmed"
                        }
                    ]
                }))
                print("[LOG] Подписка на события отправлена")

                while True:
                    try:
                        raw = await asyncio.wait_for(ws.recv(), timeout=60)
                        print(f"[RAW] {raw}")

                        data = json.loads(raw)

                        if "params" in data:
                            logs = data["params"]["result"]["value"]["logs"]
                            signature = data["params"]["result"]["value"]["signature"]
                            timestamp = datetime.now(timezone.utc).isoformat()

                            for log in logs:
                                if "Program log: Instruction:" in log:
                                    instruction_name = log.split("Instruction:")[-1].strip()

                                    # Найдём ID программы
                                    program_id = None
                                    for entry in logs:
                                        if "invoke" in entry and "Program" in entry:
                                            parts = entry.split("Program ")
                                            if len(parts) > 1:
                                                candidate = parts[1].split()[0]
                                                if len(candidate) == 44:
                                                    program_id = candidate
                                                    break

                                    program_name = program_labels.get(program_id, "Неизвестная программа")

                                    # Логгирование
                                    log_entry = {
                                        "timestamp": timestamp,
                                        "signature": signature,
                                        "instruction": instruction_name,
                                        "program": program_id
                                    }

                                    with open("logs.json", "a") as f:
                                        f.write(json.dumps(log_entry) + "\n")
                                    with open("targets.txt", "a") as t:
                                        t.write(f"{timestamp} | {signature} | {instruction_name}\n")
                                    with open("snipes.txt", "a") as s:
                                        s.write(f"{timestamp} | {signature} | {instruction_name}\n")

                                    print(f"[MATCH] 🔍 {instruction_name}")
                                    print(f"🚀 [SNIPE] Имитирован снайп на транзакцию: {signature}")

                                    if instruction_name.lower() in IMPORTANT_INSTRUCTIONS:
                                        message = (
                                            f"📦 *Инструкция:* `{instruction_name}`\n"
                                            f"⚙️ *Программа:* {program_name} (`{program_id}`)\n"
                                            f"✅ *Результат:* Успешно\n"
                                            f"🔑 *Подпись транзакции:* `{signature}`\n"
                                            f"🔍 [Открыть в Solscan](https://solscan.io/tx/{signature})"
                                        )
                                        await send_telegram(message)

                        else:
                            print("[SKIP] Пропуск нерелевантного ответа:", data)

                    except asyncio.TimeoutError:
                        print("[PING] ⏳ Таймаут, отправляю ping...")
                        await ws.ping()
                    except Exception:
                        print("[ERROR] ❌ Ошибка при получении данных:")
                        print(traceback.format_exc())
                        break

        except Exception:
            print("[ERROR] ❌ Проблема с WebSocket-соединением:")
            print(traceback.format_exc())
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(listen_to_solana())

