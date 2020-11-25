from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from app.models import Post,Comment,teacher
from app.forms import emailform,add_post,UserForm
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.shortcuts import get_list_or_404, get_object_or_404
from django.core.mail import send_mail
from taggit.models import Tag
from django.shortcuts import render,redirect
from  django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def about(request):
    return render(request,'app\\about.html')

def terms(request):
    return render(request,'app\\terms.html')

@login_required
def post_list_view(request,tag_slug=None):
    post_list=Post.objects.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        post_list=post_list.filter(tags__in=[tag])
    paginator=Paginator(post_list,3)
    page_number=request.GET.get('page')
    try:
        post_list=paginator.page(page_number)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.page(paginator.num_pages)
    return render(request,'app\\ppost_list.html',{'post_list':post_list,'tag':tag})

@login_required
def detail_view(request,year,month,date,post):
    post=get_object_or_404(Post,slug=post,
                            status='published',
                            publish__year=year,
                            publish__month=month)
    comments=post.comments.filter(active=True)
    csubmit=False
    if request.method=='POST':
            list=Comment()
            list.name=request.user
            t=request.user
            list.email=t.email
            list.body=request.POST.get("comment")
            list.post=post
            list.save()
            csubmit=True
    else:
        pass
    return render(request,'app\detail.html',{'list':post,'csubmit':csubmit,'comments':comments})


@login_required
def create(request):
    form=add_post()
    if request.method=='POST':
        form=add_post(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    if request.user!=None:
        current_user = request.user
        t = teacher.objects.filter(name__iexact=current_user)
        if t:
            return render(request,'app\\create.html',{'form':form})
        else:
            return render(request,'app\\sorry.html')

class showpost(LoginRequiredMixin,ListView):
    model=Post


def register(request):
    registered=False
    if request.method=='POST':
        user_form=UserForm(request.POST)
        if user_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user_form.save()
            registered=True
        else:
            print(user_form.errors)
    else:
        user_form=UserForm()
    return render(request,'app\\register.html',{'user_form':user_form,'registered':registered})

@login_required
def sharmebymail(request,id):
    post=get_object_or_404(Post,id=id,status='published')
    form=emailform()
    sent=False
    if request.method=='POST':
        form=emailform(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            subject='Message from '+cd['name']+'('+cd['fromm']+") on reading article on KRITIKA'S BLOG "
            message=cd['comments']+"\n"+'Title is '+post.title+'\n'+post.body
            send_mail(subject,message,cd['fromm'],[cd['to']])
            sent=True
    return render(request,'app\\sharemail.html',{'form':form,'list':post,'sent':sent})
