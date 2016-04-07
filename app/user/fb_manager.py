# -*-coding: utf-8 -*-
import json
import wget

from urllib2 import urlopen

from flask_oauth import OAuth, session

from config import FACEBOOK_APP_ID, FACEBOOK_APP_SECRET
from ..models import *

# for sorting
from collections import Counter

import os
from ..shop import shop_blueprint

# for download image
shop_image_path = os.path.join(shop_blueprint.root_path, 'image')

# for nlp
from konlpy.tag import Mecab

oauth = OAuth()
mecab = Mecab()

# same with
# find_data = set([u'팝', u'팜', u'판매', u'처분'])
# 아래 nouns 의 인덱스 탐색.
find_data = {u'팝', u'팜', u'판매', u'처분'}


def get_fb_user_name(userid, token):
    url = 'https://graph.facebook.com/v2.5/%s?access_token=%s' % (userid, token)
    return json.loads(urlopen(url).read())['name']


def get_fb_images_from_article(user, article_id):
    """
    :param user: user 객체
    :param article_id: article id
    :return: image src list
    """
    # https://graph.facebook.com/[article_id]/attachments?access_token=[access_token]
    url = 'https://graph.facebook.com/%s/attachments?access_token=%s' % (article_id, user.access_token)
    json_data = json.loads(urlopen(url).read())

    try:
        image_list = json_data['data'][0]['subattachments']['data']

        # IndexError 는 data[0]      -> 맨 끝 데이터일 경우 (data 의 length 가 0)
        # KeyError 는 subattachments -> 첨부파일이 없는 게시물일 경우
    except (IndexError, KeyError):
        return []
    else:
        # 기존 이미지 dict list 에서 src 만 추출해서 반환.
        return [image['media']['image']['src'] for image in image_list]


def get_fb_post_json(user):
    """
    :param user: 유저 객체
    :return: 유저의 모든 게시물 json 의 url
    """
    url = 'https://graph.facebook.com/me?access_token=%s&fields=posts' % user.access_token

    json_data = json.loads(urlopen(url).read())

    for article in json_data['posts']['data']:
        article['image'] = get_fb_images_from_article(user, article['id'])

    all_post_data = json_data['posts']['data']

    url = json_data['posts']['paging']['next']

    while True:
        json_data = json.loads(urlopen(url).read())

        if len(json_data['data']) == 0:
            break

        url = json_data['paging']['next']

        for article in json_data['data']:
            article['image'] = get_fb_images_from_article(user, article['id'])

        all_post_data.append(json_data['data'])

    return all_post_data

    # all_post_data[page][article]


def get_product_name_from_content(all_pos_data):
    # 일반 명사와 고유 명사만 갖고옴
    all_noun_data = [pos_data[0] for pos_data in all_pos_data if pos_data[1] in ['NNG', 'NNP']]

    # all_noun_data 와 find_data 중 겹치는 항목 찾기
    match_data = set(all_noun_data) & set(find_data)

    # maybe_product_names -> 판매 대상으로 추정되는 모든 이름들 모아놓은 것)
    # find_data 앞에 있는 모든 명사 모으기.
    # kcrong을 판매합니다 --> 'kcrong' 가져옴
    # 중복되는 이름을 차환 위해 set() 으로 형변환
    maybe_product_names = [all_noun_data[all_noun_data.index(data) - 1] for data in match_data]

    # 빈도에 기반한 정렬. (많이 나오는 항목일 수록 앞으로 오도록)
    # [1,2,3,1,2,1] -- sort --> [1,1,1,2,2,3] -- set() --> [1,2,3]
    # TODO: Set 후에 Sorting 하는게 더 비용이 낮지 않을까?
    sorted_product_names = set([name for name, cnt in Counter(maybe_product_names).most_common()])

    # product_name = ','.join(sorted_product_names)

    # 프로토 타입이므로 그냥 가장 빈도가 높은 명사 반환.. ㅜㅜ
    # TODO: 추후에 리펙토링 필요함.
    # TODO: Word2Vec 이용해 의미 분석

    try:
        return list(sorted_product_names)[0]
    except IndexError:
        return all_noun_data[0]


