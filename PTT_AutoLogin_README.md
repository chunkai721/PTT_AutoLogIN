PTT AutoLogin 功能說明文件
1. 簡介
PTT AutoLogin 是一個自動登入 PTT 的 Python 程式。它使用 PyPtt 庫來進行登入操作，並利用 LINE Notify 通知用戶程式的啟動和每次執行的結果。

2. 主要功能
自動登入: 程式會使用提供的 PTT 帳號和密碼自動登入。
LINE 通知: 程式啟動時和每次執行完畢後，都會通過 LINE Notify 通知用戶。
排程執行: 程式設定為每天 UTC 22:00 (即 UTC+8 的早上 6 點) 自動執行。
3. 環境變數
程式使用以下環境變數：

PTT_ID: PTT 的帳號。
PTT_PW: PTT 的密碼。
PTTAUTOLOGIN_LINE_TOKEN: LINE Notify 的權杖。
4. 使用方法
確保已安裝所有必要的 Python 套件。
設定上述環境變數。
執行程式。
5. 錯誤處理
程式包含以下錯誤處理機制：

登入失敗
帳號或密碼錯誤
只能使用安全連線
需要設定連絡信箱
當遇到上述錯誤時，程式會輸出相應的錯誤訊息。

6. 依賴套件
PyPtt: 用於 PTT 的登入操作。
nest_asyncio: 用於解決異步操作中的嵌套事件循環問題。
schedule: 用於排程自動執行功能。
os: 用於讀取環境變數。
time: 用於延遲操作。