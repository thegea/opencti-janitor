import os
import time
from pycti import OpenCTIApiClient
from datetime import datetime, timedelta, timezone

api_url = os.getenv("OPENCTI_URL")
api_token = os.getenv("OPENCTI_TOKEN")
retention_days = int(os.getenv("RETENTION_DAYS", "180"))

if not api_token:
    raise ValueError("OPENCTI_TOKEN must be set")

client = OpenCTIApiClient(api_url, api_token)

def purge():
    print(f"--- Startar rensning {datetime.now()} ---")
    cutoff = datetime.now(timezone.utc) - timedelta(days=retention_days)
    
    # Typer av objekt som ofta tar plats
    types = ["Indicator", "Stix-Cyber-Observable", "Report"]
    
    for obj_type in types:
        print(f"Kollar {obj_type}...")
        items = client.stix_domain_object.list(
            types=[obj_type],
            filters={
                "mode": "and",
                "filters": [{"key": "created_at", "values": [cutoff.isoformat()], "operator": "lt"}]
            }
        )
        for item in items:
            client.stix_domain_object.delete(id=item['id'])
    
    print("--- Rensning klar ---")

if __name__ == "__main__":
    while True:
        purge()
        time.sleep(86400) # Vänta 24 timmar