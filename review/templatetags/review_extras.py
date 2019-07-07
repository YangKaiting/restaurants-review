from django import template
from django.utils import timezone

register = template.Library()

@register.filter(expects_localtime=True)
def time_from_now(review_date):
    now = timezone.localtime()
    time_passed = now - review_date
    if time_passed.days > 1:
        # show days ago
        return str(time_passed.days)+" days ago"
    else:
        if time_passed.seconds/3600 > 1:
            # show hours ago
            return str(round(time_passed.seconds/3600//1))+" hours ago"
        else:
            # show minutes ago
            return str(round(time_passed.seconds/60//1)) + " mins ago"   

@register.filter
def times(number):
    return range(number)