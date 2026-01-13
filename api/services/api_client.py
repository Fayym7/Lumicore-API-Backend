
#API client for interacting with the unreliable external API.
import requests
import time
import logging
from typing import Dict, List, Any, Optional, Tuple
from django.conf import settings
import random

logger = logging.getLogger(__name__)

#Client for the unreliable API with retry logic.
class APIClient:
    
    def __init__(self):
        self.base_url = settings.API_BASE_URL
        self.candidate_id = settings.CANDIDATE_ID
        self.session = requests.Session()
        self.session.headers.update({
            'X-Candidate-Id': self.candidate_id,
            'User-Agent': 'DataCleaningApp/1.0'
        })
        
        self.max_retries = settings.MAX_RETRIES
        self.retry_delay = settings.RETRY_DELAY
    
    #Calculate backoff delay
    def _exponential_backoff(self, attempt: int) -> float:
        return self.retry_delay * (2 ** attempt) + random.uniform(0, 0.1)

    # Making HTTP request with backoff retry logic
    def _make_request_with_retry(self, method: str, endpoint: str, **kwargs) -> Optional[requests.Response]:
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(self.max_retries):
            try:
                response = self.session.request(method, url, **kwargs)
                
                # Check for rate limiting or server errors
                if response.status_code == 429:  # Too Many Requests
                    retry_after = int(response.headers.get('Retry-After', 1))
                    logger.warning(f"Rate limited. Retrying after {retry_after} seconds...")
                    time.sleep(retry_after)
                    continue
                
                if response.status_code >= 500:
                    logger.warning(f"Server error {response.status_code}. Retry attempt {attempt + 1}/{self.max_retries}")
                    if attempt < self.max_retries - 1:
                        delay = self._exponential_backoff(attempt)
                        time.sleep(delay)
                    continue
                
                # Simulate slow responses
                if random.random() < 0.15:  # 15% slow responses
                    time.sleep(random.uniform(1, 2))
                
                return response
                
            except requests.exceptions.ConnectionError as e:
                logger.warning(f"Connection error: {e}. Retry attempt {attempt + 1}/{self.max_retries}")
                if attempt < self.max_retries - 1:
                    delay = self._exponential_backoff(attempt)
                    time.sleep(delay)
                continue
            except requests.exceptions.Timeout as e:
                logger.warning(f"Timeout error: {e}. Retry attempt {attempt + 1}/{self.max_retries}")
                if attempt < self.max_retries - 1:
                    delay = self._exponential_backoff(attempt)
                    time.sleep(delay)
                continue
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                if attempt < self.max_retries - 1:
                    delay = self._exponential_backoff(attempt)
                    time.sleep(delay)
                continue
        
        logger.error(f"Failed after {self.max_retries} retries")
        return None
    
    #Fetch data from the API.
    def fetch_data(self, batch_id: int = 1) -> Tuple[Optional[List[Dict]], Optional[str]]:
        endpoint = f"/api/data?batch={batch_id}"
        
        response = self._make_request_with_retry('GET', endpoint)
        
        if response is None:
            return None, "Failed to fetch data after multiple retries"
        
        if response.status_code == 200:
            try:
                data = response.json()
                return data, None
            except ValueError as e:
                logger.error(f"Failed to parse JSON: {e}")
                return None, "Invalid JSON response"
        else:
            logger.error(f"API returned status {response.status_code}: {response.text}")
            return None, f"API error: {response.status_code}"

    #SubmitTING cleaned data to the API.
    def submit_data(self, candidate_name: str, batch_id: int, cleaned_items: List[Dict]) -> Tuple[Optional[Dict], Optional[str]]:
        endpoint = "/api/submit"
        
        payload = {
            'candidate_name': candidate_name,
            'batch_id': batch_id,
            'cleaned_items': cleaned_items
        }
        
        response = self._make_request_with_retry('POST', endpoint, json=payload)
        
        if response is None:
            return None, "Failed to submit data after multiple retries"
        
        if response.status_code == 200:
            try:
                data = response.json()
                return data, None
            except ValueError as e:
                logger.error(f"Failed to parse JSON: {e}")
                return None, "Invalid JSON response"
        else:
            logger.error(f"API returned status {response.status_code}: {response.text}")
            return None, f"API error: {response.status_code}"
    
    #API health check
    def health_check(self) -> Tuple[bool, Optional[str]]:
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200, None
        except Exception as e:
            return False, str(e)