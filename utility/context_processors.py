def privacy(request):
    do_not_track = request.session.get('DNT', None)
    if do_not_track is None:
        do_not_track = request.headers.get('DNT', 0)
        request.session['DNT'] = do_not_track
    return dict(DNT=do_not_track)
