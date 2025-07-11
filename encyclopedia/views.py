from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    entry_body = util.markdown_to_html(entry)
    return render(request, "encyclopedia/entry.html", {
        "entry_title": entry,
        "entry_body": entry_body,
    })
