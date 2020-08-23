from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm
from .models import Post, Group
from django.core.paginator import Paginator
from django.shortcuts import render

from .models import Post

def index(request):
        post_list = Post.objects.order_by('-pub_date').all()
        paginator = Paginator(post_list, 10)  # показывать по 10 записей на странице.

        page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
        page = paginator.get_page(page_number)  # получить записи с нужным смещением
        return render(
            request,
            'index.html',
            {'page': page, 'paginator': paginator}
       )



def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:12]
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'group.html', {'group': group, 'page': page, 'paginator': paginator})


@login_required
def new_post(request):
    if not request.POST:
        form = PostForm()
        return render(request, "new_post.html", {"form": form})

    form = PostForm(request.POST)
    if not form.is_valid():
        return render(request, "new_post.html", {"form": form})

    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('index')

def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts_count = Post.objects.filter(author=author).count()
    author_posts = Post.objects.filter(author=author).order_by('-pub_date')
    paginator = Paginator(author_posts, 6)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'profile.html', {
        'page': page,
        'paginator': paginator,
        'posts_count': posts_count,
        'author': author
    })


def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, author=author.id, id=post_id)
    posts_count = Post.objects.filter(author=post.author).count()
    return render(request, 'post.html', {
        'posts_count': posts_count,
        'post': post,
        'author': author
    })




    # тут тело функции. Не забудьте проверить,
    # что текущий пользователь — это автор записи.
    # В качестве шаблона страницы редактирования укажите шаблон создания новой записи
    # который вы создали раньше (вы могли назвать шаблон иначе)



@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return post_view(request, username, post_id)

    form = PostForm(request.POST, instance=post)

    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post', username=post.author, post_id=post.id)
        return render(request, 'new.html')

    return render(request, "new.html")