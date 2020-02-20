from django.db import models
from django.conf import settings


class Board(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # N : M 관계
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='like_boards',  # 다대다 관계 설정
        blank=True,  # 게시글을 좋아하는 사람이 없을 수도 있으니 blank=True
    )
    # related_name='like_boards 를 설정하지 않는다면
    # user.board_set.all() 에서 장고는 1. 내가 지금까지 작성한 게시글, 2. 내가 좋아요 한 게시글 2개 무엇을 가져와야할지 모른다.
    # 그래서
    # user.board_set.all() 은 1. 내가 지금까지 작성한 게시글을 표시
    # user.like_boards.all() 은 2. 내가 좋아요 한 게시글을 표시
    # 이렇게 지정해줘야 한다.
    dislike_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='dislike_boards',  # 다대다 관계 설정
        blank=True,  # 게시글을 좋아하는 사람이 없을 수도 있으니 blank=True
    )

    # 데이터 표현식 변경
    def __str__(self):
        return f'{self.pk}, {self.title}'


class Comment(models.Model):
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.content}'

