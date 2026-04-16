Rensar bort data äldre än x dagar från opencti community edition som inte har denna funktion.


services:
  opencti-cleaner:
    image: ghcr.io/ditt-användarnamn/opencti-janitor:latest
    container_name: opencti-cleaner
    environment:
      - OPENCTI_URL=http://opencti:4000
      - OPENCTI_TOKEN=ditt-hemliga-admin-token
      - RETENTION_DAYS=180
    restart: always
