import os
import time
from pycti import OpenCTIApiClient
from datetime import datetime, timedelta, timezone

# Inställningar som hämtas från miljövariabler i Dockhand
api_url = os.getenv("OPENCTI_URL", "http://opencti:8080")
api_token = os.getenv("OPENCTI_TOKEN")
retention_days = int(os.getenv("RETENTION_DAYS", "180"))

if not api_token:
    raise ValueError("FEL: Miljövariabeln OPENCTI_TOKEN saknas!")

# Initiera klienten
client = OpenCTIApiClient(api_url, api_token)

def purge():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"--- Startar rensning {now} ---")
    
    # Beräkna datumgränsen
    cutoff = datetime.now(timezone.utc) - timedelta(days=retention_days)
    print(f"Letar efter objekt skapade före: {cutoff.isoformat()}")
    
    # Typer av objekt som oftast tar mest plats
    types = ["Indicator", "Stix-Cyber-Observable", "Report"]
    
    for obj_type in types:
        print(f"Kollar typ: {obj_type}...")
        
        # Ny filtersyntax för OpenCTI 6.x+
        new_filters = {
            "mode": "and",
            "filters": [],
            "filterGroups": [
                {
                    "mode": "and",
                    "filters": [
                        {
                            "key": "created_at",
                            "values": [cutoff.isoformat()],
                            "operator": "lt" # 'lt' står för 'less than' (äldre än)
                        }
                    ]
                }
            ]
        }

        try:
            # Hämta listan med objekt
            items = client.stix_domain_object.list(
                types=[obj_type],
                filters=new_filters,
                first=100 # Vi tar 100 åt gången för att inte överbelasta API:et
            )
            
            if not items:
                print(f"Inga gamla {obj_type} hittades.")
                continue

            print(f"Hittade {len(items)} st {obj_type} att radera.")
            
            for item in items:
                item_name = item.get("name") or item.get("observable_value") or item["id"]
                try:
                    client.stix_domain_object.delete(id=item['id'])
                    print(f"Raderat: {item_name}")
                except Exception as e:
                    print(f"Kunde inte radera {item_name}: {str(e)}")
                    
        except Exception as e:
            print(f"Fel vid listning av {obj_type}: {str(e)}")
    
    print(f"--- Rensning klar {datetime.now().strftime('%H:%M:%S')} ---")
    print(f"Väntar 24 timmar till nästa körning...")

if __name__ == "__main__":
    # En liten delay vid start så OpenCTI hinner vakna om hela stacken startas samtidigt
    time.sleep(10) 
    while True:
        try:
            purge()
        except Exception as e:
            print(f"Ett oväntat fel uppstod i loopen: {str(e)}")
        
        # Vänta 1 dygn
        time.sleep(86400)