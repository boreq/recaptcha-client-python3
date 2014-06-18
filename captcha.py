import urllib

API_SSL_SERVER="https://www.google.com/recaptcha/api"
API_SERVER="http://www.google.com/recaptcha/api"
VERIFY_SERVER="www.google.com"

class RecaptchaResponse(object):
    def __init__(self, is_valid, error_code=None):
        self.is_valid = is_valid
        self.error_code = error_code

def display_html(public_key, use_ssl=False, error=None):
    """Gets the HTML to display for reCAPTCHA

    public_key -- The public api key
    use_ssl -- Should the request be sent over ssl?
    error -- An error message to display (from RecaptchaResponse.error_code)"""

    error_param = '&error=%s' % error if error else ''

    if use_ssl:
        server = API_SSL_SERVER
    else:
        server = API_SERVER

    return """<script type="text/javascript" src="%(ApiServer)s/challenge?k=%(PublicKey)s%(ErrorParam)s"></script>

<noscript>
  <iframe src="%(ApiServer)s/noscript?k=%(PublicKey)s%(ErrorParam)s" height="300" width="500" frameborder="0"></iframe><br />
  <textarea name="recaptcha_challenge_field" rows="3" cols="40"></textarea>
  <input type='hidden' name='recaptcha_response_field' value='manual_challenge' />
</noscript>
""" % {
        'ApiServer': server,
        'PublicKey': public_key,
        'ErrorParam': error_param,
    }


def submit(recaptcha_challenge_field, recaptcha_response_field, private_key, remote_ip):
    """Submits a reCAPTCHA request for verification. Returns RecaptchaResponsek
    for the request

    recaptcha_challenge_field -- The value of recaptcha_challenge_field from the form
    recaptcha_response_field -- The value of recaptcha_response_field from the form
    private_key -- your reCAPTCHA private key
    remote_ip -- the user's ip address
    """

    # There is no point in checking if the captcha is valid if one of the fields is empty.
    if not (recaptcha_response_field and recaptcha_challenge_field):
        return RecaptchaResponse(is_valid=False, error_code='incorrect-captcha-sol')

    params = {
        'privatekey': private_key,
        'remoteip': remote_ip,
        'challenge': recaptcha_challenge_field,
        'response': recaptcha_response_field,
    }

    # Data must be encoded to 'percent-encoded' string first and to bytes later.
    params = urllib.parse.urlencode(params).encode('utf-8')

    request = urllib.request.Request(
        url = "http://%s/recaptcha/api/verify" % VERIFY_SERVER,
        data = params,
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "User-agent": "reCAPTCHA Python",
        }
    )
    
    # Get the server's response.
    httpresp = urllib.request.urlopen(request)
    return_values = httpresp.read()
    httpresp.close()

    # Returned values are in form of bytes, split them to lines and decode to text.
    return_values = [value.decode('utf-8') for value in return_values.splitlines()]

    # Line 0 contains true if the solution was valid or false otherwise.
    # Line 1 contains an optional error code.
    captcha_valid = (return_values[0] == 'true')
    error_code = return_values[1] if len(return_values) > 1 else None

    return RecaptchaResponse(is_valid=captcha_valid, error_code=error_code)
