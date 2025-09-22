import os
import time
import random
import logging
import PyPtt
import nest_asyncio
import schedule
from datetime import datetime
import pytz
from dotenv import load_dotenv
from logging.handlers import TimedRotatingFileHandler

# Initialize environment variables
load_dotenv()
ptt_id = os.environ.get('PTT_ID')
ptt_pw = os.environ.get('PTT_PW')
LOG_DIR = os.environ.get('LOG_DIR', 'logs')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()

def setup_logging():
    """Configure rotating file and console logging."""
    os.makedirs(LOG_DIR, exist_ok=True)

    root_logger = logging.getLogger()
    level = getattr(logging, LOG_LEVEL, logging.INFO)
    root_logger.setLevel(level)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

    file_handler = TimedRotatingFileHandler(
        filename=os.path.join(LOG_DIR, 'app.log'),
        when='midnight',
        backupCount=7,
        encoding='utf-8'
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    # Reset handlers to avoid duplicates when reloading
    root_logger.handlers.clear()
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

def initialize():
    """Initialize the environment and notify the start of the program."""
    nest_asyncio.apply()
    setup_logging()
    logging.info('PTT AutoLogin 程式啟動')

def run_bot():
    """Log in to PTT and notify upon completion."""
    ptt_bot = PyPtt.API()

    try:
        logging.info('開始登入 PTT')
        ptt_bot.login(ptt_id=ptt_id, ptt_pw=ptt_pw, kick_other_session=False)
        logging.info('PTT 登入成功')
    except PyPtt.LoginError:
        logging.error('登入失敗 (LoginError)')
    except PyPtt.WrongIDorPassword:
        logging.error('帳號密碼錯誤 (WrongIDorPassword)')
    except PyPtt.OnlySecureConnection:
        logging.error('只能使用安全連線 (OnlySecureConnection)')
    except PyPtt.ResetYourContactEmail:
        logging.error('請先至信箱設定連絡信箱 (ResetYourContactEmail)')
    finally:
        ptt_bot.logout()
        logging.info('PTT 已登出')

def schedule_random_time():
    """Schedule the bot to run at a random time every day."""
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)
    schedule_time = f"{random_hour:02d}:{random_minute:02d}"
    schedule.every().day.at(schedule_time).do(run_bot)
    logging.info(f'已排程今日執行時間：{schedule_time}')

def main():
    """Main function: test login once, then schedule daily random run."""
    # Run immediate login test
    run_bot()
    # Then schedule daily random run
    schedule_random_time()

    while True:
        # Convert system's UTC time to UTC+8
        taipei = pytz.timezone('Asia/Taipei')
        current_time = datetime.now(taipei)

        if current_time.hour == 0 and current_time.minute == 0:
            # Reschedule at a new random time every day at midnight
            schedule.clear()
            schedule_random_time()
            logging.info('已於午夜重新抽隔天隨機時間')
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    initialize()
    main()
