from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from .forms import CustomUserChangeForm, CustomUserCreationForm


# 회원 가입 기능
@require_http_methods(['GET', 'POST'])
def signup(request):
    # 사용자가 로그인 상태에서 또 로그인 화면이 뜨지 않게 하는 방법
    if request.user.is_authenticated:
        return redirect('boards:index')
    # POST
    if request.method == 'POST':
        # 사용자 회원가입 로직
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():  # 사용자가 정보를 담아서 모든 정보가 유효하다면
            user = form.save()  # 회원가입 된 상태를 뜻함.
            auth_login(request, user)  # 회원가입과 동시에 로그인 상태를 만듬
            return redirect('boards:index')
    # GET accounts/signup/
    else:
        form = CustomUserCreationForm()
        # context = {'form': form} # 주석처리 가능
        # return render(request, 'accounts/signup.html', context) # 주석처리 가능
    # 유효하지 않다면 회원가입 다시 해주세요 사용자에게 보여줘야 함.
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)


# 로그인 기능
@require_http_methods(['GET', 'POST'])
def login(request):
    # 사용자가 로그인 상태라면 더이상 로그인 페이지가 안 나타나게!
    if request.user.is_authenticated:
        return redirect('boards:index')
    # POST
    if request.method == 'POST':
        # 로그인 로직 실행
        form = AuthenticationForm(request, request.POST)  # 사용자가 보낸 입력을 받는다.
        # 사용자 입력 유효성 검사
        if form.is_valid():
            # 로그인 구현
            auth_login(request, form.get_user())
            # print('next :', request.GET.get('next'))    # 출력값 : next : /boards/create/
            return redirect(request.GET.get('next') or 'boards:index')
            # 기존에 로그아웃 했다가 로그인 하면 홈화면으로 갔었는데 이제는 boards/create로 자동으로 넘어간다.

    # GET accounts/login  -> html 페이지만 렌더링
    else:
        form = AuthenticationForm()
        # context = {'form': form}
        # return render(request, 'accounts/login.html', context)
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


# 로그아웃 기능
@require_GET
def logout(request):
    # 로그아웃 로직
    auth_logout(request)
    return redirect('boards:index')


# 계정 정보 변경 기능
@require_http_methods(['GET', 'POST'])
# 로그인 상태에서만 아래 함수 접속 및 처리
@login_required
def update(request):
    if not request.user.is_authenticated:  # 만약 로그인 한 사용자가 아니라면  # 한마디로 로그인 안한사람은 update 접근 불가하게 만듬
        return redirect('boards:index')

    if request.method == 'POST':
        # 업데이트 로직 수행
        form = CustomUserChangeForm(request.POST, instance=request.user)  # 수정할 때 항상 인스턴스 속성을 줘야 한다.
        # embed()  # 잠시 멈춤 이 위까지 실행되므로 터미널에서 form 치면 관련 정보를 얻을 수 있다.
        # forms.py 에 원하는 정보 추출할 때 쓴다.
        if form.is_valid:
            form.save()
            return redirect('boards:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
        # context = {'form': form}
        # return render(request, 'accounts/update.html', context)
    context = {'form': form}                                # 사용자가 갖고 있는 폼을 갖고 다시 리턴하게끔 할 수 있다.
    return render(request, 'accounts/update.html', context)


# 계정 비밀번호 변경 기능
@require_http_methods(['GET', 'POST'])
# 로그인 상태에서만 아래 함수 접속 및 처리
@login_required
def change_password(request):
    if request.method == "POST":
        # 사용자의 패스워드 변경 로직
        form = PasswordChangeForm(request.user, request.POST)  # 반드시 특정 사용자가 있어야 비밀번호를 바꿀 수 있다.
        # 유효성 검사
        if form.is_valid():
            form.save()
            # 세션의 정보화 회원의 정보가 달라져서 세션을 유지한 상태로 새롭게 업데이트
            update_session_auth_hash(request, request.user)
            return redirect('boards:index')
    else:
        form = PasswordChangeForm(request.user)  # 반드시 특정 사용자가 있어야 비밀번호를 바꿀 수 있다.
        # context = {'form': form}
        # return render(request, 'accounts/change_password.html', context)
    context = {'form': form}
    return render(request, 'accounts/change_password.html', context)


# 계정 삭제 기능
@require_POST
def delete(request):
    # 유저 삭제 로직
    request.user.delete()
    return redirect('boards:index')

