from django.urls import path,include
from .views import homepage,contactus,aboutus,searchbox,handlesignup,handlelogin,handlelogout,bloghome,blogpost,postComment, tagged
urlpatterns = [
     # API to post a comment
    path('postComment/',postComment,name='postComment'),
    path('',homepage,name='Home'),
    path('contact/',contactus,name='ContactUs'),
    path('about/',aboutus,name='AboutUs'),
    path('blog/',bloghome,name='Bloghome'),
    path('blogpost/<str:slug>',blogpost,name='blogs'),
    path('tag/<slug:slug>',tagged,name='tagged'),
    path('search/',searchbox,name='Searchbox'),
    path('signup/',handlesignup,name='HandleSignup'),
    path('login/',handlelogin,name='HandleLogin'),
    path('oauth/',include('social_django.urls',namespace='social')),
    path('logout/',handlelogout,name='HandleLogout'),
    
]