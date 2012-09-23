#coding:utf-8
from django import forms
from django.contrib.auth.models import User
from delivery.models import UserProfile
from addresses.models import Neighborhood
from django.contrib import messages
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
		first_name = forms.CharField()
		last_name = forms.CharField()
		email = forms.EmailField()
		password = forms.CharField( widget=forms.PasswordInput )
		password2 = forms.CharField( widget=forms.PasswordInput )
		birth_date = forms.DateField(  )
		cpf = forms.CharField(  )
		tel_number = forms.CharField(  )
		cep = forms.CharField(  )
		street = forms.CharField(  )
		number = forms.CharField(  )
		complement = forms.CharField( required=False )
		neighborhood = forms.CharField(  )
		observations = forms.CharField( required=False, widget=forms.Textarea )
		class Meta:
				model = UserProfile
		def clean(self):
				cleaned_data = super(UserProfileForm, self).clean()

				email = cleaned_data.get("email")
				user_email = User.objects.filter(email=email)

				user = cleaned_data.get("user")

				birth_date = cleaned_data.get("birth_date")

				password = cleaned_data.get("password")
				password2 = cleaned_data.get("password2")

				neighborhood = cleaned_data.get("neighborhood")
				registereds_neighborhoods = Neighborhood.objects.filter(des=neighborhood)

				msg = u"Error"

				if user_email:
						self._errors["email"] = self.error_class([msg])
						raise forms.ValidationError("Este e-mail encontra-se cadastrado em nosso sistema. Por favor, tente um diferente.")
				if password != password2:
						self._errors["password"] = self.error_class([msg])
						self._errors["password2"] = self.error_class([msg])
						raise forms.ValidationError("Por favor, confirme sua senha novamente.")
				if neighborhood and not registereds_neighborhoods:
						self._errors["neighborhood"] = self.error_class([msg])
						raise forms.ValidationError("Infelizmente não cobrimos o seu bairro.")
				
				return cleaned_data
