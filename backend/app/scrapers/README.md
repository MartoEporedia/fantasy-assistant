# Auto Data Update System

This directory contains web scrapers and data aggregators for automatically fetching player data from Italian fantasy football websites.

## Available Scrapers

### 1. Fantacalcio.it Scraper (`fantacalcio_scraper.py`)
- **Purpose**: Fetch comprehensive player database with statistics
- **Data collected**:
  - Player name, team, role, age, nationality
  - Current season stats (goals, assists, matches played)
  - Average ratings and fantasy points
  - Market value estimates
  - Detailed player information (injuries, suspensions)

### 2. Gazzetta dello Sport Scraper (`gazzetta_scraper.py`)
- **Purpose**: Get real-time match ratings and updates
- **Data collected**:
  - Weekly player ratings and votes
  - Injury and suspension updates
  - Fixture difficulty ratings
  - Probable lineups

### 3. Data Aggregator (`data_aggregator.py`)
- **Purpose**: Combine and validate data from multiple sources
- **Features**:
  - Smart merging of data from different sources
  - Automatic player matching by name
  - Data validation and error handling
  - Update statistics tracking

## Automatic Updates

### Celery Tasks (`app/tasks.py`)

The system automatically updates data on these schedules:

1. **Full Player Data Update**
   - **When**: Daily at 2:00 AM
   - **What**: Complete refresh of all player data
   - **Sources**: Fantacalcio.it

2. **Match Ratings Update**
   - **When**: Monday mornings at 6:00 AM
   - **What**: Update player ratings after weekend matches
   - **Sources**: Gazzetta dello Sport

3. **Injury Status Checks**
   - **When**: 3 times daily (9 AM, 3 PM, 9 PM)
   - **What**: Check for injury/suspension updates
   - **Sources**: Gazzetta dello Sport

## Manual Updates via API

You can trigger manual updates using these endpoints:

### Update All Data
```bash
POST /api/data/update/all
Authorization: Bearer <token>
```

### Update Injuries Only
```bash
POST /api/data/update/injuries
Authorization: Bearer <token>
```

### Update Specific Matchday Ratings
```bash
POST /api/data/update/ratings/{matchday}
Authorization: Bearer <token>
```

### Check Update Status
```bash
GET /api/data/update/status
Authorization: Bearer <token>
```

## Running Celery Workers

To enable automatic updates, start Celery workers:

### Start Celery Worker
```bash
cd backend
celery -A app.tasks worker --loglevel=info
```

### Start Celery Beat (Scheduler)
```bash
celery -A app.tasks beat --loglevel=info
```

### Or run both together
```bash
celery -A app.tasks worker --beat --loglevel=info
```

## Docker Setup

Add to `docker-compose.yml`:

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
      - db
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=redis://redis:6379
```

## Important Notes

### Legal & Ethical Scraping

⚠️ **Important**: Web scraping must be done responsibly:

1. **Respect robots.txt**: Always check and follow the website's robots.txt file
2. **Rate limiting**: The scrapers include delays to avoid overloading servers
3. **Terms of Service**: Ensure you're allowed to scrape the website
4. **Data ownership**: Respect copyright and data ownership
5. **Use official APIs when available**: If a website provides an API, use it instead

### Reliability

- Scrapers are based on HTML structure which can change
- Monitor for errors and update selectors when websites change
- Consider using official APIs when available
- Implement fallback data sources

### Performance

- Updates run in background tasks
- Use Redis for caching frequently accessed data
- Schedule intensive updates during low-traffic hours
- Monitor database size and performance

## Troubleshooting

### Scraper Not Working

1. **Check HTML structure**: Websites may have changed their layout
   ```python
   # Update selectors in scraper files
   player_rows = soup.find_all('tr', class_='NEW-CLASS-NAME')
   ```

2. **Check network connectivity**
   ```bash
   curl https://www.fantacalcio.it
   ```

3. **Check logs**
   ```bash
   # View Celery logs
   tail -f celery.log
   ```

### No Data Updates

1. **Verify Celery is running**
   ```bash
   celery -A app.tasks inspect active
   ```

2. **Check Redis connection**
   ```bash
   redis-cli ping
   ```

3. **Manually trigger update via API** to test
   ```bash
   curl -X POST http://localhost:8000/api/data/update/all \
     -H "Authorization: Bearer <token>"
   ```

## Future Enhancements

- [ ] Add more data sources (transfermarkt, whoscored, etc.)
- [ ] Implement machine learning for data validation
- [ ] Add data quality scoring
- [ ] Create data reconciliation dashboard
- [ ] Implement webhook notifications for updates
- [ ] Add support for historical data archiving

## Contributing

When adding new scrapers:

1. Follow the existing scraper structure
2. Include error handling and logging
3. Add rate limiting (minimum 100ms between requests)
4. Document the data schema
5. Add tests for parsing functions
6. Update this README
