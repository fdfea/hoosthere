from django.test import TestCase, Client
from studentmatching.models import Profile, MessageBoardPost, MessageBoardCategory, Message
from django.contrib.auth.models import User
from studentmatching.forms import EditProfileForm, EditUserForm
from django.urls import reverse

# Create your tests here.
class ProfileTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='usertest')
        self.user2 = User.objects.create_user(username='user2')
        self.profile1 = Profile.objects.create(user_id=999,user=self.user1, major="CPE", minor="Math",classes_taken="CS_3240")
        self.profile2 = Profile.objects.create(user_id=99, user=self.user2, major="CS", minor="None",classes_taken="CS_2150")
        self.message = Message.objects.create(sender=self.user1,receiver=self.user2,viewer=self.user2,content='hi my name is usertest')
        self.message2 = Message.objects.create(sender=self.user2, receiver=self.user1, viewer=self.user1,content='hi my name is user2')

    def test_major_minor(self):
        self.assertEqual(self.profile1.major, "CPE")
        self.assertEqual(self.profile1.minor, "Math")
        self.assertEqual(self.profile1.classes_taken,"CS_3240")

    def test_messToUser(self):
        self.assertEqual(self.message.sender,self.user1)
        self.assertEqual(self.message.receiver,self.user2)
        self.assertEqual(self.message.content,'hi my name is usertest')

    def test_messToUser2(self):
        self.assertEqual(self.message2.sender,self.user2)
        self.assertEqual(self.message2.receiver,self.user1)
        self.assertEqual(self.message2.content,'hi my name is user2')

    def tearDown(self):
        self.profile1.delete()
        self.user1.delete()
        self.message.delete()
        self.message2.delete()

class FormRequestTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='usertest')
        self.profile1 = Profile.objects.create(user_id=999, user=self.user1, major="CPE", minor="Math",classes_taken="CS_3240")
#    def test_form(self):
#        client = Client()
#        response = self.client.get(reverse('help'))
#        self.assertEqual(response.status_code,200)
    def test_form2(self):
        data = {'major':self.profile1.major,'minor':self.profile1.minor,'classes_taken':self.profile1.classes_taken}
        form = EditProfileForm({'major':"CPE",'minor':"EE",'classes_taken':"OS"})
        self.assertTrue(form.is_valid())
        #self.assertTrue(form.Profile.major,"CPE")

    def tearDown(self):
        self.user1.delete()
        self.profile1.delete()



class UserEditTest(TestCase):
    def setUp(self):
        self.userTemp = User.objects.create_user(username='usertest', email='jd@gmail.com', first_name='jack',last_name='doe')

    def test_UserForm(self):
        form = EditUserForm({'email':'johndoe@gmail.com','first_name':'John','last_name':'Doe'})
        self.assertTrue(form.is_valid())

    def tearDown(self):
        self.userTemp.delete()

class MessageBoardTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='usertest')
        self.profile1 = Profile.objects.create(user_id=999, user=self.user1, major="CPE", minor="Math",classes_taken="CS_3240")
        self.category1 = MessageBoardCategory.objects.create(name="Miscellaneous")
        self.mess1 = MessageBoardPost.objects.create(message_title="HoosThere Example",message_body="Hello World!",poster=self.user1,category=self.category1)
        self.user2 = User.objects.create_user(username='usertest2')
        self.profile2 = Profile.objects.create(user_id=99, user=self.user1, major="EE", minor="CS",classes_taken="CS_2150")
        self.category2 = MessageBoardCategory.objects.create(name="Classes")
        self.mess2 = MessageBoardPost.objects.create(message_title="2150 Help",message_body="Need Help with AVl Trees",poster=self.user2,category=self.category2)

    def test_post(self):
        self.assertEqual(self.mess1.poster,self.user1)
        self.assertEqual(self.mess1.category, self.category1)
        self.assertEqual(self.mess1.message_body, "Hello World!")
        self.assertEqual(self.mess1.message_title,"HoosThere Example")

    def test_post2(self):
        self.assertEqual(self.mess2.poster, self.user2)
        self.assertEqual(self.mess2.category, self.category2)
        self.assertEqual(self.mess2.message_title, "2150 Help")
        self.assertEqual(self.mess2.message_body, "Need Help with AVl Trees")

    def test_post3(self):
        self.assertNotEqual(self.mess1.poster,self.user2)
        self.assertNotEqual(self.mess2.poster, self.user1)
        self.assertNotEqual(self.mess1.category, self.category2)
        self.assertNotEqual(self.mess2.category, self.category1)


    def tearDown(self):
        self.user1.delete()
        self.profile1.delete()
        self.category1.delete()
        self.mess1.delete()
        self.user2.delete()
        self.profile2.delete()
        self.category2.delete()
        self.mess2.delete()

