def dnt(request):
    do_not_track = request.session.get('DNT', None)
    Tk = request.headers.get('Tk')
    if do_not_track is None:
        do_not_track = request.headers.get('DNT', 0)
        request.session['DNT'] = do_not_track
    return dict(DNT=do_not_track, Tk=Tk)
