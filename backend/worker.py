import os
import time
import logging
import asyncio
import redis
from supabase import create_client, Client
from web3 import Web3
from web3.exceptions import ContractLogicError, TransactionNotFound
from decimal import Decimal
import json
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('worker.log') if os.environ.get('LOG_TO_FILE') else logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class YieldCalculationWorker:
    def __init__(self):
        self.setup_clients()
        self.interval = int(os.environ.get('WORKER_INTERVAL', 60))  # seconds
        self.max_retries = int(os.environ.get('MAX_RETRIES', 3))
        self.retry_delay = int(os.environ.get('RETRY_DELAY', 5))
        
    def setup_clients(self):
        """Initialize Supabase, Redis, and Web3 clients with error handling"""
        try:
            # Supabase client
            supabase_url = os.environ.get('SUPABASE_URL')
            supabase_key = os.environ.get('SUPABASE_KEY')
            
            if not supabase_url or not supabase_key:
                raise ValueError("Supabase URL and KEY must be set in environment variables")
                
            self.supabase: Client = create_client(supabase_url, supabase_key)
            logger.info("Supabase client initialized successfully")
            
            # Redis client
            redis_url = os.environ.get('REDIS_URL')
            if redis_url:
                self.redis_client = redis.from_url(redis_url)
                logger.info("Redis client initialized successfully")
            else:
                self.redis_client = None
                logger.warning("Redis URL not set, caching disabled")
            
            # Web3 provider
            web3_provider = os.environ.get('WEB3_PROVIDER_URL', 'http://localhost:8545')
            self.w3 = Web3(Web3.HTTPProvider(web3_provider))
            
            if self.w3.is_connected():
                logger.info(f"Web3 connected to {web3_provider}")
            else:
                logger.warning("Web3 connection failed")
                
        except Exception as e:
            logger.error(f"Failed to initialize clients: {e}")
            raise
    
    def exponential_backoff(self, retry_count):
        """Calculate exponential backoff delay"""
        return min(self.retry_delay * (2 ** retry_count), 300)  # Max 5 minutes
    
    def get_pending_calculations(self):
        """Fetch pending yield calculations from Supabase"""
        try:
            response = self.supabase.table('yield_calculations')\
                .select('*')\
                .eq('status', 'pending')\
                .order('created_at', desc=False)\
                .limit(10)\
                .execute()
            
            return response.data if response.data else []
            
        except Exception as e:
            logger.error(f"Error fetching pending calculations: {e}")
            return []
    
    def calculate_yield(self, calculation_data):
        """
        Calculate yield based on provided data
        This is a simplified example - implement your actual yield logic here
        """
        try:
            # Example yield calculation - replace with your actual logic
            principal = Decimal(calculation_data.get('principal', 0))
            rate = Decimal(calculation_data.get('rate', 0))
            time_period = Decimal(calculation_data.get('time_period', 1))
            
            # Simple compound interest calculation
            yield_amount = principal * ((1 + rate) ** time_period - 1)
            
            return {
                'yield_amount': float(yield_amount),
                'calculated_at': datetime.utcnow().isoformat(),
                'status': 'completed'
            }
            
        except Exception as e:
            logger.error(f"Error calculating yield: {e}")
            return {
                'error': str(e),
                'status': 'failed'
            }
    
    def update_calculation(self, calculation_id, update_data):
        """Update calculation record in Supabase"""
        try:
            response = self.supabase.table('yield_calculations')\
                .update(update_data)\
                .eq('id', calculation_id)\
                .execute()
            
            if response.data:
                logger.info(f"Updated calculation {calculation_id} with status: {update_data.get('status')}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error updating calculation {calculation_id}: {e}")
            return False
    
    def cache_result(self, calculation_id, result):
        """Cache calculation result in Redis"""
        if not self.redis_client:
            return
            
        try:
            cache_key = f"yield_result:{calculation_id}"
            self.redis_client.setex(
                cache_key,
                timedelta(hours=1),  # Cache for 1 hour
                json.dumps(result)
            )
            logger.debug(f"Cached result for calculation {calculation_id}")
        except Exception as e:
            logger.warning(f"Failed to cache result: {e}")
    
    def process_calculations(self):
        """Process all pending yield calculations"""
        pending_calculations = self.get_pending_calculations()
        
        if not pending_calculations:
            logger.info("No pending calculations found")
            return
        
        logger.info(f"Processing {len(pending_calculations)} pending calculations")
        
        for calculation in pending_calculations:
            calculation_id = calculation['id']
            
            # Retry logic with exponential backoff
            for retry in range(self.max_retries):
                try:
                    logger.info(f"Processing calculation {calculation_id} (attempt {retry + 1})")
                    
                    # Calculate yield
                    result = self.calculate_yield(calculation)
                    
                    # Update database
                    update_success = self.update_calculation(calculation_id, result)
                    
                    if update_success:
                        # Cache successful results
                        if result.get('status') == 'completed':
                            self.cache_result(calculation_id, result)
                        break
                    else:
                        raise Exception("Failed to update calculation in database")
                        
                except Exception as e:
                    logger.error(f"Attempt {retry + 1} failed for calculation {calculation_id}: {e}")
                    
                    if retry == self.max_retries - 1:
                        # Final attempt failed, mark as failed
                        self.update_calculation(calculation_id, {
                            'error': str(e),
                            'status': 'failed'
                        })
                    else:
                        # Wait before retry
                        backoff_delay = self.exponential_backoff(retry)
                        time.sleep(backoff_delay)
    
    def run(self):
        """Main worker loop"""
        logger.info(f"Yield calculation worker started. Interval: {self.interval}s")
        
        while True:
            try:
                start_time = time.time()
                
                self.process_calculations()
                
                # Calculate sleep time to maintain consistent interval
                processing_time = time.time() - start_time
                sleep_time = max(0, self.interval - processing_time)
                
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    
            except KeyboardInterrupt:
                logger.info("Worker stopped by user")
                break
            except Exception as e:
                logger.error(f"Unexpected error in worker loop: {e}")
                time.sleep(self.interval)  # Wait before retrying

if __name__ == "__main__":
    # Validate required environment variables
    required_vars = ['SUPABASE_URL', 'SUPABASE_KEY']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        exit(1)
    
    worker = YieldCalculationWorker()
    worker.run()
