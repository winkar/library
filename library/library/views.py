from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import RequestContext
from django.contrib.auth.decorators import login_required


@login_required
def library(request):
    return render_to_response("index.html",context_instance=RequestContext(request))
