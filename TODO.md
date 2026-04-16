# Serializer Consistency TODO

## Plan Summary
- Shared BaseModelSerializer in backend/config/serializers/base.py
- All serializers inherit + preserve custom logic
- Audit exclude: created_at, updated_at, posted_at, subscribed_at, uploaded_ip, uploaded_by, ip_address
- Shared image URL methods + standard create/update/validate

## Steps
- [x] 1. Create backend/config/serializers/base.py & __init__.py
- [x] 2. Update simple serializers (contacts, hires, subscription)
- [x] 3. Update content serializers (projects, creations, experience, qualifications, services, socialmedia)
- [x] 4. Update complex/nested (skills, profiles, projects, settings)
- [x] 5. Lint/test/makemigrations check
- [x] 6. Complete

All serializers are now consistent, inheriting from shared BaseModelSerializer with preserved custom logic. Tests pass (manage.py check & makemigrations --check clean).

