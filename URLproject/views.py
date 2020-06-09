from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.validators import URLValidator
from django.db.models import F
from django.http import Http404
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
            link_db.hash = link_db.get_hash()
            link_db.ip = request.META.get('REMOTE_ADDR')
            # link_db.ip = request.META.get('HTTP_X_FORWARDED_FOR')
            link_db.save()
            short_url = request.build_absolute_uri(link_db.hash)

    return render(request, "index.html",
                  {"error": url_error, "shorturl": short_url})


def all(request):
    all_results = models.Link.objects.all().order_by('-redir_num')
    return render(request, "links.html",
                  {"all_results": all_results, "all": "active"})


def mine(request):
    mine_results = models.Link.objects.all().filter(ip=request.META.get('REMOTE_ADDR')).order_by('-redir_num')
    return render(request, "links.html",
                  {"mine_results": mine_results, "mine": "active"})


def delete(request, linkid):
    if models.Link.objects.get(id=linkid).ip == request.META.get('REMOTE_ADDR'):
        link = models.Link.objects.get(id=linkid)
        link.delete()
    return redirect("/mine/")


def redir(request, linkhash):
    try:
        link = models.Link.objects.get(hash=linkhash)
        models.Link.objects.filter(hash=linkhash).update(redir_num=F('redir_num') + 1)
        return redirect(link.original)
    except ObjectDoesNotExist:
        raise Http404("Нет такой ссылки.")
