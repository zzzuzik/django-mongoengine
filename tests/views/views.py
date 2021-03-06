#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import, division, print_function

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator

from django_mongoengine import views

from .forms import AuthorForm
from .models import Artist, Author, Book, Page


class CustomTemplateView(views.TemplateView):
    template_name = 'views/about.html'

    def get_context_data(self, **kwargs):
        return {'params': kwargs, 'key': 'value'}


class ObjectDetail(views.DetailView):
    template_name = 'views/detail.html'

    def get_object(self):
        return {'foo': 'bar'}


class ArtistDetail(views.DetailView):
    queryset = Artist.objects.all()


class AuthorDetail(views.DetailView):
    queryset = Author.objects.all()


class PageDetail(views.DetailView):
    queryset = Page.objects.all()
    template_name_field = 'template'


class DictList(views.ListView):
    """A ListView that doesn't use a model."""
    queryset = [
        {'first': 'John',
         'last': 'Lennon'}, {'first': 'Yoko',
                             'last': 'Ono'}
    ]
    template_name = 'views/list.html'


class ArtistList(views.ListView):
    template_name = 'views/list.html'
    queryset = Artist.objects.all()


class AuthorList(views.ListView):
    queryset = Author.objects.all().order_by('name')


class CustomPaginator(Paginator):
    def __init__(self,
                 queryset,
                 page_size,
                 orphans=0,
                 allow_empty_first_page=True):
        super(CustomPaginator, self).__init__(
            queryset,
            page_size,
            orphans=2,
            allow_empty_first_page=allow_empty_first_page)


class AuthorListCustomPaginator(AuthorList):
    paginate_by = 5

    def get_paginator(self,
                      queryset,
                      page_size,
                      orphans=0,
                      allow_empty_first_page=True):
        return super(AuthorListCustomPaginator, self).get_paginator(
            queryset,
            page_size,
            orphans=2,
            allow_empty_first_page=allow_empty_first_page)


class ArtistCreate(views.CreateView):
    document = Artist


class NaiveAuthorCreate(views.CreateView):
    queryset = Author.objects.all()


class AuthorCreate(views.CreateView):
    document = Author
    success_url = '/list/authors/'


class SpecializedAuthorCreate(views.CreateView):
    document = Author
    form_class = AuthorForm
    template_name = 'views/form.html'
    context_object_name = 'thingy'

    def get_success_url(self):
        return reverse('author_detail', args=[self.object.id, ])


class AuthorCreateRestricted(AuthorCreate):
    post = method_decorator(login_required)(AuthorCreate.post)


class ArtistUpdate(views.UpdateView):
    document = Artist


class NaiveAuthorUpdate(views.UpdateView):
    queryset = Author.objects.all()


class AuthorUpdate(views.UpdateView):
    document = Author
    success_url = '/list/authors/'


class OneAuthorUpdate(views.UpdateView):
    success_url = '/list/authors/'

    def get_object(self):
        return Author.objects.get(pk='1')


class SpecializedAuthorUpdate(views.UpdateView):
    document = Author
    form_class = AuthorForm
    template_name = 'views/form.html'
    context_object_name = 'thingy'

    def get_success_url(self):
        return reverse('author_detail', args=[self.object.id])


class NaiveAuthorDelete(views.DeleteView):
    queryset = Author.objects.all()


class AuthorDelete(views.DeleteView):
    document = Author
    success_url = '/list/authors/'


class SpecializedAuthorDelete(views.DeleteView):
    queryset = Author.objects.all()
    template_name = 'views/confirm_delete.html'
    context_object_name = 'thingy'

    def get_success_url(self):
        return reverse('authors_list')


class AuthorGetQuerySetFormView(views.edit.DocumentFormMixin):
    def get_queryset(self):
        return Author.objects.all()
