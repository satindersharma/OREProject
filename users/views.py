from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission
from django.views.generic.edit import CreateView, View, FormView
from django.views.generic import DetailView, TemplateView, UpdateView, ListView
# from django.views.generic import DetailView
from django.contrib.auth import get_user_model
from django.contrib import messages
from .mixins import NextUrlMixin
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomPasswordResetForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse_lazy, reverse
from django.contrib import messages
# from profiles.models import Setting
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from users.models import UserProfile
from users.forms import UserProfileForm, OREUserCreateForm, OREPasswordlessLoginForm, OREPasswordlessLoginVerifyCodeForm
from django.contrib.contenttypes.models import ContentType
import requests
import json
from django.conf import settings
from algosdk import algod
from users.ore import OREMixin
from urllib.parse import urlencode


REDIRECT_HTML = '<!DOCTYPE html><html lang="en"><head><meta charSet="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=0"/><meta name="theme-color" content="#000000"/><meta name="msapplication-TileColor" content="#222222"/><meta name="theme-color" content="#ffffff"/><meta name="msapplication-TileImage" content="/favicons/mstile-150x150.png"/><meta name="description" content="ORE ID is the universal authentication and authorization platform for blockchain."/><meta name="author" content="AIKON"/><link rel="shortcut icon" href="/favicons/favicon.ico"/><link rel="apple-touch-icon" sizes="120x120" href="/favicons/apple-touch-icon.png"/><link rel="icon" type="image/png" sizes="32x32" href="/favicons/favicon-32x32.png"/><link rel="icon" type="image/png" sizes="16x16" href="/favicons/favicon-16x16.png"/><link rel="mask-icon" href="/favicons/safari-pinned-tab.svg" color="#222222"/><meta name="viewport" content="width=device-width"/><meta charSet="utf-8"/><title>ORE ID</title><link rel="preload" href="/_next/static/css/3c21af68510cfeb2f217ce14117b43cb32f452ea_CSS.9ccfe52f.chunk.css" as="style"/><link rel="stylesheet" href="/_next/static/css/3c21af68510cfeb2f217ce14117b43cb32f452ea_CSS.9ccfe52f.chunk.css" data-n-p=""/><noscript data-n-css="true"></noscript><link rel="preload" href="/_next/static/chunks/main-0a5ee3545751b4c2f453.js" as="script"/><link rel="preload" href="/_next/static/chunks/webpack-d7b2fb72fb7257504a38.js" as="script"/><link rel="preload" href="/_next/static/chunks/framework.c7b20b4e446c7cca89e7.js" as="script"/><link rel="preload" href="/_next/static/chunks/commons.d03bab4c355412d29eff.js" as="script"/><link rel="preload" href="/_next/static/chunks/36be787778a34a78272c31d122a8d4caac64ee8d.c88f3d3b5c3a9767a9bb.js" as="script"/><link rel="preload" href="/_next/static/chunks/pages/_app-382f5080ecc13427e082.js" as="script"/><link rel="preload" href="/_next/static/chunks/c727088c.21cb767f773baa92a0be.js" as="script"/><link rel="preload" href="/_next/static/chunks/c78d26b1.a584650294ca5e8e6fae.js" as="script"/><link rel="preload" href="/_next/static/chunks/eb0defb7.ecaf484481f05a4fbaa3.js" as="script"/><link rel="preload" href="/_next/static/chunks/8050e1a2.798ed5305ec1425c1975.js" as="script"/><link rel="preload" href="/_next/static/chunks/e971612a.df88ce9a4c17e0489424.js" as="script"/><link rel="preload" href="/_next/static/chunks/041beda9.11a13abb398d2fe1066e.js" as="script"/><link rel="preload" href="/_next/static/chunks/54bd6e75932f69cea63a890638a6a70120694729.45ec01dd33b998ccf3ed.js" as="script"/><link rel="preload" href="/_next/static/chunks/444360df9fffb9a2710034b801c9f0d6c8ee61dd.870ed0cab806564f7e26.js" as="script"/><link rel="preload" href="/_next/static/chunks/3c21af68510cfeb2f217ce14117b43cb32f452ea.7fe1e4796e31db8b2544.js" as="script"/><link rel="preload" href="/_next/static/chunks/3c21af68510cfeb2f217ce14117b43cb32f452ea_CSS.748f7f460fe4ac62566f.js" as="script"/><link rel="preload" href="/_next/static/chunks/pages/index-94d81457168927febc17.js" as="script"/></head><body><div id="__next"><div class="redirect-https"><div></div></div></div><script id="__NEXT_DATA__" type="application/json">{"props":{"pageProps":{}},"page":"/","query":{},"buildId":"CDS0XUKkaLQQZEasJypEP","runtimeConfig":{"REACT_APP_PORT":"8080","REACT_APP_ENVIRONMENT":"production","REACT_APP_AUTH0_AUDIENCE":"https://oreid.aikon.com","REACT_APP_AUTH0_DOMAIN":"auth.oreid.io","REACT_APP_AUTH0_AUTH_URI":"https://auth.oreid.io/oauth/token","REACT_APP_AUTH0_CLIENT_ID":"wm19msdFxZUe4P9oVcGoZJgWjQpgCfhI","REACT_APP_AUTHO_BASE_CLAIM_URL":"https://oreid.aikon.com","REACT_APP_AUTH0_CLIENT_PUBLIC_SIGNING_CERT":"LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tDQpNSUlDK1RDQ0FlR2dBd0lCQWdJSlk0QWYwaVVyM05iS01BMEdDU3FHU0liM0RRRUJDd1VBTUJveEdEQVdCZ05WDQpCQU1URDJGcGEyOXVMbUYxZEdnd0xtTnZiVEFlRncweE9EQTBNREV4TlRNeU5UWmFGdzB6TVRFeU1Ea3hOVE15DQpOVFphTUJveEdEQVdCZ05WQkFNVEQyRnBhMjl1TG1GMWRHZ3dMbU52YlRDQ0FTSXdEUVlKS29aSWh2Y05BUUVCDQpCUUFEZ2dFUEFEQ0NBUW9DZ2dFQkFPWEFkczB1SmdsVEU4QnBHQ0l2YmJoalIvSHA0c3lIRTkxNHZjcWc4anRxDQorV2R5OVgzbjlOSDlJMFlDZ3JwRncxMlFiVlBmSkI5STdGMUVsTkFoVmxkZ3ZIZnh4SjhJSVJrc1BsdG5CWTlhDQpYUy93ZnpvSGdMSjdxc2tSRk55bHJSVWNjMzlUc0RmUUpnYjlia05nN2hOaEZPOGJoUUg4R2kwbTJCY0VWcEw1DQpOYy9OQUJ1cjZGM1J1SEt3WWg5SFQ4cTl5MUhwU1ZVemUxNTZQMGFEMGZ5djI0d0p1d3pJN3Q0emhUelVETXhKDQpiVHRoMnlEOEQyZkNJcUphNzNWcnRmRTErbjhLZGFTR1FaSjRTbWJmUlhNWmhIVmkzeWVzc05rRXNwTXNuZ0kzDQp0S1h2OXI4Ym91U0I2WjFHVFphYUhSeURRdklUWlFvbDdrQ1pOSkxsWTlNQ0F3RUFBYU5DTUVBd0R3WURWUjBUDQpBUUgvQkFVd0F3RUIvekFkQmdOVkhRNEVGZ1FVelZZR2JkZDRRRVJxZ2xTdElGZWcvV2hTb0FZd0RnWURWUjBQDQpBUUgvQkFRREFnS0VNQTBHQ1NxR1NJYjNEUUVCQ3dVQUE0SUJBUURMdnNYdm1PTkZoVGs1WmhWVTM1VnNIT2N2DQpheTRJSE5nbEFGYi9rWnNkbjRSbEhzN1NOdHVQbGZ2TUtGUnR5SEtsdWd1VmNoY01qWlkxSStkYU1vZEpRWjhKDQpYQ2ZnN3pOQ2dCVDBzTkRlOTU3MWhDVHU4QWNCZXRXNXloZnI0VkQ2SE1TcGhOaGZtcGkwR2pISmlPbXgraXhWDQprbmJVQUVlelJHUkhVd2hFc3pXU3BkQWQ5UGZobUFZa2FzNlZaY1J6TDRWbmZRYkJuMkovWTI2bXVuYm5pbUVKDQpTZmdSaWcrZ0kydEVFZ3dKMW5GRjQ4QWNCeUtLN3pRSnR2ek0yZFQxQk9vb0JBY2xKeWwvNFgvSFdudjN0aW9pDQpIdFZuRXBDTE5weXhReGo4VktqY1NZSTVaSjYzdVRGcGwxWTlFWExUOUNSakdyL3JNcXhXZCtrVFJRbU4NCi0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0NCg==","REACT_APP_GRAPHQL_ENDPOINT":"/frontend/graphql","REACT_APP_GRAPHQL_ENDPOINT_UNSECURED":"/frontend/graphql-unsecured","REACT_APP_SEGMENT_WRITE_KEY":"lHycUviPVE2YHnvKCJzxnHtZXrMGQmQa","REACT_APP_ROLLBAR_POST_WRITE_CLIENT_KEY":"aa26c966c8f34f63b94cc433f938db2c","REACT_APP_HELPSCOUT_FORM_ID":"3c59ef1c-9b55-11e8-a978-0a23a233d4be","REACT_APP_HELPSCOUT_BASE_URL":"https://aikon.helpscoutdocs.com/","REACT_APP_DEFAULT_APP_ID":"aaaaaaa-501c-4eeb-a355-bbaa8cfa2597","REACT_APP_STRIPE_PUBLISHABLE_KEY":"pk_live_TteT4P4PKOB5Zw1Cb9m0vteC","REACT_APP_RECAPTCHA_CLIENT_KEY":"6LdJl54UAAAAAFYXRGqDjfNX9NWPzrXUmpoDU9aI","REACT_APP_OREID_APP_ID":"aaaaaaa-501c-4eeb-a355-bbaa8cfa2597","REACT_APP_OREID_URL":"https://service.oreid.io","REACT_APP_ORE_EXPLORER_URL":"https://ore.eosq.app"},"isFallback":false,"customServer":true,"gip":true,"head":[["meta",{"name":"viewport","content":"width=device-width"}],["meta",{"charSet":"utf-8"}],["title",{"children":"ORE ID"}]]}</script><script nomodule="" src="/_next/static/chunks/polyfills-635044afa53fba94a6fd.js"></script><script src="/_next/static/chunks/main-0a5ee3545751b4c2f453.js" async=""></script><script src="/_next/static/chunks/webpack-d7b2fb72fb7257504a38.js" async=""></script><script src="/_next/static/chunks/framework.c7b20b4e446c7cca89e7.js" async=""></script><script src="/_next/static/chunks/commons.d03bab4c355412d29eff.js" async=""></script><script src="/_next/static/chunks/36be787778a34a78272c31d122a8d4caac64ee8d.c88f3d3b5c3a9767a9bb.js" async=""></script><script src="/_next/static/chunks/pages/_app-382f5080ecc13427e082.js" async=""></script><script src="/_next/static/chunks/c727088c.21cb767f773baa92a0be.js" async=""></script><script src="/_next/static/chunks/c78d26b1.a584650294ca5e8e6fae.js" async=""></script><script src="/_next/static/chunks/eb0defb7.ecaf484481f05a4fbaa3.js" async=""></script><script src="/_next/static/chunks/8050e1a2.798ed5305ec1425c1975.js" async=""></script><script src="/_next/static/chunks/e971612a.df88ce9a4c17e0489424.js" async=""></script><script src="/_next/static/chunks/041beda9.11a13abb398d2fe1066e.js" async=""></script><script src="/_next/static/chunks/54bd6e75932f69cea63a890638a6a70120694729.45ec01dd33b998ccf3ed.js" async=""></script><script src="/_next/static/chunks/444360df9fffb9a2710034b801c9f0d6c8ee61dd.870ed0cab806564f7e26.js" async=""></script><script src="/_next/static/chunks/3c21af68510cfeb2f217ce14117b43cb32f452ea.7fe1e4796e31db8b2544.js" async=""></script><script src="/_next/static/chunks/3c21af68510cfeb2f217ce14117b43cb32f452ea_CSS.748f7f460fe4ac62566f.js" async=""></script><script src="/_next/static/chunks/pages/index-94d81457168927febc17.js" async=""></script><script src="/_next/static/CDS0XUKkaLQQZEasJypEP/_buildManifest.js" async=""></script><script src="/_next/static/CDS0XUKkaLQQZEasJypEP/_ssgManifest.js" async=""></script></body></html>'
class Home(LoginRequiredMixin, TemplateView):
    '''
    default home view
    '''
    template_name = 'home.html'


