from django.shortcuts import redirect

def character_selected(f): # who knows if this will work at all LOL
    def wrap(request, *args, **kwargs):
        if "character" in request.session:
            return f(request,*args, **kwargs)
        else:
            return redirect("/char")
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap  # will this work ?
