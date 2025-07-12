from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from . import util


def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })
    

def searchbar(request):
    search_word = request.GET.get("q") or ''
    entries = util.list_entries()
    if search_word == '':
        return HttpResponseRedirect(reverse('index'))
    else:
        partial_matches = []
        for entry in entries:
            if entry.lower() == search_word.lower():
                return HttpResponseRedirect(reverse('entry', kwargs={"entry": entry}))
            elif search_word.lower() in entry.lower():
                partial_matches.append(entry)
        print(partial_matches)
        return render(request, "encyclopedia/index.html", {
            "entries": partial_matches
            })


def entry(request, entry):
    if util.get_entry(entry) is None:
        return HttpResponseRedirect(reverse('not-found', kwargs={"entry": entry}))
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