from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from .models import Blogpost,Blogcomment
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Contact
from blog.templatetags import extras
from taggit.models import Tag
from django.db.models import Count
# Create your views here.
def homepage(request):
    post = Blogpost.objects.all().order_by('-time_stamp')
    return render(request,'blogtemps/home.html',{'post':post})
def bloghome(request):
    # fetching all blogposts form the database
    myposts = Blogpost.objects.all().order_by('-time_stamp')
    return render(request,'blogtemps/blogindex.html',{'mypost':myposts})
def blogpost(request,slug):
    # geting the selected post from the list
    post = get_object_or_404(Blogpost, slug=slug)
    post.blog_views = post.blog_views + 1
    post_tags = post.tags.all()
    similar_post = Blogpost.objects.filter(tags__in = post_tags)
    similar_post = similar_post.exclude(slug=slug)
    similar_post = similar_post.annotate(tag_count = Count('tags')).order_by('-tag_count','-time_stamp')
    post.save()
    comments = Blogcomment.objects.filter(post=post,parent = None)
    replies = Blogcomment.objects.filter(post=post).exclude(parent = None)
    repDict={}
    for comreply in replies:
        if comreply.parent.com_id not in repDict.keys():
            repDict[comreply.parent.com_id] = [comreply] 
        else:
            repDict[comreply.parent.com_id].append(comreply)
    Context = {'post':post,'comments':comments,'user':request.user,'repDict':repDict,'similar_post':similar_post}
    return render(request,'blogtemps/blogpost.html',Context)

# Defining view for Comment API
def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        user = request.user
        post_id = request.POST.get('post_id')
        commentid = request.POST.get('commentid')
        post = Blogpost.objects.get(post_id = post_id)
        if commentid == "":
            comments = Blogcomment(comment = comment,user = user,post = post)
            comments.save()
            messages.success(request,'Your comment has been posted successfully')
        else:
            parent = Blogcomment.objects.get(com_id= commentid)
            comments = Blogcomment(comment = comment,user = user,post = post,parent = parent)
            comments.save()
            messages.success(request,'Your repl has been posted successfully')
    return redirect(f"/blogpost/{post.slug}")

def tagged(request,slug):
    tag = get_object_or_404(Tag,slug=slug)
    post = Blogpost.objects.filter(tags = tag)
    context = {
        'tag':tag,
        'post':post
    }
    return render(request,'blogtemps/blogindex.html',context)
# managing contact us page
def contactus(request):
    # messages.error(request,'Welcome to contact')
    if request.method == "POST":
        print(request)
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc = request.POST.get('desc','')
        
        if len(name)<2 or len(email)<10 or len(phone)<7 or len(desc)<20:
            messages.error(request,'Please fill the form correctly!')
        else:
            contact = Contact(user_name =name, user_email =email,user_phone = phone, message_content = desc)
            contact.save()
            messages.success(request,'Your message has been sent.')
            thank = True
            return render(request,'hometemps/contactus.html',{'thank':thank})
    return render(request,'blogtemps/contact.html')

# handling about us
def aboutus(request):
    return render(request,'blogtemps/about.html')

# search query functionality
def searchbox(request):
    search_query = request.GET['searchbox']
    if len(search_query)>50:
        found_data = Blogpost.objects.none()
    else:
        found_datatitle = Blogpost.objects.filter(title__icontains = search_query)
        found_datacontent = Blogpost.objects.filter(blog_content__icontains = search_query)
        found_dataauther = Blogpost.objects.filter(auther__icontains = search_query)
        found_datatimestamp = Blogpost.objects.filter(time_stamp__icontains = search_query)
        found_data = found_datatitle.union(found_datacontent,found_datatitle,found_dataauther,found_datatimestamp)
    if found_data.count() == 0:
        messages.error(request,'Please Enter the correct search query!')
    search_content = {'found_data':found_data,'query':search_query}
    return render(request,'blogtemps/search.html',search_content)
    
# handling signup function
def handlesignup(request):
    if request.method == 'POST':
        # Getting POST parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        #  Checks for error input
        # user name length check
        if len(username)>10:
            messages.error(request,'User name is too lengthy, must be under 10 characters')
            return redirect('Home')
        # user name alphanumeric check
        if not username.isalnum():
            messages.error(request,'Username must be alphanumberic. Username should not contain any special character')
            return redirect('Home')
        # password check
        if password != confirmpassword:
            messages.error(request,'Password does not match')
            return redirect('Home')

        # Creating the user
        myuser = User.objects.create_user(username,email,password)
        myuser.first_name = fname
        myuser.last_name = lname
        try:
            myuser.save()
            messages.success(request,'Your account has been successfully registed')
            return redirect('Home')
        except:
            messages.error(request,'user already exists')
            return redirect('Home')
    else:
        return HttpResponse('404 - Not Found')

# handling login function
def handlelogin(request):
    if request.method == 'POST':
        # Getting POST parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        user = authenticate(username=loginusername,password=loginpassword)
        if user is not None:
            login(request,user)
            messages.success(request,'Logged in successfully')
            return redirect('Home')
        else:
            messages.error(request,'Invalid credentials,Please try again')
            return redirect('Home')
            
    return HttpResponse('404 - Not Found')
def handlelogout(request):
   
    logout(request)
    messages.success(request,'Successfully Logged out')
    return redirect('Home')

    