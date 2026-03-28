# core/signals.py

from django.db.models.signals import post_save, post_delete

from core.utils.revalidate_paths import build_path_payload
from core.utils.revalidate import trigger_revalidation
from core.revalidation_registry import REVALIDATION_MODELS


def _revalidate(instance):
    try:
        payload = build_path_payload(instance)
        trigger_revalidation(**payload)
    except Exception as e:
        print("[REVALIDATION ERROR]", e)


def register_signals(model):

    def handle_save(sender, instance, **kwargs):
        _revalidate(instance)

    def handle_delete(sender, instance, **kwargs):
        _revalidate(instance)

    post_save.connect(handle_save, sender=model, weak=False)
    post_delete.connect(handle_delete, sender=model, weak=False)


for model in REVALIDATION_MODELS:
    register_signals(model)