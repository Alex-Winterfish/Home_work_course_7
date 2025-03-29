import re
from rest_framework.serializers import ValidationError


class UrlValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = re.compile(r"^https?:\/\/(www\.)?youtube\.com\/.+$")
        url_field = dict(value).get(self.field)
        if not bool(reg.match(url_field)):
            raise ValidationError(
                detail="video_url can only be a link to wwww.youtube.com"
            )
