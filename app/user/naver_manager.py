# -*-coding: utf-8 -*-

from urllib.request import urlopen
from xml.etree.ElementTree import fromstring

from bs4 import BeautifulSoup

"""
네이버 블로그는 클릭후 내부 ajax 를 통해 게시물 데이터를 불러온다.
따라서 게시물 이미지를 받아오려면 js 렌더링이 필요하다..
selenium 이라는 모듈을 사용하면 될 것 같다.

[+] phantomjs 라는 프로그램을 이용하려면 설치가 필요하다..
http://attester.ariatemplates.com/usage/phantom.html#installing_phantomjs_on_ubuntu <-- 여기를 참고하면 될 것 같다.


In [1]: from selenium import webdriver

In [2]: browser=webdriver.PhantomJS()

In [3]: browser.get('http://seleniumhq.org/')

In [4]: browser.title
Out[4]: u'Selenium - Web Browser Automation'


---------------
뭐시여 js 렌더링을 다 했는데도 소스가 똑같다
urlopen() 으로 열어도 js 렌더링이 되던가, 아니면 browser.get() 만 실행할 경우 js 렌더링이 되지 않던가 둘중 하나인데...

---------------
소스를 뜯어보니 렌더링이 아닌, iframe 형식으로 코딩되어 있다. 왜 이렇게 했는 지는 모르겠지만,
iframe 안에 iframe 이 있고 그 iframe 안에 네이버 포스팅이 들어있다.

따라서 내부 iframe src 를 파싱해서 읽어온 다음 네이버 포스팅 파싱이 필요하다.

"""


def get_blog_main_source(article_link):
    """
    :param article_link: 해당 게시물 링크
    :return: 해당 게시물의 메인 html 데이터

        네이버 블로그는 두 번의 iframe 을 거쳐 메인 블로그 소스를 가져온다. 따라서 iframe 의 src 를 가져와 urlopen 을 시킨 후,
        read() 하여 다시 iframe.src 를 가져오는 것이 필요하다.
        해당 소스는 반복문을 사용하는 것이 바람직해 보인다.

    """
    html_parse = BeautifulSoup(urlopen(article_link).read())

    sub_iframe_src = html_parse.find('frame').get('src')

    main_iframe_html = BeautifulSoup(urlopen(sub_iframe_src).read())
    main_iframe_src = 'http://blog.naver.com/' + main_iframe_html.find('frame').get('src')

    main_blog_data = urlopen(main_iframe_src).read()

    return main_blog_data


def get_image_from_article(article_link):
    # browser = webdriver.PhantomJS()
    # browser.get(article_link)
    html_data = get_blog_main_source(article_link)
    html_parse = BeautifulSoup(html_data)

    all_image = html_parse.find('div', {'id': 'postViewArea'}).findChildren('img')

    # img 태그의 src 부분만 파싱해서 리스트로 변환
    return [image.get('src') for image in all_image]


def parse_blog_data(xml_raw):
    xml_data = fromstring(xml_raw)

    all_article = xml_data[0].findall('item')

    # 모든 게시물을 가공한 정보를 담은 list
    all_article_data = []

    # 게시물 하나 마다
    for article in all_article:
        # 게시물 tag 와 그 text 를 튜플로 묶고, 그 튜플들을 dict 로 변환
        # 따라서 이 Loop 가 도는 횟수는 len(all_article) 과 같다.

        all_article_data.append(
            # article_info.tag : article_info.text
            dict((article_info.tag, article_info.text) for article_info in article)
        )

        """
            위 all_article_data 에서 article의 link 들만 뽑아 get_image_from_article 함수에 전달해야 한다.

            별도의 loop 를 돌려서 처리하는게 빠를까? 아니면 저 append 하는 loop in list 에서 처리하는 게 더 빠를까?

            우선 하나 더 loop 를 돌리는 것으로 처리했다. 나중에 비용계산을 해봐야 겠다.
        """

        for article in all_article_data:
            article['image'] = get_image_from_article(article['link'])

    """
        처리후 article 데이터 접근법
        all_article_data --> 모든 게시물의 리스트
        all_article_data[0] --> 게시물 하나
        all_article_data[0]['category'] --> 해당 게시물의 category 조회


        >>> all_article_data[0].keys()
        ['category', '{http://activitystrea.ms/spec/1.0/}verb', 'description', 'pubDate', 'title', 'author', 'tag', 'link', 'guid', '{http://activitystrea.ms/spec/1.0/}object-type']

        >>> all_article_data[0]['category']
        'photo diary'
    """

    blog_data = {'title': xml_data[0].findtext('title'), 'article': all_article_data}

    return blog_data


def get_all_naver_article(user, naver_id):
    url = 'http://blog.rss.naver.com/' + naver_id
    xml_raw = urlopen(url).read()

    blog_data = parse_blog_data(xml_raw)

    # TODO: 가져온 blog_data 를 DB 에 저장하기.
    print(blog_data)



