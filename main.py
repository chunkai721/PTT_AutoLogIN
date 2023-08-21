import os
import time
import random
import PyPtt
import nest_asyncio
import schedule
from notify import send_line_notify
from datetime import datetime
import pytz

def initialize():
    """Initialize the environment and notify the start of the program."""
    nest_asyncio.apply()
    send_line_notify("PTT AutoLogin程式啟動", YOUR_LINE_TOKEN)

def run_bot():
    """Log in to PTT and notify upon completion."""
    ptt_bot = PyPtt.API()

    try:
        ptt_bot.login(ptt_id=ptt_id, ptt_pw=ptt_pw, kick_other_session=False)
        send_line_notify("PTT AutoLogin執行完畢", YOUR_LINE_TOKEN)
    except PyPtt.LoginError:
        print('登入失敗')
    except PyPtt.WrongIDorPassword:
        print('帳號密碼錯誤')
    except PyPtt.OnlySecureConnection:
        print('只能使用安全連線')
    except PyPtt.ResetYourContactEmail:
        print('請先至信箱設定連絡信箱')
    finally:
        ptt_bot.logout()

def schedule_random_time():
    """Schedule the bot to run at a random time every day."""
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)
    schedule_time = f"{random_hour:02d}:{random_minute:02d}"
    schedule.every().day.at(schedule_time).do(run_bot)

def main():
    """Main function to schedule the bot and keep it running."""
    schedule_random_time()

    while True:
        # Convert system's UTC time to UTC+8
        taipei = pytz.timezone('Asia/Taipei')
        current_time = datetime.now(taipei)

        if current_time.hour == 0 and current_time.minute == 0:
            # Reschedule at a new random time every day at midnight
            schedule.clear()
            schedule_random_time()
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    # Environment variables
    ptt_id = os.environ.get('PTT_ID')
    ptt_pw = os.environ.get('PTT_PW')
    YOUR_LINE_TOKEN = os.environ.get('PTTAUTOLOGIN_LINE_TOKEN')

    initialize()
    main()
