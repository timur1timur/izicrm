from django.shortcuts import render, redirect
from .models import MarkupCommon, MarkupCustomerCategory, MarkupMaterialCategory, MarkupWorkCategory, MarkupSetting
from .forms import MarkupCustomerCategoryForm, MarkupMaterialCategoryForm, MarkupWorkCategoryForm


def MarkupList(request):
    common = MarkupCommon.objects.all()
    customers = MarkupCustomerCategory.objects.all()
    materials = MarkupMaterialCategory.objects.all()
    works = MarkupWorkCategory.objects.all()

    context = {
        'common': common,
        'customers': customers,
        'materials': materials,
        'works': works
    }
    return render(request, 'markup/markups.html', context=context)

def MarkupCommonEdit(request, id):
    if request.method == 'GET':
        item = MarkupCommon.objects.get(pk=id)
        markup = item.markup

        form = MarkupCustomerCategoryForm({'markup': markup})
        return render(request, 'markup/markup_common_edit.html',
                      context={'form': form})

    if request.method == 'POST':
        form = MarkupCustomerCategoryForm(request.POST)
        markup = request.POST.get("markup", None)

        if markup != None:
            item = MarkupCommon.objects.get(pk=id)
            item.markup = markup
            item.save(update_fields=['markup'])
            return redirect('markup:markup_list')
        return render(request, 'markup/markup_common_edit', context={'form': form})


def MarkupCustomerCategoryEdit(request, id):
    if request.method == 'GET':
        item = MarkupCustomerCategory.objects.get(pk=id)
        markup = item.markup
        source_t = item.source_t
        form = MarkupCustomerCategoryForm({'markup': markup, 'source_t': source_t})
        return render(request, 'markup/markup_edit.html',
                      context={'form': form, 'source_t': item.get_source_t_display()})

    if request.method == 'POST':
        form = MarkupCustomerCategoryForm(request.POST)
        markup = request.POST.get("markup", None)
        source_t = request.POST.get("source_t", None)
        if markup != None and source_t != None:
            item = MarkupCustomerCategory.objects.get(pk=id)
            item.markup = markup
            item.source_t = source_t
            item.save(update_fields=['markup', 'source_t'])
            return redirect('markup:markup_list')
        return render(request, 'markup/markup_edit', context={'form': form})


def MarkupMaterialCategoryEdit(request, id):
    if request.method == 'GET':
        item = MarkupMaterialCategory.objects.get(pk=id)
        markup = item.markup
        source_t = item.source_t
        form = MarkupMaterialCategoryForm({'markup': markup, 'source_t': source_t})
        return render(request, 'markup/markup_edit.html',
                      context={'form': form, 'source_t': item.get_source_t_display()})

    if request.method == 'POST':
        form = MarkupMaterialCategoryForm(request.POST)
        markup = request.POST.get("markup", None)
        source_t = request.POST.get("source_t", None)
        if markup != None and source_t != None:
            item = MarkupMaterialCategory.objects.get(pk=id)
            item.markup = markup
            item.source_t = source_t
            item.save(update_fields=['markup', 'source_t'])
            return redirect('markup:markup_list')
        return render(request, 'markup/markup_edit', context={'form': form})


def MarkupWorkCategoryEdit(request, id):
    if request.method == 'GET':
        item = MarkupWorkCategory.objects.get(pk=id)
        markup = item.markup
        source_t = item.source_t
        form = MarkupWorkCategoryForm({'markup': markup, 'source_t': source_t})
        return render(request, 'markup/markup_edit.html',
                      context={'form': form, 'source_t': item.get_source_t_display()})

    if request.method == 'POST':
        form = MarkupWorkCategoryForm(request.POST)
        markup = request.POST.get("markup", None)
        source_t = request.POST.get("source_t", None)
        if markup != None and source_t != None:
            item = MarkupWorkCategory.objects.get(pk=id)
            item.markup = markup
            item.source_t = source_t
            item.save(update_fields=['markup', 'source_t'])
            return redirect('markup:markup_list')
        return render(request, 'markup/markup_edit', context={'form': form})

def MarkupViewChange(request, id):
    settings = MarkupSetting.objects.get(name='markup_view')
    if int(id) == 1:
        settings.value = 1
        settings.save(update_fields=['value'])
    elif int(id) == 0:
        settings.value = 0
        settings.save(update_fields=['value'])
    return redirect(request.META.get('HTTP_REFERER'))