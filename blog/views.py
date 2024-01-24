from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail

from .models import Post
from .forms import EmailForm

# Create your views here.
def postlist(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list,3)
    page_number = request.GET.get('page',1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/postlist.html',{'posts':posts})

def post_detail(request,year,month,day,post):
    post = get_object_or_404(Post,status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,'blog/detail.html',{'post':post})


def post_share(request,post_id):
    post = get_object_or_404(Post,id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
        post_url = request.build_absolute_uri(
            post.get_absolute_url())
        subject = f"{cd['name']} recommends you read {post.title}"
        message = f"Read {post.title } at {post_url}\n\n {cd['name']}\'s comments: {cd['comments']}"
        send_mail(subject, message, 'ehanson787@gmail.com',[cd['to']])
        sent = True
    else:
        form = EmailForm()
    return render(request,'blog/email.html',{'post':post,'form':form, 'sent':sent})
