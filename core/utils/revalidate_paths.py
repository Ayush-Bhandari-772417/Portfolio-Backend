# apps/core/utils/revalidate_paths.py

# =========================================================
# FILE: backend/core/utils/revalidate_paths.py
#
# FRONTEND ROUTES:
#   /
#   /projects/
#   /projects/{slug}/
#   /creations/
#   /creations/{type}/
#   /creations/{type}/{slug}/
#
# BACKEND ENDPOINTS:
#   /api/public/bootstrap/
#   /api/public/projects/
#   /api/public/projects/{slug}
#   /api/public/creations/
#   /api/public/creations/{slug}
#
# PURPOSE:
# Generate frontend paths to revalidate after backend changes.
# Hybrid revalidation system:
#   - Path-based (precise page invalidation)
#   - Tag-based (scalable data invalidation)
#
# IMPORTANT:
# Bootstrap endpoint is used across ALL pages:
# - Footer (social media, settings)
# - Recommendation logic (projects/creations count)
#
# => Therefore, most updates affect ALL routes.
#
# STRATEGY:
# - Always revalidate "/" because it depends on bootstrap data
# - Revalidate list + detail pages selectively
# - Avoid redundant or invalid paths
# =========================================================


# =========================================================
# COMMON HELPERS
# =========================================================

def _unique(paths):
    """Remove duplicates while preserving clean output."""
    return list(set(paths))


# =========================================================
# GLOBAL BASE PATHS
# =========================================================

def base_paths():
    """
    Core paths affected by global/bootstrap data changes.
    """
    return [
        "/",               # homepage (depends on bootstrap)
        "/projects/",      # project listing
        "/creations/",     # creation listing
    ]


# =========================================================
# TAG DEFINITIONS (IMPORTANT)
# =========================================================

def base_tags():
    """
    Global tags used across app.
    """
    return [
        "bootstrap",   # footer, settings, SEO, profile
    ]


# =========================================================
# CREATION PATHS
# =========================================================

def build_creation_paths(creation):
    """
    Generate all frontend paths affected by a Creation update.

    Affects:
    - homepage (/)
    - creation listing (/creations/)
    - type listing (/creations/{type}/)
    - detail page (/creations/{type}/{slug}/)
    """

    paths = base_paths()
    tags = base_tags() + ["creations"]

    if not creation:
        return {
            "paths": _unique(paths),
            "tags": _unique(tags),
        }

    # Type (e.g., blog, poem, story)
    creation_type = getattr(creation, "type", None)
    slug = getattr(creation, "slug", None)

    # Type listing page
    if creation_type:
        paths.append(f"/creations/{creation_type}/")
        tags.append(f"creations:type:{creation_type}")

    # Detail page
    if creation_type and slug:
        paths.append(f"/creations/{creation_type}/{slug}/")
        tags.append(f"creation:{slug}")

    return {
        "paths": _unique(paths),
        "tags": _unique(tags),
    }


# =========================================================
# PROJECT PATHS
# =========================================================

def build_project_paths(project):
    """
    Generate all frontend paths affected by a Project update.

    Affects:
    - homepage (/)
    - project listing (/projects/)
    - detail page (/projects/{slug}/)
    """

    paths = base_paths()
    tags = base_tags() + ["projects"]

    if not project:
        return {
            "paths": _unique(paths),
            "tags": _unique(tags),
        }

    slug = getattr(project, "slug", None)

    if slug:
        paths.append(f"/projects/{slug}/")
        tags.append(f"project:{slug}")

    return {
        "paths": _unique(paths),
        "tags": _unique(tags),
    }


# =========================================================
# GLOBAL MODELS (BOOTSTRAP)
# =========================================================

def build_global_path():
    return {
        "paths": _unique(base_paths()),
        "tags": _unique(base_tags()),
    }


# =========================================================
# MODEL MAPPING
# =========================================================

MODEL_PATH_BUILDERS = {
    "category": build_creation_paths,
    "creation": build_creation_paths,
    "experience": build_global_path,
    "profile": build_global_path,
    "project": build_project_paths,
    "projectgallery": build_project_paths,
    "qualification": build_global_path,
    "service": build_global_path,
    "setting": build_global_path,
    "seopagesetting": build_global_path,
    "sitemapsetting": build_global_path,
    "displaysetting": build_global_path,
    "skill": build_global_path,
    "subskill": build_global_path,
    "socialmedia": build_global_path,
}


# =========================================================
# MAIN DISPATCHER
# =========================================================

def build_path_payload(instance=None):
    """
    Returns:
    {
        "paths": [...],
        "tags": [...]
    }
    """

    if instance is None:
        return build_global_path()

    model_name = instance.__class__.__name__.lower()
    builder = MODEL_PATH_BUILDERS.get(model_name, build_global_path)

    return builder(instance)
