from django.contrib import admin
from .models import Board, Comment


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'created_at', 'updated_at', )  # 파일 마지막에는 공백 한개 있어야 한다.
    readonly_fields = ['created_at', 'updated_at', ]  # 파일 마지막에는 공백 한개 있어야 한다.


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'content', 'created_at' )  # 파일 마지막에는 공백 한개 있어야 한다.
    readonly_fields = ['created_at', ]  # 파일 마지막에는 공백 한개 있어야 한다.

