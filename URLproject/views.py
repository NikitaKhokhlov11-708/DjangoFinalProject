from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.validators import URLValidator
from django.db.models import F
from django.http import Http404
from django.shortcuts import render, redirect

from URLproject import models


def index(request):
    """Main page

    :param request: an HttpRequest object that contains metadata about the request
    :return: reloads main page with data
    """
    url_error = False  # Flag that is used to check if the url is valid or not
    url_input = ""  # Variable to store the url input
    short_url = ""  # Variable to store a short url

    # Check if this view was called by pressing the button "Сократить"
    if request.method == "POST":
        validator = URLValidator()
        try:
            url_input = request.POST.get("url", None)
            # If the input url is blank
            if not url_input:
                url_error = True
            else:
                validator(url_input)
        # If the input url is invalid
        except ValidationError:
            url_error = True

        # If url is valid
        if not url_error:
            '''
            try:
                short_url = request.build_absolute_uri(models.Link.objects.get(original=url_input).hash)
            except ObjectDoesNotExist:
                link_db = models.Link()
                link_db.original = url_input
                link_db.hash = link_db.get_hash()
                link_db.ip = request.META.get('REMOTE_ADDR')
                # link_db.ip = request.META.get('HTTP_X_FORWARDED_FOR')
                link_db.save()
                short_url = request.build_absolute_uri(link_db.hash)
            '''
            link_db = models.Link()
            link_db.original = url_input
            link_db.hash = link_db.get_hash()
            link_db.ip = request.META.get('REMOTE_ADDR')  # Get the IP address of the request
            # link_db.ip = request.META.get('HTTP_X_FORWARDED_FOR')
            link_db.save()
            short_url = request.build_absolute_uri(link_db.hash)  # Build link using hash of original link

    return render(request, "index.html",
                  {"error": url_error, "shorturl": short_url})


def all(request):
    """All links page

    :param request: an HttpRequest object that contains metadata about the request
    :return: provides a template of all links with data
    """
    all_results = models.Link.objects.all().order_by('-redir_num')  # Get all links from database and order them by
    # num of redirects
    # 'all' is a variable to let the template understand which tab to show
    return render(request, "links.html",
                  {"all_results": all_results, "all": "active"})


def mine(request):
    """My links page

    :param request: an HttpRequest object that contains metadata about the request
    :return: provides a template of all links with data
    """
    # Get my links (created from my IP) from database and order them by num of redirects
    mine_results = models.Link.objects.all().filter(ip=request.META.get('REMOTE_ADDR')).order_by('-redir_num')
    # 'mine' is a variable to let the template understand which tab to show
    return render(request, "links.html",
                  {"mine_results": mine_results, "mine": "active"})


def delete(request, linkid):
    """Delete link method

    :param request: an HttpRequest object that contains metadata about the request
    :param linkid: an identifier of the link to delete
    :return: redirects to my links page
    """
    # Check if a link with such id exists
    try:
        # Check if this link created from my ip address
        if models.Link.objects.get(id=linkid).ip == request.META.get('REMOTE_ADDR'):
            link = models.Link.objects.get(id=linkid)
            link.delete()
    finally:
        return redirect("/mine/")


def redir(request, linkhash):
    """Redirection method (from short link to original)

    :param request: an HttpRequest object that contains metadata about the request
    :param linkhash: a hash of the original link (the 6 chars after the domain name)
    :return: redirects to original link or drops an error 404 (Not found)
    """
    # Check if a link with such hash exists
    try:
        link = models.Link.objects.get(hash=linkhash)
        models.Link.objects.filter(hash=linkhash).update(redir_num=F('redir_num') + 1)
        return redirect(link.original)
    except ObjectDoesNotExist:
        raise Http404()


def error_404(request, exception):
    return render(request, 'error_404.html')
