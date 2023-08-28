from django import template
import re

register = template.Library()

@register.filter
def youtube_id(value):
    """
    Extracts the video ID from a YouTube URL.
    """
    youtube_id_match = re.search(r'(?<=v=)[^&#]+', value)
    youtube_id_match = youtube_id_match or re.search(r'(?<=be/)[^&#]+', value)
    trailer_id = (youtube_id_match.group(0) if youtube_id_match
                  else None)
    return trailer_id
@register.filter
def split(value, key):
    """
    Splits the value by a key and returns the value of the resultant list at index 1.
    """
    try:
        return value.split(key)[1]
    except:
        return value
@register.filter(name='split_name')
def split_name(name):
    words = name.split()
    if len(words) > 1:
        first_word = words[0].capitalize()
        last_word = words[-1].capitalize()
        return f"{first_word} {last_word}"
    else:
        return words[0].capitalize() if words else ""
@register.filter(name='div')
def div(value, arg):
    try:
        return int(value) / int(arg)
    except (ValueError, ZeroDivisionError):
        return 0