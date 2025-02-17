from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note
from notes.forms import NoteForm


User = get_user_model()


class TestContetnt(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='note-slug',
            author=cls.author,
        )

    def test_notes_list_for_different_users(self):
        client_notes = (
            (self.author, True),
            (self.reader, False),
        )
        for user, note_in_list in client_notes:
            with self.subTest(note_in_list=note_in_list, user=user):
                self.client.force_login(user)
                url = reverse('notes:list')
                response = self.client.get(url)
                object_list = response.context['object_list']
                self.assertEqual((self.note in object_list), note_in_list)

    def test_pages_contains_form(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', self.note.slug),
        )
        self.client.force_login(self.author)
        for name, arg in urls:
            with self.subTest(arg=arg, name=name):
                url = reverse(name, args=(arg,) if arg else ())
                response = self.client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
