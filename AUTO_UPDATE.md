# 🔄 Sistema di Aggiornamento Dati Automatico

Il Fantasy Assistant ora include un **sistema completo di aggiornamento automatico dei dati** che raccoglie informazioni da fonti internet in tempo reale!

## ✨ Nuove Funzionalità

### 📡 Web Scrapers Implementati

1. **Fantacalcio.it Scraper**
   - Dati completi di tutti i giocatori Serie A
   - Statistiche stagione corrente
   - Valori di mercato
   - Info su infortuni e squalifiche

2. **Gazzetta dello Sport Scraper**
   - Voti delle partite settimanali
   - Aggiornamenti infortuni in tempo reale
   - Difficoltà degli incontri
   - Probabili formazioni

3. **Data Aggregator**
   - Combina dati da più fonti
   - Validazione automatica
   - Gestione conflitti
   - Statistiche di aggiornamento

### ⏰ Aggiornamenti Automatici

Il sistema aggiorna automaticamente i dati con questi schedule:

| Task | Quando | Cosa |
|------|--------|------|
| **Dati Giocatori** | Ogni giorno alle 2:00 | Aggiorna tutti i dati dei giocatori |
| **Voti Partite** | Lunedì mattina ore 6:00 | Aggiorna voti post-weekend |
| **Infortuni** | 3 volte al giorno (9:00, 15:00, 21:00) | Controlla infortuni/squalifiche |

### 🎮 API per Aggiornamenti Manuali

Nuovi endpoint API disponibili:

```bash
# Aggiorna tutti i dati
POST /api/data/update/all

# Aggiorna solo infortuni
POST /api/data/update/injuries

# Aggiorna voti giornata specifica
POST /api/data/update/ratings/15

# Controlla stato aggiornamenti
GET /api/data/update/status
```

## 🚀 Come Attivare

### Opzione 1: Docker (Raccomandato)

Aggiungi a `docker-compose.yml`:

```yaml
services:
  celery-worker:
    build: .
    command: celery -A app.tasks worker --loglevel=info
    depends_on:
      - redis
      - db
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=redis://redis:6379

  celery-beat:
    build: .
    command: celery -A app.tasks beat --loglevel=info
    depends_on:
      - redis
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=redis://redis:6379
```

Poi:
```bash
docker-compose up -d
```

### Opzione 2: Manuale

```bash
# Terminale 1: Worker
cd backend
celery -A app.tasks worker --loglevel=info

# Terminale 2: Scheduler
celery -A app.tasks beat --loglevel=info
```

## 📊 File Creati

```
backend/app/scrapers/
├── fantacalcio_scraper.py    # Scraper Fantacalcio.it
├── gazzetta_scraper.py       # Scraper Gazzetta
├── data_aggregator.py        # Aggregatore dati
└── README.md                 # Documentazione scrapers

backend/app/
├── tasks.py                  # Task Celery automatici
└── api/data_update.py        # API per aggiornamenti manuali
```

## ⚠️ Note Importanti

### Scraping Responsabile

I scrapers implementati seguono best practices:
- ✅ Rate limiting (pause tra richieste)
- ✅ User-Agent appropriato
- ✅ Gestione errori robusta
- ✅ Logging completo

**Importante**: Prima di usare in produzione:
1. Verifica il `robots.txt` dei siti
2. Leggi i Terms of Service
3. Considera API ufficiali se disponibili
4. Implementa caching per ridurre richieste

### Manutenzione

I selettori HTML potrebbero cambiare quando i siti si aggiornano. Se gli scrapers smettono di funzionare:

1. Controlla i log Celery
2. Ispeziona HTML dei siti target
3. Aggiorna i selettori CSS
4. Testa con `pytest`

## 🎯 Esempio di Utilizzo

### Da Frontend

Aggiungi ai servizi React:

```typescript
// src/services/dataUpdate.ts
import api from '../config/api';

export const triggerDataUpdate = async () => {
  const response = await api.post('/data/update/all');
  return response.data;
};

export const getUpdateStatus = async () => {
  const response = await api.get('/data/update/status');
  return response.data;
};
```

### Da Python

```python
from app.scrapers.data_aggregator import update_all_data
from app.db.database import SessionLocal

db = SessionLocal()
try:
    stats = update_all_data(db)
    print(f"Aggiornati: {stats['updated']} giocatori")
    print(f"Creati: {stats['created']} nuovi giocatori")
finally:
    db.close()
```

## 📈 Prossimi Passi

Per utilizzare al meglio il sistema:

1. **Configura Celery** con Docker o manualmente
2. **Testa gli scrapers** manualmente prima
3. **Monitora i log** per eventuali errori
4. **Personalizza gli schedule** se necessario
5. **Aggiungi altre fonti** dati se disponibili

## 🔍 Troubleshooting

**Celery non si avvia?**
```bash
# Verifica Redis
redis-cli ping

# Verifica configurazione
celery -A app.tasks inspect active
```

**Nessun dato aggiornato?**
```bash
# Trigger manuale via API
curl -X POST http://localhost:8000/api/data/update/all \
  -H "Authorization: Bearer YOUR_TOKEN"

# Controlla status
curl http://localhost:8000/api/data/update/status \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 📚 Documentazione Completa

Vedi `backend/app/scrapers/README.md` per:
- Dettagli tecnici scrapers
- Configurazione avanzata
- Best practices scraping
- Troubleshooting dettagliato

---

✨ **Ora il tuo Fantasy Assistant si aggiorna automaticamente con dati reali!**
