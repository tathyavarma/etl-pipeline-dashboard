# ETL Pipeline — Production Folder Structure

```
etl_pipeline/                          # ← Project root
│
├── .github/
│   └── workflows/
│       ├── ci.yml                     # CI: lint, test, build
│       └── deploy.yml                 # CD: deploy to Render/AWS
│
├── backend/                           # ← Django application root
│   ├── config/                        # Project-level Django config
│   │   ├── __init__.py
│   │   ├── settings/
│   │   │   ├── __init__.py
│   │   │   ├── base.py                # Shared settings
│   │   │   ├── development.py         # Dev overrides
│   │   │   ├── production.py          # Prod overrides
│   │   │   └── testing.py             # Test overrides
│   │   ├── urls.py                    # Root URL conf
│   │   ├── wsgi.py
│   │   └── asgi.py
│   │
│   ├── apps/
│   │   ├── core/                      # Shared utilities, base models
│   │   │   ├── __init__.py
│   │   │   ├── models.py              # Abstract base models
│   │   │   ├── exceptions.py          # Custom exceptions
│   │   │   ├── pagination.py          # DRF pagination classes
│   │   │   ├── permissions.py         # Custom DRF permissions
│   │   │   └── utils.py               # Common helpers
│   │   │
│   │   ├── products/                  # Product domain
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── models.py              # Product, Category, PriceHistory
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── filters.py             # django-filter FilterSets
│   │   │   ├── signals.py
│   │   │   └── tests/
│   │   │       ├── __init__.py
│   │   │       ├── test_models.py
│   │   │       ├── test_views.py
│   │   │       └── factories.py       # factory_boy factories
│   │   │
│   │   ├── sources/                   # Data source registry
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── models.py              # Source, SourceConfig
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   └── tests/
│   │   │
│   │   ├── etl/                       # ETL job management
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── models.py              # ETLJob, ETLJobLog
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   └── tests/
│   │   │
│   │   └── analytics/                 # Analytics endpoints
│   │       ├── __init__.py
│   │       ├── apps.py
│   │       ├── views.py               # Aggregate query views
│   │       ├── serializers.py
│   │       ├── urls.py
│   │       └── tests/
│   │
│   ├── etl_engine/                    # ← Core ETL engine (no Django deps)
│   │   ├── __init__.py
│   │   │
│   │   ├── extractors/                # Extraction layer
│   │   │   ├── __init__.py
│   │   │   ├── base.py                # Abstract BaseExtractor
│   │   │   ├── api_connector.py       # REST API extractor
│   │   │   ├── html_scraper.py        # BeautifulSoup scraper
│   │   │   ├── file_parser.py         # CSV/XML parser
│   │   │   └── registry.py            # Extractor registry/factory
│   │   │
│   │   ├── transformers/              # Transformation layer
│   │   │   ├── __init__.py
│   │   │   ├── base.py                # Abstract BaseTransformer
│   │   │   ├── normalizer.py          # Schema normalization
│   │   │   ├── validator.py           # Data validation rules
│   │   │   ├── cleaner.py             # Data cleaning logic
│   │   │   └── schema.py              # Pydantic/dataclass schemas
│   │   │
│   │   ├── loaders/                   # Loading layer
│   │   │   ├── __init__.py
│   │   │   ├── base.py                # Abstract BaseLoader
│   │   │   ├── postgres_loader.py     # Bulk insert + dedup
│   │   │   └── version_tracker.py     # Price history tracking
│   │   │
│   │   └── pipeline.py                # Orchestrates E→T→L
│   │
│   ├── tasks/                         # Celery tasks
│   │   ├── __init__.py
│   │   ├── celery.py                  # Celery app config
│   │   ├── etl_tasks.py               # ETL job tasks
│   │   ├── scheduled.py               # Periodic task schedule
│   │   └── utils.py                   # Task helpers
│   │
│   ├── management/
│   │   └── commands/
│   │       ├── run_etl.py
│   │       ├── fetch_books.py
│   │       ├── fetch_shopify.py
│   │       └── clean_data.py
│   │
│   ├── static/                        # Django static files
│   ├── media/                         # User uploads (CSV/XML)
│   ├── templates/                     # Django templates (fallback)
│   ├── logs/                          # Log files (gitignored)
│   ├── manage.py
│   └── requirements/
│       ├── base.txt
│       ├── development.txt
│       └── production.txt
│
├── frontend/                          # ← React frontend (Vite)
│   ├── public/
│   ├── src/
│   │   ├── api/                       # Axios API clients
│   │   ├── components/                # Reusable components
│   │   ├── pages/                     # Route-level pages
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Products.jsx
│   │   │   ├── Sources.jsx
│   │   │   └── Jobs.jsx
│   │   ├── hooks/                     # Custom React hooks
│   │   ├── store/                     # Zustand/Redux state
│   │   └── utils/
│   ├── package.json
│   └── vite.config.js
│
├── nginx/
│   ├── nginx.conf                     # Production Nginx config
│   └── nginx.dev.conf                 # Dev config
│
├── docker/
│   ├── django/
│   │   ├── Dockerfile
│   │   └── entrypoint.sh
│   ├── celery/
│   │   ├── Dockerfile
│   │   └── entrypoint.sh
│   └── frontend/
│       └── Dockerfile
│
├── scripts/
│   ├── start-dev.sh
│   ├── run-tests.sh
│   └── deploy.sh
│
├── docker-compose.yml                 # Development
├── docker-compose.prod.yml            # Production
├── .env.example
├── .env                               # Never commit!
├── .gitignore
├── Makefile                           # Dev shortcuts
└── README.md
```
