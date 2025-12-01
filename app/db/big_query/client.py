from typing import Optional
from google.cloud import bigquery
from google.cloud.bigquery import Client
import logging

logging.basicConfig(level=logging.INFO)

class BigQueryClient:
    """
    Manages the singleton BigQuery client connection.
    Uses Application Default Credentials (ADC) for authentication.
    """
    def __init__(self, project_id: str = None):
        self._client: Optional[Client] = None
        self.project_id = project_id
        self._initialize_client()

    def _initialize_client(self):
        """Initializes the BigQuery client."""
        try:
            # ADC automatically handles authentication on Cloud Run
            # by using the attached Service Account.
            self._client = bigquery.Client(project=self.project_id)
            logging.info("BigQuery client initialized successfully using ADC.")
        except Exception as e:
            logging.error(f"Error initializing BigQuery client: {e}")
            raise RuntimeError("Could not initialize BigQuery client. Check credentials or service account permissions.")

    def close(self):
        """
        Closes the underlying BigQuery client connection.
        """
        if self._client:
            self._client.close()
            self._client = None
            logging.info("BigQuery client connection closed.")

    def get_client(self) -> Client:
        """Returns the initialized BigQuery client instance."""
        if self._client is None:
            # Should not happen if _initialize_client succeeds, but good for safety
            self._initialize_client()
        return self._client