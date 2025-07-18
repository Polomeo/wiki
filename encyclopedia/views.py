import markdown2
import random

from django import forms
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse


from . import util

def validate_entry_title(title):
    all_entries = [e.lower() for e in util.list_entries()]
    if title.lower() in all_entries:
        raise ValidationError('Already exists an entry with this title. Please choose a diferent one.')

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title",
                            required = True,
                            max_length = 50,
                            validators=[validate_entry_title]
                            )
    content = forms.CharField(widget=forms.Textarea())

class EditEntryForm(forms.Form):
    content = forms.CharField(label="Content",
                            widget=forms.Textarea(),
                            )

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
        return render(request, "encyclopedia/search_results.html", {
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


def new_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('entry', kwargs={"entry": title}))
        else:
            return render(request, "encyclopedia/new_entry.html", {
                    "form": form
                })

    return render(request, "encyclopedia/new_entry.html", {
        "form": NewEntryForm()
    })


def edit_entry(request, title):
    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            content_clean = form.cleaned_data['content']
            util.save_entry(title, content_clean)
            return HttpResponseRedirect(reverse('entry', kwargs={"entry": title}))
        else:
            data = {"title": form.cleaned_data['title'], 
                    "content": form.cleaned_data['content'],
                    }
            return render(request, "encyclopedia/edit_entry.html", {
                    "form": EditEntryForm(initial=data),
                    "title": title,
                })
    # GET Method
    content = util.get_entry(title)
    return render(request, "encyclopedia/edit_entry.html", {
        "form": EditEntryForm(initial={"content": content}),
        "title": title,
    })


def random_entry(request):
    random_pick = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse('entry', kwargs={"entry": random_pick}))
