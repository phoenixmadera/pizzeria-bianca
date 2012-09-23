#coding:utf-8
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import AuthenticationForm
from addresses.models import Neighborhood, NeighborhoodRate, Address
from delivery.models import UserProfile, DeliveryTime
from products.models import Product
from django.template import RequestContext
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from delivery.forms import UserProfileForm
import random, string 
from datetime import date, datetime
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseRedirect, QueryDict
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_safe
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.utils.http import base36_to_int
from django.conf import settings
# Create your views here.
@csrf_protect
def index(request):
		r = NeighborhoodRate.objects.all()
		n = Neighborhood.objects.all()
		if request.user.is_authenticated():
			return redirect('/passo1/')
		return render_to_response('index.html', RequestContext(request, {'neighborhoods': n,
																																		 'rates': r,}))

@csrf_protect
def user_login(request):
		r = NeighborhoodRate.objects.all()
		n = Neighborhood.objects.all()
		username = password = ''
		if request.user.is_authenticated():
			return redirect('/passo1/')
		if request.POST:
				username = request.POST.get('username')
				password = request.POST.get('password')
				keep_connected = request.POST.get('keep_connected')
				user = authenticate(username=username, password=password)
				if user is not None:
				    if user.is_active:
								login(request, user)
								if keep_connected:
										request.session.set_expiry(1296000)
								else:
										request.session.set_expiry(900)
								return redirect('/passo1/')
				    else:
				        messages.error(request, 'Sua conta ainda não está ativada.')
				else:
				    messages.error(request, 'Seu email e/ou senha estão incorretos.')
		return render_to_response('index.html', RequestContext(request, {'username': username,
																																		 'neighborhoods': n,
																																		 'rates': r,}))
def user_register(request):
	r = NeighborhoodRate.objects.all()
	n = Neighborhood.objects.all()
	if request.user.is_authenticated():
			return redirect('/passo1/')
	if request.POST:
			form = UserProfileForm(request.POST)
			password = request.POST.get('password')
			email = request.POST.get('email')
			first_name = request.POST.get('first_name')
			last_name = request.POST.get('last_name')
			birth_date = request.POST.get('birth_date')
			cpf = request.POST.get('cpf')
			tel_number = request.POST.get('tel_number')
			cep = request.POST.get('cep')
			street = request.POST.get('street')
			number = request.POST.get('number')
			complement = request.POST.get('complement')
			neighborhood = request.POST.get('neighborhood')
			observations = request.POST.get('observations')
			username = last_name+""+str(random.randint(0, 9999))

			if form.is_valid():
					birth_date = datetime.strptime(birth_date, '%d/%m/%Y')

					user = User.objects.create_user(username, email, password)
					user.first_name = first_name
					user.last_name = last_name
					user.is_active = False

					neighborhood_aux = Neighborhood.objects.get(des=neighborhood)

					user_profile = UserProfile.objects.create(user=user,
																										birth_date=birth_date,
																										cpf=cpf,
																										tel_number=tel_number,
																										activation_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for n in range(20)))

					address = Address.objects.create(cep=cep,
																					street=street,
																					number=number,
																					complement=complement,
																					neighborhood=neighborhood_aux,
																					observations=observations,
																					user=user_profile)

					send_mail(
										 'Bianca Pizzaria - Ative sua conta!',
										 'Por favor visite http://localhost:800/nova_conta/%s/ para ativar a sua conta.' % (user_profile.activation_key),
										 'contato420wear@gmail.com',
										 [email,])

					user.save()
					address.save()
					user_profile.save()
					
					messages.success(request, 'Você receberá em breve um e-mail com as instruções para confirmar sua conta.')
					return redirect('/')
	else:
			form = UserProfileForm()

	return render_to_response('index.html',  RequestContext(request, {'form': form, 
																																		'neighborhoods': n,
																																		'rates': r,}))

@login_required(login_url='/')
def passo1(request):
		d = DeliveryTime.objects.filter(pk=1)
		p = Product.objects.all()
		return render_to_response('steps/one.html', RequestContext(request, {'delivery_time': d,
																																				 'products': p}))

def logout_view(request):
		logout(request)
		return redirect('/')

def user_activation(request, activation_key):
		 try:
				 #First, the code tries to look up the user based on the activation key
				 user_profile = UserProfile.objects.get(activation_key=activation_key)
				 user = user_profile.user
				 #If found, and the user is not active, the user's account is activated.
				 if user.is_active == False:
						 user.is_active = True
						 user.save()
						 messages.success(request, 'A sua conta foi ativada corretamente! Faça seu login abaixo.')
						 return redirect('/')
						 #Else, if the user is already active, an error page is passed
				 else:
				 		messages.error(request, 'A sua conta já está ativada.')
				 		return redirect('/')
		 #If no user is found with the activation key, an error page is passed
		 except UserProfile.DoesNotExist:
		 		messages.error(request, 'Esta chave de ativação é inválida.')
		 		return redirect('/')
		 return render_to_response('index.html', RequestContext(request))


@csrf_protect
def password_reset(request, is_admin_site=False,
                   template_name='registration/password_reset_form.html',
                   email_template_name='registration/password_reset_email.html',
                   subject_template_name='registration/password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   current_app=None,
                   extra_context=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('delivery.views.password_reset_done')
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
            }
            if is_admin_site:
                opts = dict(opts, domain_override=request.META['HTTP_HOST'])
            form.save(**opts)
            request.session['reset_success'] = 'True'
            return HttpResponseRedirect(reverse('delivery.views.password_reset_done'))
    else:
        form = password_reset_form()
    context = {
        'form': form,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)

def password_reset_done(request,
                        template_name='registration/password_reset_done.html',
                        current_app=None, extra_context=None):
		context = {}
		if 'reset_success' in request.session and request.session['reset_success'] == 'True':
				request.session['reset_success'] = 'False'
		else:
				return redirect('/')
		if extra_context is not None:
				context.update(extra_context)
		return TemplateResponse(request, template_name, context,
                            current_app=current_app)

@sensitive_post_parameters()
@never_cache
def password_reset_confirm(request, uidb36=None, token=None,
                           template_name='registration/password_reset_confirm.html',
                           token_generator=default_token_generator,
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None,
                           current_app=None, extra_context=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    assert uidb36 is not None and token is not None # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('delivery.views.password_reset_complete')
    try:
        uid_int = base36_to_int(uidb36)
        user = User.objects.get(id=uid_int)
    except (ValueError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                request.session['change_success'] = 'True'
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(None)
    else:
        validlink = False
        form = None
    context = {
        'form': form,
        'validlink': validlink,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)

def password_reset_complete(request,
                            template_name='registration/password_reset_complete.html',
                            current_app=None, extra_context=None):
		context = {
		    'login_url': settings.LOGIN_URL
		}
		if 'change_success' in request.session and request.session['change_success'] == 'True':
				request.session['change_success'] = 'False'
		else:
				return redirect('/')
		if extra_context is not None:
				context.update(extra_context)
		return TemplateResponse(request, template_name, context,
                            current_app=current_app)