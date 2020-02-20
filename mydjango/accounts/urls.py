from django.urls import path
from accounts import views


# 경로 앱 이름 지정 'accounts:index 앱 name 역할을 한다.'
app_name = 'accounts'


# accounts/@@@
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('update/', views.update, name='update'),
    path('password/', views.change_password, name='change_password'),
    path('delete/', views.delete, name='delete'),

    # Path Converter  <꺽쇠>
    # str : /(슬래시)를 제외한 모든 문자열과 매치된다. 타입이 지정되지 않았다면 디폴트로 str 타입을 사용한다.
    # int : 0 또는 양의 정수와 매치된다. 매치된 정수는 python 의 int 타입으로 변환된다.
    # slug : slug 형식의 문자열(ASCII, 숫자, 하이픈, 밑줄로만 구성됨)과 매치된다.
    # uuid : UUID 형식의 문자열과 매치된다. 매치된 문자열은 python 의 UUID 타입으로 변환된다.
    # path : /(슬래시)를 포함한 모든 문자열과 매치된다. 이는 URL 패턴의 일부가 아니라 전체를 추출하고자 할때 많이 사용한다.
]