def get_price_from_content(all_pos_data):
    # 가격은 (pos 기준) NNBC 앞에 SN 을 찾으면 될 듯.
    # NNBC -> 체언-단위를 나타내는 명사
    # SN -> 숫자

    # 모든 숫자 데이터를 가져옴
    all_int_data = []
    all_noun_int_data = [pos_data[0] for pos_data in all_pos_data if pos_data[1] in ['SN', 'NNG', 'NNP']]

    # TODO: 모든 숫자데이터와 명사데이터를 가져와서, find_data 와 일치하는 데이터 앞에 있는 숫자 데이터를 가져올 것

    match_data = list(set(all_noun_int_data) & set(find_data))

    for data in match_data:

        # all_noun_int_data[:match_data.index
        search_data = all_noun_int_data[:match_data.index(data)]

        # search_data 에서 가장 뒤에 있는 숫자데이터를 찾을 것.
        try:
            all_int_data.append([data for data in search_data if data[1] == 'SN'][-1])
        except IndexError:
            continue

    # 원래는 단위명사까지 처리하여 가격을 파싱하려 했으나, 지금은 프로토타입 단계이므로 그냥 가장 처음에 나오는 숫자를 리턴.

    if len(all_int_data) == 0:
        for pos_data in all_pos_data:
            if pos_data[1] == 'SN':
                return pos_data[0]
        return 0

    else:
        return all_int_data[0]


def get_tag_list_from_content(message):
    word_list = message.replace('\n', ' ').split(' ')

    """
    word_list 의 요소 중에
    단어의 길이가 0 이 아니면서
    첫 글자 (word[0]) 가 # 인 word 들만 tag_list 에 포함
    """

    tag_list = [word[1:] for word in word_list if len(word) != 0 and word[0] == '#']

    return tag_list


def save_product_db(user, images, tags, price, name):
    p = Product(name, user, price, False)

    """
    for image, tag in zip(images, tags)
        이 코드를 사용하려 했으나, images 와 tags 의 길이가 다르면 에러 ㅜ
    """

    # 이미지 db 추가
    for image in images:
        file_download = wget.download(image, shop_image_path)
        filename = file_download.split('/')[-1]
        pi = ProductImage(filename)
        db.session.add(pi)

        p.image.append(pi)

    # 태그 db 추가
    for tag in tags:
        t = Tag(tag)
        db.session.add(t)

        p.tag.append(t)

    db.session.add(p)

    db.session.commit()

    return


def save_all_fb_article(user):
    all_article_data = get_fb_post_json(user)

    for article in all_article_data:
        try:
            message = article['message']
        except KeyError:
            continue

        except TypeError:
            all_article_data += article
            continue

        else:  # 만약 내용이 있는 게시물이면.

            pos_data = mecab.pos(message)
            tag_list = get_tag_list_from_content(message)

            # 만약 해당 게시물에 파니 태그가 있다면 (파싱 대상 게시물 이라면)
            if 'panee' in tag_list:
                price = get_price_from_content(pos_data)
                product_name = get_product_name_from_content(pos_data)
                # article['image']

                print "%s 는 %s 원입니다." % (product_name, price)

                if Product.query.filter_by(user=user, name=product_name, price=price).first() is not None:
                    # 기존에 파싱되어 있는 상품이라면 넘긴다
                    continue

                save_product_db(user, article['image'], tag_list, price, product_name)


facebook = oauth.remote_app('facebook',
                            base_url='https://graph.facebook.com/',
                            request_token_url=None,
                            access_token_url='/oauth/access_token',
                            authorize_url='https://www.facebook.com/dialog/oauth',
                            consumer_key=FACEBOOK_APP_ID,
                            consumer_secret=FACEBOOK_APP_SECRET,
                            request_token_params={'scope': ['email', 'user_posts']}
                            )


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')
