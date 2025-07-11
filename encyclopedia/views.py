from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    if util.get_entry(entry) is None:
        return HttpResponseRedirect(reverse('not-found',kwargs={"entry": entry}))
    else:
        entry_body = util.markdown_to_html(util.get_entry(entry))
        return render(request, "encyclopedia/entry.html", {
            "entry_title": entry,
            "entry_body": entry_body,
        })

def entry_not_found(request, entry):
    return render(request, "encyclopedia/entry_not_found.html", {
        "entry_name": entry
    })