class SignUpView(NextUrlMixin, CreateView):
    form_class = CustomUserCreationForm
    success_url = '/'
    template_name = 'registration/signup.html'
    success_message = 'You have signed up successfully'
    default_next = '/'

    def form_valid(self, form):
        # save the new user first
        form.save()
        # get the username and password
        # authenticate user then login
        user = authenticate(
            username=form.cleaned_data['username'], password=form.cleaned_data['password1'], )
        login(self.request, user)
        messages.success(self.request, 'You have signed up successfully')
        next_path = self.get_next_url()
        return HttpResponseRedirect(next_path)


class UserLoginView(NextUrlMixin, SuccessMessageMixin, LoginView):
    form_class = CustomAuthenticationForm
    redirect_authenticated_user = True
    # template_name = 'registration/login3.html'


class UserLogoutView(NextUrlMixin, SuccessMessageMixin, LogoutView):
    pass


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm


class UserProfileView(LoginRequiredMixin, UpdateView):
    '''
    user profile view

    '''
    template_name = 'registration/profile_page.html'
    model = UserProfile
    form_class = UserProfileForm
    success_url = reverse_lazy('users:user-profile')

    def get_object(self, queryset=None):
        ''' overwrite the method so we not need to config url '''
        try:
            obj = self.model.objects.get(user=self.request.user)
            return obj
        except Exception as ex:
            print('class UserProfileView def get_object', ex)
            return

    def get_initial(self, *args, **kwargs):
        ''' initialize your's form values here '''
        base_initial = self.initial.copy()
        base_initial.update({'user': self.request.user})
        return base_initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['user_profile_form'] = context.pop('form')
        except KeyError:
            context['user_profile_form'] = self.get_form()

        try:
            context['user_profile_object'] = context.pop('object')
        except KeyError:
            context['user_profile_object'] = self.get_object()

        return context

    def form_valid(self, form, *args, **kwargs):
        if not form.instance.user:
            form.instance.user = self.request.user
        form.save()
        if self.request.is_ajax():
            return JsonResponse({'result': 'Success', 'content': 'Profile Updated'})
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax() and form.errors:
            errors = form.errors.as_json()
            return HttpResponse(errors, status=400, content_type='application/json')
        return super().form_invalid(form)


