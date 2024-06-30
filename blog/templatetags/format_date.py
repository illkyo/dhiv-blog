from django import template
from django.utils import timezone
from django.utils.timesince import timesince
from datetime import timedelta
from django.utils.translation import ngettext_lazy as __
from django.utils.translation import gettext_lazy as _

register = template.Library()

dhivehi_time_strings = {
    "year": __("%(num)d އަހަރު", "%(num)d އަހަރު", "num"),
    "month": __("%(num)d މަސް", "%(num)d މަސް", "num"),
    "week": __("%(num)d ހަފްތާ", "%(num)d ހަފްތާ", "num"),
    "day": __("%(num)d ދުވަސް", "%(num)d ދުވަސް", "num"),
    "hour": __("%(num)d ގަޑިއިރު", "%(num)d ގަޑިއިރު", "num"),
    "minute": __("%(num)d މިނެޓް", "%(num)d މިނެޓް", "num"),
}

def dhivehi_date(date, with_year=False):
    month_names = [
        "ޖެނުއަރީ", "ފެބްރުއަރީ", "މާރޗް", "އޭޕްރިލް", "މޭ", "ޖޫން",
        "ޖުލައި", "އޮގަސްޓު", "ސެޕްޓެމްބަރް", "އޮކްޓޯބަރް", "ނޮވެމްބަރު", "ޑިސެމްބަރް"
    ]
    day = date.day
    month = month_names[date.month - 1]
    year = date.year
    
    if with_year:
        return _(f"{year} {day} {month}")
    
    return _(f"{day} {month}")
    

@register.filter
def format_date(post_date): # Does not account for months with 31 days and February. And Leap Years. Yet.
    now = timezone.now()
    time_since = now - post_date
    month = timedelta(days=30)
    year = timedelta(days=365)
    
    if time_since > year:
        return dhivehi_date(post_date, with_year=True)
    elif time_since > month:
        return dhivehi_date(post_date)
    else:
        return _(timesince(post_date, now, time_strings=dhivehi_time_strings, depth=1) + ' ކުރިން')