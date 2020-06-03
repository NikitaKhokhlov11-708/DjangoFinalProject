from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.shortcuts import render

from URLproject import models


def index(request):
    url_error = False
    url_input = ""
    shortened_url = ""

    if request.method == "POST":
        validator = URLValidator()
        try:
            url_input = request.POST.get("url", None)
            if not url_input:
                url_error = True
            else:
                validator(url_input)
        except ValidationError:
            url_error = True

        if not url_error:
            link_db = models.Link()
            link_db.link = url_input
            link_db.hash = link_db.get_hash()
            link_db.save()
            shortened_url = request.build_absolute_uri(link_db.hash)
            url_input = ""

    return render(request, "index.html",
                  {"error": url_error, "url": url_input, "shorturl": shortened_url})
