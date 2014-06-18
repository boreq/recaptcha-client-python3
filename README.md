# recaptcha-client-python3
Client script for reCaptcha compatibile with Python 3.

## Why?
The [original code](https://code.google.com/p/recaptcha/) does not support Python 3. In fact it does not support Python 2 either since it contains semicolons and does not follow [PEP-8](http://legacy.python.org/dev/peps/pep-0008/) in any way.

## How?
### Check

    import captcha

    response = captcha.submit(
        recaptcha_challenge_field,
        recaptcha_response_field,
        your_private_key,
        remote_ip
    )

    if response.is_valid:
        do_something()
    else:
        display_error_message()

### Display
Use the following to get the HTML:

    captcha.display_html(your_public_key)