class DeleteProfileImage(LoginRequiredMixin, View):
    '''
    delete profile image
    '''

    def post(self, request, *args, **kwargs):
        try:
            # db = request.POST.get('disabled')
            # print('---- is Disabled ----', db)
            p = UserProfile.objects.get(user=request.user)
            p.image = ''
            p.save()
            return JsonResponse({'result': 'Success', 'content': 'Image Deleted'})
        except Exception as ep:
            print('class DeleteProfileImage def post', ep)
        return HttpResponse({'result': 'error', 'content': 'Unable to Delete'}, status=400, content_type='application/json')


class GetOREUserView(View):
    def get(self, request, *args, **kwargs):
        url = settings.OREID_APP_URL + "account/user?account=" + \
            settings.OREID_APP_ACCOUNT_NAME
        payload = {}
        headers = {
            'api-key': settings.OREID_API_KEY,
        }

        {'processId': '44d5bf9852ca',
         'accountName': 'ore1ro1owtgb',
         'email': 'satinder@gmail.com',
         'picture': 'https://storage.googleapis.com/oreid-files/images/user-custodial|8bef34117d9e5ff037d8ea6817b661b4-profile.jpg',
         'name': 'John Q Smith',
         'username': 'satinder12345',
         'permissions': [
             {'chainNetwork': 'algo_test',
              'chainAccount': 'E46ZM4BTC3MPVF3WH2T4GRIHI4N2NT7ZXGDFUSMT76FK634TXFB7GOC5HQ',
              'permissionName': 'active',
              'publicKey': '273d96703316d8fa97763ea7c34507471ba6cff9b9865a4993ff8aaf6f93b943',
              'privateKeyStoredExterally': False,
              'externalWalletType': None,
              'accountType': 'native',
              'permission': 'active'}
         ]}
        
        response = requests.request("GET", url, headers=headers, data=payload)
        context = {'ore_data': response.json()}
        return render(request, 'home.html', context=context)


