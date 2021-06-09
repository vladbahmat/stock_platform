from django.core.mail import send_mail
from django.utils import translation

from django.utils.translation import ugettext_lazy as _

def send_email_language_notification(email, code):
    some_text = _('Hello')
    with translation.override(code):
        print(translation.gettext(some_text))
        send_mail('shrek', translation.gettext(some_text) , 'uservice589@gmail.com', email)