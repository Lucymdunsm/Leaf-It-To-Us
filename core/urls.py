from django.urls import path, re_path
from core import views

# These are preliminary URL patterns. You will have to change the views. calls to the correct method names.
urlpatterns = [
    re_path(r'^$', views.home, name = 'home'),
    # Reviews for the "about" section assume that FAQ and contact won't be on the same page.

    re_path(r'^about/$', views.about, name='about'),
    re_path(r'^contact/$', views.contact, name='contact'),
    re_path(r'^faq/$', views.faq, name='faq'),

    # Tea Catalog URLs. This assumes each sort (popularity, type, origin) will need its own URL.
    # I do not know what the difference between tea catalog and tea listings is.
    re_path(r'^teas/$', views.teas, name='teas'),
    re_path(r'^teas/popular/$', views.most_popular, name='popular'),
    re_path(r'^teas/type/$', views.type, name='type'),
    re_path(r'^teas/origin/$', views.origin, name='origin'),
    re_path(r'^teas/(?P<tea_name_slug>[\w\-]+)/$', views.show_tea, name='show_tea'),

    # Specific review pages have an id slug that is passed on to the view function.
    re_path(r'^reviews/$', views.reviews, name='reviews'),
    re_path(r'^reviews/(?P<review_id_slug>[\w\-]+)/$', views.show_review, name='show_review'),

    # Generic registration and login pages.
    re_path(r'^register/$', views.register, name='register'),
    re_path(r'^login/$', views.user_login, name='login'),
    re_path(r'^logout/$', views.user_logout, name='logout'),

    # Account pages. These will only show information if user is logged in.
    # Unsure how much is being shown on a single page (do wee need separate URLs for dashboard
    # and account details? Dashboard and saved teas?
    re_path(r'^account/$', views.show_account, name='show_account'),
    re_path(r'^account/settings/$', views.settings, name='settings'),
    re_path(r'^account/reviews/$', views.user_reviews, name='user_reviews'),
    re_path(r'^account/saved_teas/$', views.saved_teas, name='saved_teas'),

    # Search URLs. Unsure whether search will be its own page or just a bar on the home page.
    # Again, unsure what the difference between Tea catalog and tea listings is.
    re_path(r'^search/$', views.search, name='search'),
]