class GetOREAppTokenView(View):
    def get(self, request, *args, **kwargs):
        url = settings.OREID_APP_URL + "app-token"
        # payload = json.dumps({
        #                     "newAccountPassword": "SomeNewPassword",
        #                     "currentAccountPassword": "CurrentUserPassword",
        #                     "secrets": [
        #                         {
        #                         "RepublicAccountRecoveryToken": "Some Secret Value"
        #                         }
        #                     ]
        #                     })
        payload = {}
        headers = {
            'api-key': settings.OREID_API_KEY,
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        context = {'ore_data': response.json()}
        return render(request, 'home.html', context=context)


class CreateOREUserView(OREMixin, FormView):
    '''
    Create ORE User
    '''

    form_class = OREUserCreateForm
    template_name = 'ore_form.html'
    success_url = reverse_lazy('users:home')

    # def get_success_url(self):

    #     return super().get_success_url()

    def form_valid(self, form, *args, **kwargs):
        # print(form.cleaned_data)
        data = form.cleaned_data
        res = self.create_ore_user(data=data)
        print("====================")
        print(res)
        print("====================")
        context = super().get_context_data(**kwargs)
        context['ore_data'] = res
        return super().form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        print(form.errors)
        return super().form_valid(form)

    # def get_context_data(self,*args,**kwargs):
    #     context  = super().get_context_data(**kwargs)
    #     return context


class OREPasswordlessLoginView(OREMixin, FormView):
    form_class = OREPasswordlessLoginForm
    template_name = 'email_send_code_form.html'
    success_url = reverse_lazy('users:ore-verify-code')
    
    def form_valid(self, form, *args, **kwargs):
        # print(form.cleaned_data)
        email = form.cleaned_data.get('email')
        res = self.send_login_code(email=email)
        # res = {}
        print("====================")
        print(res)
        print("====================")
        context = super().get_context_data(**kwargs)
        context['code_response'] = res
        if res.get('success',True):
            # base_url = reverse_lazy('users:ore-verify-code')  # 1 /ore-verify-code/
            # query_string =  urlencode({'email': email})  # 2 email=email@gmail.com
            # url = '{}?{}'.format(base_url, query_string)  # 3 /ore-verify-code/?email=email@gmail.com
            # return HttpResponseRedirect(url)
            c_form = OREPasswordlessLoginVerifyCodeForm(initial={'email':email})
            return render(self.request,'email_verify_code_form.html',{'form':c_form})
        return super().form_valid(form)


class OREPasswordlessLoginVerifyCodeView(OREMixin, FormView):
    form_class = OREPasswordlessLoginVerifyCodeForm
    template_name = 'email_verify_code_form.html'
    # success_url = reverse_lazy('users:ore-verify-code')
    
    def form_valid(self, form, *args, **kwargs):
        # print(form.cleaned_data)
        code = form.cleaned_data.get('code')
        email = form.cleaned_data.get('email')
        print(email)
        # res = self.verify_login_code(email=email,code=code)
        res = self.authenticate_ore_user(email=email,code=code)
        # res = {}
        print("====================")
        print(res)
        print("====================")
        context = super().get_context_data(**kwargs)
        context['code_response'] = res
        return HttpResponse(res)
        # return HttpResponse(REDIRECT_HTML)
        # return super().form_valid(form)