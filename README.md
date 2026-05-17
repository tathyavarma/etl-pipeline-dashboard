# ETL Pipeline — Production-Ready Data Engineering Platform

A full-stack ETL (Extract, Transform, Load) web application built with
Django, DRF, Celery, PostgreSQL, Redis, and React.

## Architecture

```
Data Sources → Extractors → Normalizer → Loader → PostgreSQL
                                                       ↑
Celery Beat (Scheduler) → Celery Workers ──────────────┘
                                                       ↓
                                              DRF REST API
                                                       ↓
                                           React Dashboard
```

## Quick Start (Docker)

```bash
# 1. Clone and configure
git clone https://github.com/yourorg/etl-pipeline
cd etl-pipeline
cp .env.example .env          # Edit as needed

# 2. Start all services
make up

# 3. Seed data
make seed                     # Scrapes Books to Scrape + mock Shopify

# 4. Open in browser
# API:       http://localhost:8000/api/v1/
# Admin:     http://localhost:8000/admin/      (admin / changeme123)
# Frontend:  http://localhost:5173/
# Flower:    http://localhost:5555/
```

## Manual Setup (without Docker)

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements/development.txt
cp .env.example .env          # Edit DATABASE_URL and REDIS_URL

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# In separate terminals:
celery -A tasks.celery worker --loglevel=info
celery -A tasks.celery beat --loglevel=info
```

## Adding a New Data Source

1. Create a source via API or Admin:
```json
POST /api/v1/sources/
{
  "name": "My New Source",
  "source_type": "html",
  "base_url": "https://example.com/products",
  "config": {
    "extra": { "max_pages": 10 },
    "rate_limit_delay": 1.0
  }
}
```

2. Trigger ETL:
```json
POST /api/v1/etl/jobs/trigger/
{ "source_id": "<uuid from step 1>" }
```

3. Monitor in Flower or via API:
```
GET /api/v1/etl/jobs/<job_id>/logs/
```

## ETL Management Commands

```bash
# Run all active sources
python manage.py run_etl --all

# Run specific source
python manage.py run_etl --source "Books to Scrape"

# Fetch specific sources
python manage.py fetch_books --pages 10
python manage.py fetch_shopify --mock

# Data maintenance
python manage.py clean_data --dry-run
python manage.py clean_data
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/token/` | Get JWT token |
| POST | `/api/auth/token/refresh/` | Refresh JWT |
| GET | `/api/v1/products/` | List products (filter/search/paginate) |
| GET | `/api/v1/products/{id}/` | Product detail + price history |
| GET | `/api/v1/products/stats/` | Aggregated stats |
| GET | `/api/v1/products/{id}/price-history/` | Full price history |
| GET | `/api/v1/products/categories/` | All categories |
| GET | `/api/v1/sources/` | List sources |
| POST | `/api/v1/sources/` | Create source |
| POST | `/api/v1/sources/{id}/toggle/` | Toggle active |
| POST | `/api/v1/etl/jobs/trigger/` | Trigger ETL job |
| GET | `/api/v1/etl/jobs/` | List jobs |
| GET | `/api/v1/etl/jobs/{id}/logs/` | Job logs |
| POST | `/api/v1/etl/jobs/{id}/retry/` | Retry failed job |
| GET | `/api/v1/analytics/summary/` | Dashboard summary |
| GET | `/api/v1/analytics/price-trends/` | Price over time |
| GET | `/api/v1/analytics/categories/` | Category distribution |
| GET | `/api/v1/analytics/sources/` | Source comparison |
| GET | `/api/v1/analytics/top-products/` | Top products |

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DJANGO_SECRET_KEY` | Django secret key | **Required** |
| `DATABASE_URL` | PostgreSQL URL | `postgresql://...` |
| `REDIS_URL` | Redis URL | `redis://localhost:6379/0` |
| `DJANGO_DEBUG` | Debug mode | `False` |
| `SHOPIFY_SHOP_URL` | Shopify store domain | *(mock data used if blank)* |
| `SHOPIFY_ACCESS_TOKEN` | Shopify API token | *(mock data used if blank)* |
| `SENTRY_DSN` | Sentry error tracking | *(optional)* |

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Django 4.2, DRF 3.15 |
| Task Queue | Celery 5.4, Redis 7 |
| Database | PostgreSQL 16 |
| Scraping | BeautifulSoup4, lxml, httpx |
| Data Processing | pandas, pydantic |
| Frontend | React 18, Vite, Recharts |
| Serving | Gunicorn, Nginx |
| DevOps | Docker, Docker Compose, GitHub Actions |

## Deployment

### Render
```bash
# Set environment variables in Render dashboard, then:
render deploy
```

### AWS (ECS)
```bash
aws ecr get-login-password | docker login --username AWS --password-stdin $ECR_URL
docker build -t $ECR_URL/etl-pipeline:latest -f docker/django/Dockerfile .
docker push $ECR_URL/etl-pipeline:latest
```

### Railway
```bash
railway up
```

## Project Structure

See `STRUCTURE.md` for the full annotated directory tree.

## License

MIT
