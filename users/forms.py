import unicodedata

from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class UsernameField(forms.CharField):
    def to_python(self, value):
        value = super().to_python(value)
        if self.max_length is not None and len(value) > self.max_length:
            # Normalization can increase the string length (e.g.
            # "ﬀ" -> "ff", "½" -> "1⁄2") but cannot reduce it, so there is no
            # point in normalizing invalid data. Moreover, Unicode
            # normalization is very slow on Windows and can be a DoS attack
            # vector.
            return value
        return unicodedata.normalize("NFKC", value)

    def widget_attrs(self, widget):
        return {
            **super().widget_attrs(widget),
            "autocapitalize": "none",
            "autocomplete": "username",
            "dir": "auto"
        }

class RegisterForm(UserCreationForm):

    password1 = forms.CharField(
      label=_("ޕާސްވޯރޑް"),
      strip=False,
      widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "dir": "auto"}),
      help_text=password_validation.password_validators_help_text_html(),
  )
    password2 = forms.CharField(
      label=_("ޕާސްވޯރޑް ޔަގީން ކޮއްލެވުމަށް"),
      widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "dir": "auto"}),
      strip=False,
      help_text=_("ކުރިން ޖެއްސެވި ޕާސްވޯރޑް ޖައްސަވާލައްވާ"),
  )
    
    error_messages = {
      "password_mismatch": _("ޖެއްސެވި ދެ ޕާސްވޯރޑް ދިމައެއް ނޫން"),
  }

    class Meta:
      model = User
      fields = ("username",)
      field_classes = {"username": UsernameField}
      
class LoginForm(AuthenticationForm):
    
	username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True, "dir": "auto"}))
	password = forms.CharField(
        label=_("ޕާސްވޯރޑް"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "dir": "auto"}),
    )

	error_messages = {
        "invalid_login": _(
            "ރަނގަޅު ޔޫސަރނަމަކާ ޕާސްވޯރޑެއް ޖައްސަވާ"
        ),
        "inactive": _("This account is inactive."),
    }