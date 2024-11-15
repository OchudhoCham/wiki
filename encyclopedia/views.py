from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import random
import markdown2
from django.urls import reverse
from . import util
from django import forms


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return HttpResponse("Entry Not Found.")
    html_content = markdown2.markdown(content)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })

def search(request):
    query = request.GET.get("q", "")
    if util.get_entry(query):
        return entry(request, query) #Redirect to entry page if found
    else:
        #Show search results if entry is not found
        matches = [entry for entry in util.list_entries() if query.lower() in entry.lower()]
        return render(request, "encyclopedia/search_results.html", {
            "matches": matches,
            "query": query
        })

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")

def new_page(request):
    if request.method =="POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title):
                return render(request, "encyclopedia/error.html", {
                    "message": "An entry with this title already exists."
                })
            util.save_entry(title, content)
            return redirect("entry", title=title)
        return redirect(request, "encyclopedia/new_page.html", {
            "form": NewPageForm()
        })

def edit_page(request, title):
    content = util.get_entry(title)
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            util.save_entry(title, form.cleaned_data["content"])
            return redirect("entry", title=title)
        return render(request, "encyclopedia/edit_page.html", {
            "form": NewPageForm(initial={'title': title, 'content': content}),
            "title": title
        })
    
def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect("entry", title=random_entry)