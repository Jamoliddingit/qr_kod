# QR Code Telegram Bot (Render + GitHub ready)

Bu repo GitHub va Render uchun tayyorlangan QR kod Telegram bot loyihasi.

## Muhim

- `main.py` ichida **bot token yozilmagan**.
- `BOT_TOKEN` environment variable orqali olinadi.
- Tokenni **hech qachon GitHubga qo‘ymang**.

## Ishga tushirish (lokal)

1. Virtual environment yarating va faollashtiring (ixtiyoriy).
2. Kerakli kutubxonalarni o‘rnating:

   ```bash
   pip install -r requirements.txt
   ```

3. Environment o‘zgaruvchini o‘rnating:

   **Windows (PowerShell):**
   ```powershell
   $env:BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
   ```

   **Linux / macOS:**
   ```bash
   export BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
   ```

4. Botni ishga tushiring:

   ```bash
   python main.py
   ```

## Render uchun

- Render dashboard’da:
  - `BOT_TOKEN` environment variable qo‘shing.
  - `RENDER_EXTERNAL_URL` ni xizmat URL manziliga teng qiling.
