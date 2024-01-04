from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('home_page/', views.home_page, name='home'),
    path('coding/', views.coding, name='coding'),
    path('before_coding/', views.before_coding, name='before_coding'),
    path('about/', views.about, name='about'),
    path('FAQ/', views.faq, name='faq'),
    path('training/<int:training_num>/', views.training, name='training'),
    path('trainingExplanations/<int:training_num>/', views.training_explanations, name='trainingExplanations'),
    path('translating/', views.translating, name='translating'),
    path('suggesting/', views.suggesting, name='suggesting'),
    path('support_suggestion/<int:suggestion_id>/<str:suggestion_type>/', views.support_suggestion, name='support_suggestion'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/',  views.logout, name='logout'),
    path('Logout/', views.custom_logout, name='custom_logout'),
    path("admin/", admin.site.urls),
    path("register/", views.user_registration, name='user_registration'),
    path("coding_submitted/", views.coding_submitted, name='coding_submitted'),
    path("suggestion_submitted/", views.suggestion_submitted),
    path("contact_submitted/", views.contact_submitted, name="contact_submitted"),
    path('guest_registration/', views.guest_registration),
    path('get_basic_terms/', views.get_basic_terms_to_translate, name='get_basic_terms'),
    path('get_translated_terms/', views.get_translated_terms, name='get_translated_terms'),
    path('get_related_links_ids/', views.get_related_links_ids, name='get_related_links_ids'),
    path('get_related_link_url/', views.get_related_link_url, name='get_related_link_url'),
    path('registration_submitted/', views.registration_submitted, name='registration_submitted'),
    path('translating_submitted/', views.translating_submitted, name='translating_submitted'),
    path('profile/<username>/', views.profile_page, name='profile'),
    path("edit_picture/", views.edit_profile_picture, name="edit_picture"),

    path('register_email_confirmation/', views.register_email_confirmation, name='register_email_confirmation'),
    path('change_email_confirmation/', views.change_email_confirmation, name='change_email_confirmation'),
    path("registration_submitted/<uidb64>/<token>/", views.activate_registration, name='activate_registration'),
    path("profile/<uidb64>/<token>/", views.activate_email_change, name='activate_email_change'),


    # reset password:
    path("reset_password/", auth_views.PasswordResetView.as_view(), name="reset_password"),
    path("reset_password_sent/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset_password_complete/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("password_change/", auth_views.PasswordChangeView.as_view(), name="password_change"),
    path("password_change_done/", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),

    path('get_stop_coding/', views.get_stop_coding, name='get_stop_coding'),

    # forum
    path('forum/', views.forum, name='forum'),
    path('discussions/', views.discussions, name='discussions'),
    path('discussions/<str:category>/', views.discussions, name='discussions'),
    path('add_comment/', views.add_comment, name='add_comment'),

]
