from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from boards.models import Board, Comment
from boards.forms import BoardForm, CommentForm


# 사이트/boards 첫 화면
@require_GET
def index(request):  # 클라이언트의 request 요청을 받겠다.
    boards = Board.objects.order_by('-pk')  # 게시판 등록된 글을 내림차순으로  # 오름차순은 order_by('pk')
    context = {'boards': boards}
    return render(request, 'boards/index.html', context)  # 클라이언트의 request 를 boards/index.html 로 보내고 context 도 보낸다.


# 로그인한 사용자에 한해 게시글 등록 기능 구현
@login_required  # 로그인 상태에서만 아래 함수 접속 및 처리
@require_http_methods(['GET', 'POST'])  # GET 과 POST 만 받겠다 라는 의미
def create(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)  # 바로 저장하지 않고
            board.user = request.user        # 유저값을 대입한 뒤
            board = form.save()              # 저장한다.
            return redirect('boards:detail', board.pk)
    else:
        form = BoardForm()
    context = {'form': form}
    return render(request, 'boards/form.html', context)


# 게시글 상세 보기 기능 구현
# boards/3/
@require_GET  # GET 만 받겠다 라는 의미
def detail(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    #  Board 를 참조하고 있는 모든 댓글
    comments = board.comment_set.order_by('-pk')
    comment_form = CommentForm()
    person = get_object_or_404(get_user_model(), pk=board.user_id)
    context = {
        'board': board,
        'comment_form': comment_form,
        'comments': comments,
        'person': person,
    }
    return render(request, 'boards/detail.html', context)


# 게시글 삭제 기능 구현
# POST boards/3/delete/
@require_POST
def delete(request, board_pk):
    # 특정 보드를 불러와서 삭제한다.
    board = get_object_or_404(Board, pk=board_pk)
    # 요청을 보낸 유저와 게시글의 작성자가 같을때만 삭제
    if request.user != board.user:
        return redirect('boards:detail', board_pk)
    board.delete()
    return redirect('boards:index')


# 로그인한 사용자에 한해 글 수정 기능 구현
@login_required  # 로그인 상태에서만 아래 함수 접속 및 처리
@require_http_methods(['GET', 'POST'])  # GET 과 POST 만 받겠다 라는 의미
def update(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    # 원작자가 작성한 게시글을 다른사람이 수정하지 못하게 하는 처리
    # request.user : 요청을 보내는 사용자, board.user : 게시글 수정을 하는 사용자
    if request.user != board.user:
        return redirect('boards:detail', board_pk)
    #  POST boards/3/update/
    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            board = form.save(commit=False)  # 바로 저장하지 않고
            board.user = request.user        # 유저값을 대입한 뒤
            board = form.save()              # 저장한다.
            return redirect('boards:detail', board.pk)
    #  GET boards/3/update/
    else:
        form = BoardForm(instance=board)  # board 데이터 할당
    context = {
        'form': form,
        'board_pk': board_pk,
    }
    return render(request, 'boards/form.html', context)


# 댓글 등록 기능 구현
@require_POST  # POST 만 받겠다 라는 의미
def comments_create(request, board_pk):
    # 로그인하지 않은 사용자 차단
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    # 댓글 작성 로직
    comment_form = CommentForm(request.POST)  # model form 에 사용자 입력을 받는다.
    # 유효성 검사
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
    # 유저 정보 할당
        comment.user = request.user
        # 같은 말 comment.user_id = request.user.id
    # board 정보 할당
        comment.board_id = board_pk  # pk 로 할당
    # 저장
        comment.save()

    return redirect('boards:detail', board_pk)


# 댓글 삭제 기능 구현
@require_POST  # POST 만 받겠다 라는 의미
def comments_delete(request, board_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.user == request.user:
        comment.delete()
    # 댓글 삭제 로직
    return redirect('boards:detail', board_pk)


# '좋아요' 기능 구현
# '좋아요'와 '좋아요 취소'를 함수 2개로 만들어도 되지만 한개의 like 에서 if 문을 사용해서 분기 처리하는게 좋다.
@login_required()
def like(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    user = request.user
    # board 를 좋아요 누른 모든 사람중에서 user 가 있다면
    if user in board.like_users.all():
        board.like_users.remove(user)  # 좋아요 해제
    else:  # 아니라면
        board.like_users.add(user)  # 좋아요 추가
    return redirect('boards:detail', board_pk)


# '싫어요' 기능 구현
# '싫어요'와 '싫어요 취소'를 함수 2개로 만들어도 되지만 한개의 dislike 에서 if 문을 사용해서 분기 처리하는게 좋다.
def dislike(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    user = request.user
    # board 를 싫어요 누른 모든 사람중에서 user 가 있다면
    if user in board.dislike_users.all():
        board.dislike_users.remove(user)  # 싫어요 해제
    else:  # 아니라면
        board.dislike_users.add(user)  # 싫어요 추가
    return redirect('boards:detail', board_pk)


# '팔로우' 기능 구현
@login_required
def follow(request, board_pk, user_pk):
    user = request.user
    person = get_object_or_404(get_user_model(), pk=user_pk)

    if user != person:
        if user in person.followers.all():
            person.followers.remove(user)
        else:
            person.followers.add(user)
    return redirect('boards:detail', board_pk)

