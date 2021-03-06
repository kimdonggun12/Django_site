from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post, Category, Tag
from django.contrib.auth.models import User


# Create your tests here.
class TestView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_django = User.objects.create_user(username='django', password='qlalfqjsgh1')

        self.user_django2 = User.objects.create_user(username='django2', password='qlalfqjsgh1')
        self.category_programming = Category.objects.create(name='programming', slug='programming')
        self.category_music = Category.objects.create(name='music', slug='music')

        self.tag_python_kor = Tag.objects.create(name='파이썬공부', slug = '파이썬공부')
        self.tag_python = Tag.objects.create(name='python', slug='python')
        self.tag_hello = Tag.objects.create(name='hello', slug='hello')

    def test_post_list(self):
        # 1.1 포스트 목록 페이지를 가져온다
        response = self.client.get("/blog/")
        # 1.2 정상적으로 페이지가 로드된다
        self.assertEqual(response.status_code, 200)
        # 1.3 페이지 타이틀은 'Blog'이다
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog')
        # 1.4 네비게이션 바가 있다.
        navbar = soup.nav
        # 1.5 Blog, About Me 문구가 있다
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        # 2.1 메인 영역에 게시물이 하나도 없다면
        self.assertEqual(Post.objects.count(),0)

        # 2.2 '아직 게시물이 없습니다' 문구가 보인다.
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)
        # 3.1 게시물이 2개 있다면
        post_001 = Post.objects.create(
            title = '첫번째 포스트입니다.',
            content = 'Hello world ',
            author = self.user_django,
            category = self.category_programming
        )
        self.post_001.tags.add(self.tag_hello)

        post_002 =  Post.objects.create(
            title = '두번째 포스트입니다.',
            content = '두번째 Hello world ',
            author = self.user_django2,
            category = self.category_music
        )
        self.assertEqual(Post.objects.count(), 2)

        # 3.2 포스트 목록 페이지를 새로고침했을 때
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)
        # 3.3 메인 영역에 포스트 2개의 타이틀이 존재한다.
        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        # 3.4 '아직 게시물이 없습니다'라는 문구는 더이상 보이지 않는다.
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

        self.assertIn(self.user_django.username.upper(), main_area.text)
        self.assertIn(self.user_django2.username.upper(), main_area.text)

    def test_post_detail(self):

        # 1.1 Post가 하나 있다.
        # post_001 = Post.objects.create(
        #     title = '첫번째 포스트입니다',
        #     content = 'Hello world',
        #     author = self.user_django
        # )
        # 1.2 포스트의 url이 'blog/1/'이다
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')

        # 2 첫 번째 포스트의 상세 페이지 테스트
        # 2.1 첫 번째 post url 로 접근하면 정상적으로 작동한다.
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 2.2 포스트 목록 페이지와 같은 네비게이션 바가 있따.
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('Aboutme', navbar.text)

        self.category_card_test(soup)
        # 2.3 첫 번째 포스트의 제목이 웹 브라우저 탭 타이틀에 들어 있따.
        self.assertIn(self.post_001.title, soup.title.text)

        # 2.4 첫 번째 포스트 제목이 포스트 영역에 있다.
        main_area = soup.find('div', id='main-area')
        post_area = soup.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.title)
        self.assertIn(self.user_django.username.upper(), post_area.text)


        # 2.6 첫번째 포스트 내용이 포스트 영역에 있따.
        self.assertIn(self.post_001.content, post_area.text)







