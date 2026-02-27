from django.urls import path,include
from ecommerce import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from .forms import LoginForm,MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm

urlpatterns = [
    path('',views.Productview.as_view(),name='home'),
    path('product-details/<int:pk>',views.ProductDetailView.as_view(),name='productdetail'),
    path('add-to-cart/',views.add_to_cart,name='add-to-cart'),
    path('showcart/',views.show_cart,name='showcart'),
    path('plus-quantity/', views.plus_quantity, name='plus_quantity'),
    path('minus-quantity/', views.minus_quantity, name='minus_quantity'),
    path('remove-cart/', views.remove_cart, name='remove_cart'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('orders/', views.orders, name='orders'),
    path('checkout/', views.checkout, name='checkout'),
    path('electronic/',views.electronics,name='electronic'),
    path('electronic/<slug:data>',views.electronics,name='electronicdata'),
    path('fashion/',views.Fashion,name='fashion'),
    path('fashion/<slug:data>',views.Fashion,name='fashiondata'),
    path('grocery/',views.Grocery,name='grocery'),
    path('grocery/<slug:data>',views.Grocery,name='grocerydata'),
    path('vegetables/',views.Vegetables,name='vegetables'),
    path('vegetables/<slug:data>',views.Vegetables,name='vegetablesdata'),
    path('shop/', views.shop, name='shop'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('registration/',views.CustomerRegistrationView.as_view(),name='registration'),
    path('accounts/login/',auth_views.LoginView.as_view(template_name='login.html',form_class=LoginForm),name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/',views.address,name='address'),
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='passwordchange.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'),name='passwordchange'),
    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'),name='passwordchangedone'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',form_class=MySetPasswordForm,success_url='/password-reset-complete/'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
