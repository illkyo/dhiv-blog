from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from .models import User, Profile
from blog.models import Comment

class CustomUsernameField(UsernameField):

    def widget_attrs(self, widget):
        return {
            **super().widget_attrs(widget),
            "autocapitalize": "none",
            "autocomplete": "username",
            "dir": "auto"
        }
        
password1_help_text_html="""<ul style="color: #818182; padding-right: 25px; padding-top: 15px">
                                <li>ޕާސްވޯރޑް އިންގިރޭސި އަކުރުން ޖައްސަވާ</li>
                                <li>ޕާސްވޯރޑުގައި ތިޔަބޭފުޅާޔާ ބެހޭ އެއްވެސް މައުލޫމާތެއް ނުޖައްސަވާ</li>
                                <li>ޕާސްވޯރޑް 8 އަކުރަށް ވުރެއް ކުރުނުކުރައްވާ</li>
                                <li>ޕާސްވޯރޑާކީ މީހުން އާންމުކޮށް ޖައްސަވާ ޕާސްވޯރޑަކައް ނުހަދައްވާ</li>
                                <li>ޕާސްވޯރޑުގައި އަކުރާއި ނަންބަރު ހިމޭނޭހެން ޖައްސަވާ</li>
                            </ul>"""

class RegisterForm(UserCreationForm):

    password1 = forms.CharField(
      label=_("ޕާސްވޯރޑް"),
      strip=False,
      widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
      help_text=_(password1_help_text_html),
    #   help_text=password_validation.password_validators_help_text_html(),
  )
    password2 = forms.CharField(
      label=_("ޕާސްވޯރޑް ޔަގީން ކޮއްލެވުމަށް"),
      widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
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
    
	username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True}))
	password = forms.CharField(
        label=_("ޕާސްވޯރޑް"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
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
        
class CommentCreateForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content' : forms.Textarea(attrs={'placeholder': 'ކޮމެންޓެއް ލިޔުއްވުމަށް ...', 'class': 'comment-box'})
        }
        labels = {
            'content': ''
        }