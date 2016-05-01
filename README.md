# 서버 실행 커맨드 정리
    
## 처음 이용시
#### (아래 커맨드 실행 후, "git pull 이후" 로 넘어가면 됩니다.)
 
    
    source env/bin/activate
: 파이썬 가상환경을 이용합니다.
 
---
    pip3 install -r dev.txt
: 필요한 패키지를 설치합니다.

---
    python manage.py db init
: db migrate 를 위한 파일을 만듭니다. 

## git pull 이후

    python manage.py db migrate
: 모델링 소스에서 기존 디비와 다른 부분이 있는지 검증합니다.

---
    python manage.py db upgrade
: 모델링이 달라진 부분이 있다면, migration 을 진행합니다.

