from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from .models import User, Profile

class CustomUsernameField(UsernameField):

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
      field_classes = {"username": CustomUsernameField}
      
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
 
class UserUpdateForm(forms.ModelForm):
    
	class Meta:
		model = User
		fields = ['username']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].help_text = ('')
         
    
class ProfileUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        exclude = ['user']
        widgets = {
			'bio': forms.Textarea(),
		}