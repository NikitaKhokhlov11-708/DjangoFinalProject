from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.shortcuts import render, redirect

from URLproject import models


def index(request):
    url_error = False
    url_input = ""
    short_url = ""

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
            link_db.original = url_input
            link_db.short = request.build_absolute_uri(link_db.get_hash())
            link_db.ip = request.META.get('REMOTE_ADDR')
            # link_db.ip = request.META.get('HTTP_X_FORWARDED_FOR')
            link_db.save()
            short_url = link_db.short

    return render(request, "index.html",
                  {"error": url_error, "shorturl": short_url})


def all(request):
    query_results = models.Link.objects.all()
    return render(request, "all.html",
                  {"query_results": query_results})


def delete(request, id):
    employee = models.Link.objects.get(id=id)
    employee.delete()
    return redirect("/all")
