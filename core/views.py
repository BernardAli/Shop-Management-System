import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect

from core.forms import StockSearchForm, StockUpdateForm, StockCreateForm, ReorderLevelForm, ReceiveForm, IssueForm, \
    CashSearchForm, IssueCashForm, ReceiveCashForm
from core.models import Stock, Cash


# Create your views here.


def home_page(request):
    return render(request, "home.html")


@login_required
def list_item(request):
    header = 'List of Items'
    form = StockSearchForm(request.POST or None)

    queryset = Stock.objects.all()
    context = {
        "header": header,
        "queryset": queryset,
        "form": form,
    }
    if request.method == 'POST':
        category = form['category'].value()
        queryset = Stock.objects.filter(  # category__icontains=form['category'].value(),
            item_name__icontains=form['item_name'].value()
        )

        if category != '':
            queryset = queryset.filter(category_id=category)

        if form['export_to_CSV'].value():
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
            instance = queryset
            for stock in instance:
                writer.writerow([stock.category, stock.item_name, stock.quantity])
            return response
        context = {
            "form": form,
            "header": header,
            "queryset": queryset,
        }
    return render(request, "list_item.html", context)


@login_required
def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Added')
        return redirect('/list_items')
    context = {
        "form": form,
        "title": "Add Item",
    }
    return render(request, "add_item.html", context)


@login_required
def update_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Updated')
            return redirect('/list_items')

    context = {
        'form': form
    }
    return render(request, 'add_item.html', context)


@login_required
def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Successfully Deleted')
        return redirect('/list_items')
    return render(request, 'delete_item.html')


@login_required
def stock_detail(request, pk):
    queryset = Stock.objects.get(id=pk)
    context = {
        "title": queryset.item_name,
        "queryset": queryset,
    }
    return render(request, "stock_detail.html", context)


@login_required
def reorder_level(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Reorder level for " + str(instance.item_name) + " is updated to " + str(
            instance.reorder_level))

        return redirect("/list_items")
    context = {
        "instance": queryset,
        "form": form,
    }
    return render(request, "add_item.html", context)


@login_required
def issue_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        if instance.sale_quantity > instance.quantity:
            messages.success(request, "Stock Not Enough")
        else:
            instance.purchased_quantity = 0
            instance.total_sale_price = instance.unit_sale_price * instance.sale_quantity
            instance.quantity -= instance.sale_quantity
            instance.sale_by = str(request.user)
            messages.success(request, "Issued SUCCESSFULLY. " + str(instance.quantity) + " " + str(
                instance.item_name) + "s now left in Store")
            instance.save()

        return redirect('/stock_detail/' + str(instance.id))
    # return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": 'Issue ' + str(queryset.item_name),
        "queryset": queryset,
        "form": form,
        "username": 'Issue By: ' + str(request.user),
    }
    return render(request, "add_item.html", context)


@login_required
def receive_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.sale_quantity = 0
        instance.total_purchase_price = instance.unit_purchase_price * instance.purchased_quantity
        instance.quantity += instance.purchased_quantity
        instance.purchased_by = str(request.user)
        instance.save()
        messages.success(request, "Received SUCCESSFULLY. " + str(instance.quantity) + " " + str(
            instance.item_name) + "s now in Store")

        return redirect('/stock_detail/' + str(instance.id))
    # return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": 'Reaceive ' + str(queryset.item_name),
        "instance": queryset,
        "form": form,
        "username": 'Receive By: ' + str(request.user),
    }
    return render(request, "add_item.html", context)


@login_required
def cash_item(request):
    header = 'Cash Book'
    # form = CashSearchForm(request.POST or None)

    queryset = Cash.objects.order_by('created_on').last()
    context = {
        "header": header,
        "queryset": queryset,
    }
    # if request.method == 'POST':
    #     queryset = Cash.objects.filter(  # category__icontains=form['category'].value(),
    #         detail__icontains=form['detail'].value()
    #     )
    #
    #     if form['export_to_CSV'].value():
    #         response = HttpResponse(content_type='text/csv')
    #         response['Content-Disposition'] = 'attachment; filename="CashBook.csv"'
    #         writer = csv.writer(response)
    #         writer.writerow(['DATE', 'RECIPIENT', 'DETAIL', 'AMOUNT CR', 'AMOUNT DB', 'BALANCE'])
    #         instance = queryset
    #         for cash in instance:
    #             writer.writerow([cash.created_on, cash.recipient, cash.detail, cash.amount_in,
    #                              cash.amount_out, cash.balance])
    #         return response
    #     context = {
    #         "form": form,
    #         "header": header,
    #         "queryset": queryset,
    #     }
    return render(request, "cash_item.html", context)


@login_required
def issue_cash(request, pk):
    queryset = Cash.objects.get(id=pk)
    form = IssueCashForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        if instance.amount_out > instance.balance:
            messages.success(request, "Not Enough Cash")
        else:
            instance.amount_in = 0
            instance.balance -= instance.amount_out
            instance.issue_by = str(request.user)
            messages.success(request, "Cash Paid Successfully")
            instance.save()

        return redirect('cash_item')
    # return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": 'Issue ' + str(queryset.issue_by),
        "queryset": queryset,
        "form": form,
        "username": 'Issue By: ' + str(request.user),
    }
    return render(request, "add_cash.html", context)


@login_required
def receive_cash(request, pk):
    queryset = Cash.objects.get(id=pk)
    form = ReceiveCashForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.amount_out = 0
        instance.balance += instance.amount_in
        instance.issue_by = str(request.user)
        messages.success(request, "Cash Received Successfully")
        instance.save()

        return redirect('cash_item')
    # return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": 'Issue ' + str(queryset.issue_by),
        "queryset": queryset,
        "form": form,
        "username": 'Issue By: ' + str(request.user),
    }
    return render(request, "add_cash.html", context)