import os
import time
from supabase import create_client

def calculate_yields():
    supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
    while True:
        time.sleep(3600)
        print("🔄 Calculating staking yields...")

if __name__ == '__main__':
    calculate_yields()
