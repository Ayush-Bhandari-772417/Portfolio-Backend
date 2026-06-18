# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Setup
```bash
# Create virtual environment (if not exists)
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (copy from .env.example if needed)
cp .env.example .env  # Then edit .env with your values
```

### Database
```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Development Server
```bash
# Run development server
python manage.py runserver

# Run on specific port
python manage.py runserver 8000
```

### Testing
```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test projects

# Run specific test class
python manage.py test projects.tests.ProjectModelTest

# Run specific test method
python manage.py test projects.tests.ProjectModelTest.test_project_creation
```

### Static Files
```bash
# Collect static files (for production)
python manage.py collectstatic
```

### Linting/Formatting
```bash
# Check code formatting (if using black)
black --check .

# Format code (if using black)
black .

# Import sorting (if using isort)
isort --check .
isort .
```

## Code Architecture

### Project Structure
This Django project follows a modular app structure where each portfolio section is a separate app:
- **apps/**: Contains all Django apps (users, projects, creations, experience, etc.)
- **config/**: Project settings and URL configuration
- **media/**: User-uploaded files (managed by Supabase storage)
- **staticfiles/**: Collected static files for production

### Key Applications
1. **users**: Custom User model extending AbstractUser with bio, profile_image, social_links
2. **projects**: Main portfolio projects with gallery images, technologies, features
3. **creations**: Similar to projects but for different types of work
4. **experience**: Work experience and employment history
5. **skills**: Technical skills and proficiency levels
6. **education**: Academic background and certifications
7. **services**: Services offered
8. **testimonials**: Client testimonials and reviews
9. **contact**: Contact form handling
10. **public_api**: Public endpoints accessible without authentication
11. **seo**: SEO metadata management
12. **subscription**: Newsletter and subscription management

### Authentication System
- Custom JWT authentication using cookies (`config.authentication.CookieJWTAuthentication`)
- Access token: 15 minutes, Refresh token: 12 hours
- Tokens stored in HTTP-only cookies for XSS protection
- Custom admin permission: `config.permissions.IsSecureAdmin`

### Storage System
- Primary storage: Supabase S3-compatible storage via `core.storage.SupabaseStorage`
- Static files: WhiteNoise for serving and compression
- Environment variables for Supabase credentials:
  - `SUPABASE_URL`, `SUPABASE_BUCKET`, `SUPABASE_S3_ACCESS_KEY`, `SUPABASE_S3_SECRET_KEY`

### API Structure
- All API endpoints under `/api/`
- Public endpoints: `/api/public/` and `/api/v1/public/`
- SEO endpoints: `/api/seo/`
- Admin/auth endpoints: `/api/admin/auth/` (custom cookie-based views)
- Each app has its own `urls.py` included in `config/urls.py`

### Environment Variables
Critical variables in `.env`:
- `SECRET_KEY`: Django secret key
- `DEBUG`: Boolean for development/production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- Database: `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
- Supabase: `SUPABASE_URL`, `SUPABASE_BUCKET`, `SUPABASE_S3_ACCESS_KEY`, `SUPABASE_S3_SECRET_KEY`
- CORS: `CORS_ALLOWED_ORIGINS` (for Next.js frontend)
- Frontend revalidation: `FRONTEND_REVALIDATE_URL`

### Common Development Tasks
1. **Adding a new model**: 
   - Create model in app's `models.py`
   - Run `makemigrations` and `migrate`
   - Register in admin if needed (`admin.py`)
   - Create serializer (`serializers.py`)
   - Create viewset/view (`views.py`)
   - Add URLs (`urls.py`)

2. **Modifying authentication**: 
   - Check `config/authentication.py` for custom auth
   - Review `config/permissions.py` for custom permissions
   - Update `REST_FRAMEWORK` settings in `settings.py`

3. **Working with media/files**:
   - Files automatically go to Supabase storage via `core.storage.SupabaseStorage`
   - ImageField/FileField in models handle uploads
   - Check `settings.py` for STORAGES configuration

4. **Updating CORS settings**:
   - Modify `CORS_ALLOWED_ORIGINS` in `.env`
   - Update `settings.py` if needed for development

### Important Files
- `config/settings.py`: Main Django configuration
- `config/urls.py`: Project URL routing
- `manage.py`: Django entry point
- `requirements.txt`: Python dependencies
- `.env`: Environment variables (not in version control)
- `core/storage.py`: Custom Supabase storage backend

### Debugging Tips
1. **Authentication issues**: Check cookie settings and JWT configuration
2. **Media upload failures**: Verify Supabase credentials and bucket permissions
3. **CORS errors**: Ensure `CORS_ALLOWED_ORIGINS` includes frontend URL
4. **Database connection**: Verify Supabase PostgreSQL credentials and network access