class viewTests(TestCase):
    def setUp(self):
        self.userTemp = User.objects.create_user(username='qp7te', email='jd@gmail.com', first_name='jack',last_name='doe')
        self.profile1 = Profile.objects.create(user_id=999, user=self.userTemp, major="CPE", minor="Math",classes_taken="CS_3240")
        self.category1 = MessageBoardCategory.objects.create(name="Miscellaneous")
        self.mess1 = MessageBoardPost.objects.create(message_title="HoosThere Example",message_body="Hello World!",poster=self.userTemp,category=self.category1)

    def test_HomeView(self):
        response = self.client.get('http://127.0.0.1:8000/',follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'studentmatching/index.html')

    def test_SearchViewBoardTitle(self):
        response = self.client.get('http://127.0.0.1:8000/board_search',{'search' : 'HoosThere_Example'},follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'studentmatching/board_search.html')

    def test_SearchViewBoardMess(self):
        response = self.client.get('http://127.0.0.1:8000/board_search',{'search' : 'Hello World!'},follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'studentmatching/board_search.html')

    def test_SearchViewName(self):
        response = self.client.get('http://127.0.0.1:8000/search',{'search' : 'jack'},follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'studentmatching/search.html')

    def test_SearchViewLastName(self):
        response = self.client.get('http://127.0.0.1:8000/search',{'search' : 'doe'},follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'studentmatching/search.html')

    def test_SearchViewUsername(self):
        response = self.client.get('http://127.0.0.1:8000/search',{'search' : 'qp7te'},follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'studentmatching/search.html')

    def test_UserSearchpostWrong(self):
        response = self.client.post('http://127.0.0.1:8000/search',{'search' : ''})
        self.assertEqual(response.status_code,301)

    def test_BoardSearchWrong(self):
        response = self.client.post('http://127.0.0.1:8000/board_search', {'search': ''})
        self.assertEqual(response.status_code, 301)

    def testSendMess(self):
        response = self.client.post('http://127.0.0.1:8000/send_message',{'content':'the message'})
        self.assertEqual(response.status_code,404)

    def test_viewMess(self):
        response = self.client.post('http://127.0.0.1:8000/direct_message', {'user': self.userTemp})
        self.assertEqual(response.status_code,404)

    def tearDown(self):
        self.userTemp.delete()
        self.profile1.delete()
        self.category1.delete()
        self.mess1.delete()

class systemTestSprint4(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='usertest')
        self.profile1 = Profile.objects.create(user_id=999, user=self.user1, major="CPE", minor="Math",classes_taken="CS_3240")
        self.category1 = MessageBoardCategory.objects.create(name="Miscellaneous")
        self.mess1 = MessageBoardPost.objects.create(message_title="HoosThere Example", message_body="Hello World!",poster=self.user1, category=self.category1)

    def test_post(self):
        self.assertEqual(self.mess1.poster,self.user1)
        self.assertEqual(self.mess1.category, self.category1)
        self.assertEqual(self.mess1.message_body, "Hello World!")
        self.assertEqual(self.mess1.message_title,"HoosThere Example")

    def test_profileEdit(self):
        form = EditProfileForm({'major': "CPE", 'minor': "EE", 'classes_taken': "OS"})
        self.assertTrue(form.has_changed())
        self.assertTrue(form.is_valid())

    def test_UserForm(self):
        form = EditUserForm({'email':'johndoe@gmail.com','first_name':'John','last_name':'Doe'})
        self.assertTrue(form.has_changed())
        self.assertTrue(form.is_valid())

    def test_profileInfo(self):
        self.assertEqual(self.user1.username,"usertest")
        self.assertEqual(self.profile1.major,"CPE")
        self.assertEqual(self.profile1.minor,"Math")
        self.assertEqual(self.profile1.classes_taken,"CS_3240")

    def tearDown(self):
        self.user1.delete()
        self.profile1.delete()
        self.category1.delete()
        self.mess1.delete()


class SystemTestSprint5(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='qp7te', email='jd@gmail.com', first_name='jack',last_name='doe')
        self.user2 = User.objects.create_user(username='bg4ey', email='q4sdd@gmail.com', first_name='jane',last_name='does')
        self.profile1 = Profile.objects.create(user_id=999,user=self.user1, major="EE", minor="English",classes_taken="CS_3240, LIT_3069")
        self.profile2 = Profile.objects.create(user_id=99, user=self.user2, major="CS", minor="Spanish",classes_taken="CS_2150, SPN_12")
        self.message=Message.objects.create(sender=self.user1,receiver=self.user2,viewer=self.user2,content='hi can i get help')
        self.message2 = Message.objects.create(sender=self.user2, receiver=self.user1, viewer=self.user1,content='sure when?')
        self.category1 = MessageBoardCategory.objects.create(name="Miscellaneous")
        self.mess1 = MessageBoardPost.objects.create(message_title="HoosThere Example",message_body="Hello World!",poster=self.user1,category=self.category1)

    def test_Messcheck(self):
        self.assertEqual(self.message.sender,self.user1)
        self.assertEqual(self.message.receiver,self.user2)
        self.assertEqual(self.message.content,'hi can i get help')

    def test_Messcheck2(self):
        self.assertEqual(self.message2.sender,self.user2)
        self.assertEqual(self.message2.receiver,self.user1)
        self.assertEqual(self.message2.content,'sure when?')

    def test_SearchViewBoardMess(self):
        response = self.client.get('http://127.0.0.1:8000/board_search',{'search' : 'Hello World!'},follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'studentmatching/board_search.html')

    def test_SearchViewBoardTitle(self):
        response = self.client.get('http://127.0.0.1:8000/board_search',{'search' : 'HoosThere_Example'},follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'studentmatching/board_search.html')

    def test_SearchViewName(self):
        response = self.client.get('http://127.0.0.1:8000/search',{'search' : 'jack'},follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'studentmatching/search.html')


    def test_SearchViewLastName(self):
        response = self.client.get('http://127.0.0.1:8000/search',{'search' : 'doe'},follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'studentmatching/search.html')

    def test_SearchViewUsername(self):
        response = self.client.get('http://127.0.0.1:8000/search',{'search' : 'qp7te'},follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'studentmatching/search.html')

    def testSendMess(self):
        response = self.client.post('http://127.0.0.1:8000/send_message', {'content': 'the message'})
        self.assertEqual(response.status_code, 404)

    def test_viewMess(self):
        response = self.client.post('http://127.0.0.1:8000/direct_message', {'user': self.user1})
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()
        self.profile1.delete()
        self.profile2.delete()
        self.message.delete()
        self.message2.delete()
        self.category1.delete()
        self.mess1.delete()
