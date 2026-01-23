from django import template
from django.urls import reverse

from django_starter.contrib.notifications.models import Notification

register = template.Library()


@register.inclusion_tag("django_starter/notifications/_dropdown.html", takes_context=True)
def notifications_dropdown(context, limit: int = 5):
    request = context.get("request")
    user = getattr(request, "user", None)

    if not user or not getattr(user, "is_authenticated", False):
        return {
            "recent": [],
            "unread_count": 0,
            "index_url": reverse("djs_notifications:index"),
        }

    qs = Notification.objects.filter(user=user).order_by("-created_time")
    return {
        "recent": list(qs[:limit]),
        "unread_count": qs.filter(read_time__isnull=True).count(),
        "index_url": reverse("djs_notifications:index"),
        "mark_all_read_url": reverse("djs_notifications:mark-all-read"),
    }

