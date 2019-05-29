# stats/stats.py
import os
import base64


def tracking_id(request):
    """ retrieve or generate a unique tracking ID in each user session
        to determine what pages a customer has viewed 
    """
    try:
        return request.session['tracking_id']
    except KeyError:
        request.session['tracking_id'] = base64.b64encode(os.urandom(36))
        return request.session['tracking_id']