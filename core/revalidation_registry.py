# core/revalidation_registry.py
# Import models from other apps
from creations.models import Category, Creation
from experience.models import Experience
from profiles.models import Profile
from projects.models import Project, ProjectGallery
from qualifications.models import Qualification
from services.models import Service
from settings.models import Setting, SEOPageSetting, DisplaySetting, SitemapSetting
from skills.models import Skill, SubSkill
from socialmedia.models import SocialMedia

REVALIDATION_MODELS = [
    Category,
    Creation,
    Experience,
    Profile,
    Project,
    ProjectGallery,
    Qualification,
    Service,
    Setting,
    SEOPageSetting,
    DisplaySetting,
    SitemapSetting,
    Skill,
    SubSkill,
    SocialMedia,
]