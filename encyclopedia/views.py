from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    
    return render(request, "encyclopedia/entry.html", {
        "entry": util.markdown_to_html(entry) 
    })
