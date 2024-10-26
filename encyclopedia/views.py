from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import markdown2
from django.urls import reverse 
from . import util

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
        entries = [entry for entry in util.list_entries() if query.lower() in entry.lower()]
        return render(request, "encyclopedia/search_results.html", {
            "entries": entries,
            "query": query
        })
