from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.base import *

from .form import *
from .models import *


class MainPageView(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_template_names(self):
        template_name = super(MainPageView, self).get_template_names()
        search = self.request.GET.get('q')
        filter = self.request.GET.get('filter')
        if search:
            template_name = 'search.html'
        elif filter:
            template_name = 'new.html'
        return template_name

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('q')
        filter = self.request.GET.get('filter')
        context['categories'] = Category.objects.all()
        if search:
            context['products'] = Product.objects.filter(Q(title__icontains=search)|Q(description__icontains=search))
        else:
            context['products'] = Product.objects.all()
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category-detail.html'
    context_object_name = 'category'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.slug = kwargs.get('slug', None)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(category_id=self.slug)
        return context


class ProductDetailView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = CommentsForm()
        return render(request, 'product-detail.html', locals())

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = CommentsForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            comment = Comments(text=text)
            comment.user = request.user
            comment.product = product
            comment.save()
            return redirect(product.get_absolute_url())




class IsAdminCheckMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser)


class ProductCreateView(IsAdminCheckMixin, View):
    def get(self, request):
        form = CreateProductForm()
        formset = ImagesFormSet(queryset=Image.objects.none())
        return render(request, 'create.html', locals())

    def post(self, request):
        form = CreateProductForm(request.POST)
        formset = ImagesFormSet(request.POST, request.FILES, queryset=Image.objects.none())
        if form.is_valid() and formset.is_valid():
            product = form.save()
            for form in formset.cleaned_data:
                image = form.get('image')
                if image is not None:
                    pic = Image(product=product, image=image)
                    pic.save()
            return redirect(product.get_absolute_url())
        print(form.errors, formset.errors)


class ProductEditView(IsAdminCheckMixin, View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = CreateProductForm(instance=product)
        formset = ImagesFormSet(queryset=product.images.all())
        return render(request, 'edit.html', locals())

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = CreateProductForm(instance=product, data=request.POST)
        formset = ImagesFormSet(request.POST,
                                request.FILES,
                                request.FILES,
                                queryset=product.images.all())

        if form.is_valid() and formset.is_valid():
            product = form.save()
            for form in formset.cleaned_data:
                image = form.get('image')
                if image is not None:
                    if not Image.objects.filter(product=product, image=image).exists():
                        pic = Image(product=product, image=image)
                        pic.save()
            for form in formset.deleted_forms:
                image = form.cleaned_data.get('id')
                image.delete()
            return redirect(product.get_absolute_url())
        print(form.errors, formset.errors)


class ProductDeleteView(IsAdminCheckMixin, DeleteView):
    model = Product
    template_name = 'delete.html'
    success_url = reverse_lazy('home')
