# Public Views Standardization TODO

## Completed:
- [x] Created config/public/base.py with PublicBaseReadOnlyViewSet, PublicBaseCreateViewSet
- [x] Refactored all public/views.py to inherit bases

## Pending:
- [ ] cd backend && python manage.py check
- [ ] Test public endpoints:
  - Read-only (projects, skills etc.): GET list/detail, filter/search/pagination, is_public filter
  - Write-only (contacts/hires/subscription): POST create (throttle/reCAPTCHA)
  - Special: creations ImageUploadView (upload test), experience dashboard_stats
- [ ] Verify SEO: fast querysets, AllowAny, no auth required
- [ ] python manage.py runserver

## Notes:
- Write-only (contacts/hires/subscription): PublicBaseCreateViewSet (CreateModelMixin only)
- Read-only: PublicBaseReadOnlyViewSet
- All custom logic preserved
- Global admin perms overridden by explicit AllowAny
