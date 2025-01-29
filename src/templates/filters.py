from flask import current_app as app
from pytz import timezone


@app.template_filter("apply_tz")
def apply_tz(value):
    if value is None:
        return None
    value = value.replace(tzinfo=timezone("UTC"))
    tz = timezone(app.config.get("TZ"))
    new_value = value.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S %Z")
    return new_value
