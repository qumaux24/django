
from django.shortcuts import render,redirect, get_object_or_404
from .models import Post, Image, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
# Create your views here.

# 게시글 목록
def list(request):
    posts = Post.objects.all().order_by('-created_at')
    request.session['previous_page']=request.get_full_path()
    page=request.GET.get('page', '1')
    # list=Post.objects.order_by('-created_at')
    paginator=Paginator(posts, 10)
    page_obj=paginator.get_page(page)
    context={
        # 'posts': posts,
        'list': page_obj,

        }
    return render(request, 'main.html', context)

# 게시글 새로 작성하기
def write(request): #새 글 폼 띄워줌, 게시글 저장
    #post랑 get의 차이: post는 비밀화되어있는 정보들 get은 주소창에 그대로 정보가 뜬다.
    #get은 비어있는 느낌, post는 꽉 차있는 느낌
    if request.method=='POST':
        form=PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.writer=request.user
            post.save()
            
            for img in request.FILES.getlist('image',None):
                Image.objects.create(post=post, image=img)
                
            return redirect('post:list')
    else:
        form=PostForm() #request는 현재 상황인데 없으니까 아예 새 포스트를 불러옴
        return render(request,'write.html', {'form':form})

# 게시글 보여주기
def show(request, post_id):
    post = get_object_or_404(Post, pk =post_id)
    images=Image.objects.filter(post=post)
    comments = post.comment_set.all()  
    commentForm = CommentForm() 
    context = {
        'post': post,
        'images': images,
        'comments': comments,
        'commentForm': commentForm, 
    }
    return render(request, 'detail.html', context)

# 게시글 수정, 삭제
@login_required(login_url='/accounts/home/login')
def deleteget(request, post_id):
    post=Post.objects.get(id=post_id)
    post.delete()
    return redirect('post:list')

def updateget(request, post_id):
    post=Post.objects.get(pk=post_id)
    images=Image.objects.filter(post=post)
    if request.method=='POST':
        postForm=PostForm(request.POST, request.FILES.getlist('image'), instance=post)
        
        if postForm.is_valid():
            postForm.save()
            for img in request.FILES.getlist('new_image',None):
                Image.objects.create(post=post, image=img)
            #수정을 했을 경우에만 작성시간 밑에 수정시간이 뜨게
            return redirect('post:show', post_id)
    else:
        postForm=PostForm(instance=post)
        context={
            'postForm':postForm,
            'post_id':post_id,
            'images':images,
        }
        return render(request, 'updated.html', context)                

# 이미지 삭제
def image_delete(request, post_id):
    if request.user.is_authenticated:
        post=get_object_or_404(Post, pk=post_id)
        image_id=request.POST.get('image_id')
        image=get_object_or_404(Image, id=image_id, post=post)
        if request.user == post.writer:
            image.delete()
    return redirect('post:show', post_id=post_id)

# 댓글 기능
@require_POST
def comments_create(request, pk):
    if request.user.is_authenticated:
        post=Post.objects.get(pk=pk)
        commentForm=CommentForm(request.POST)
        if commentForm.is_valid():
            comment=commentForm.save(commit=False)
            comment.post=post
            comment.writer=request.user
            comment.save()
        return redirect('post:show', pk)
    return redirect('accounts/home/login')

@require_POST
def comments_delete(request, pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.writer:
            comment.delete()
    return redirect('post:show', pk)

# 좋아요 기능
@require_POST
def likes(request, post_pk):
    if request.user.is_authenticated:
        post=get_object_or_404(Post, pk=post_pk)
        if post.like_users.filter(pk=request.user.pk).exists():
            post.like_users.remove(request.user)
        else:
            post.like_users.add(request.user)
        return redirect('post:show', post_pk)
    return redirect('accounts/home/login')
