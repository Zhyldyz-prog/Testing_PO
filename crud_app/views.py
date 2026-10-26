from django.shortcuts import render, redirect, get_object_or_404
from .models import Item
from .forms import ItemForm


# 1. CREATE (Создание)
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'crud_app/item_form.html', {'form': form, 'title': 'Создать элемент'})


# 2. READ LIST (Просмотр списка)
def item_list(request):
    items = Item.objects.all().order_by('-id')
    return render(request, 'crud_app/item_list.html', {'items': items})


# 3. READ DETAIL (Просмотр одного элемента)
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'crud_app/item_detail.html', {'item': item})


# 4. UPDATE (Редактирование)
def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_detail', pk=item.pk)
    else:
        form = ItemForm(instance=item)
    return render(request, 'crud_app/item_form.html', {'form': form, 'title': 'Редактировать элемент'})


# 5. DELETE (Удаление)
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'crud_app/item_confirm_delete.html', {'item': item})