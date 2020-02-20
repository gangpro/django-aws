from django.urls import path
from boards import views

# 경로 앱 이름 지정 'boards:detail'
app_name = 'boards'

# boards/
urlpatterns = [
    # boards
    path('', views.index, name='index'),  # boards/  # 첫 화면
    path('<int:board_pk>/', views.detail, name='detail'),  # boards/@/
    path('create/', views.create, name='create'),  # boards/create/
    path('<int:board_pk>/delete/', views.delete, name='delete'),  # boards/@/delete/
    path('<int:board_pk>/update/', views.update, name='update'),  # boards/@/update/

    # comments
    # POST /boards/@/comments
    path('<int:board_pk>/comments/', views.comments_create, name='comments_create'),  # boards/@/comments/
    path('<int:board_pk>/comments/<int:comment_pk>/delete/', views.comments_delete, name='comments_delete'),  # boards/@/comments/@/delete/

    # like & dislike
    path('<int:board_pk>/like/', views.like, name='like'),  # 특정 게시글 좋아요 path  # boards/@/like/
    path('<int:board_pk>/dislike/', views.dislike, name='dislike'),  # 특정 게시글 좋아요 path  # boards/@/dislike/

    # follow
    path('<int:board_pk>/follow/<int:user_pk>/', views.follow, name='follow'),  # boards/@/follow/@/

    # Path Converter  <꺽쇠>
    # str : /(슬래시)를 제외한 모든 문자열과 매치된다. 타입이 지정되지 않았다면 디폴트로 str 타입을 사용한다.
    # int : 0 또는 양의 정수와 매치된다. 매치된 정수는 python 의 int 타입으로 변환된다.
    # slug : slug 형식의 문자열(ASCII, 숫자, 하이픈, 밑줄로만 구성됨)과 매치된다.
    # uuid : UUID 형식의 문자열과 매치된다. 매치된 문자열은 python 의 UUID 타입으로 변환된다.
    # path : /(슬래시)를 포함한 모든 문자열과 매치된다. 이는 URL 패턴의 일부가 아니라 전체를 추출하고자 할때 많이 사용한다.
]

