import time
from main import run_ict_ai_mentor

while True:
    try:
        run_ict_ai_mentor()
        time.sleep(60)
    except Exception as e:
        print("Error:", e)
        time.sleep(60)
