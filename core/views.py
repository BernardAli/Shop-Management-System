import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, HttpResponse, redirect

from core.forms import StockSearchForm, StockUpdateForm, StockCreateForm, ReorderLevelForm, ReceiveForm, IssueForm, \
    CashSearchForm, IssueCashForm, ReceiveCashForm, StockHistorySearchForm, ImpriestLevelForm, CashHistorySearchForm
from core.models import Stock, Cash, StockHistory, CashHistory


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
            # instance.purchased_quantity = 0
            instance.total_sale_price = instance.unit_sale_price * instance.sale_quantity
            instance.quantity -= instance.sale_quantity
            instance.total_sale_price = instance.sale_quantity * instance.unit_sale_price
            instance.sale_by = str(request.user)
            messages.success(request, "Issued SUCCESSFULLY. " + str(instance.quantity) + " " + str(
                instance.item_name) + "s now left in Store")
            instance.save()
            issue_history = StockHistory(
                last_updated=instance.last_updated,
                category_id=instance.category_id,
                item_name=instance.item_name,
                quantity=instance.quantity,
                sale_to=instance.sale_to,
                sale_by=instance.sale_by,
                sale_quantity=instance.sale_quantity,
                unit_sale_price=instance.unit_sale_price,
                total_sale_price=instance.total_sale_price,
            )
            issue_history.save()

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
        # instance.sale_quantity = 0
        instance.total_purchase_price = instance.unit_purchase_price * instance.purchased_quantity
        instance.quantity += instance.purchased_quantity
        instance.total_purchase_price = instance.purchased_quantity * instance.unit_purchase_price
        instance.purchased_by = str(request.user)
        instance.save()
        receive_history = StockHistory(
            last_updated=instance.last_updated,
            category_id=instance.category_id,
            item_name=instance.item_name,
            quantity=instance.quantity,
            purchased_quantity=instance.purchased_quantity,
            purchased_by=instance.purchased_by,
            purchased_from=instance.purchased_from,
            unit_purchase_price=instance.unit_purchase_price,
            total_purchase_price=instance.total_purchase_price,
        )
        receive_history.save()
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
def list_history(request):
    header = 'HISTORY DATA'
    queryset = StockHistory.objects.all()
    paginator = Paginator(queryset, 15)
    page_number = request.GET.get('page')
    queryset = paginator.get_page(page_number)
    form = StockHistorySearchForm(request.POST or None)
    context = {
        "header": header,
        "queryset": queryset,
        "form": form,
    }
    if request.method == 'POST':
        category = form['category'].value()
        # queryset = StockHistory.objects.filter(
        #     item_name__icontains=form['item_name'].value()
        # )

        queryset = StockHistory.objects.filter(
            item_name__icontains=form['item_name'].value(),
            last_updated__range=[
                form['start_date'].value(),
                form['end_date'].value()
            ]
        )

        if category != '':
            queryset = queryset.filter(category_id=category)

        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="Stock History.csv"'
            writer = csv.writer(response)
            writer.writerow(
                ['CATEGORY',
                 'ITEM NAME',
                 'QUANTITY',
                 'ISSUE QUANTITY',
                 'RECEIVE QUANTITY',
                 'RECEIVE BY',
                 'ISSUE BY',
                 'TOTAL SALE PRICE',
                 'TOTAL PURCHASE PRICE',
                 'LAST UPDATED'])
            instance = queryset
            for stock in instance:
                writer.writerow(
                    [stock.category,
                     stock.item_name,
                     stock.quantity,
                     stock.sale_quantity,
                     stock.purchased_quantity,
                     stock.purchased_by,
                     stock.sale_by,
                     stock.total_sale_price,
                     stock.total_purchase_price,
                     stock.last_updated])
            return response

        paginator = Paginator(queryset, 15)
        page_number = request.GET.get('page')
        queryset = paginator.get_page(page_number)

        context = {
            "form": form,
            "header": header,
            "queryset": queryset,
        }
    return render(request, "list_history.html", context)


@login_required
def cash_item(request):

    queryset = Cash.objects.all()
    context = {
        "queryset": queryset,
    }

    return render(request, "cash_item.html", context)


@login_required
def cash_detail(request, pk):
    queryset = Cash.objects.get(id=pk)
    context = {
        "queryset": queryset,
    }
    return render(request, "cash_detail.html", context)


@login_required
def impriest_level(request, pk):
    queryset = Cash.objects.get(id=pk)
    form = ImpriestLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Reorder level for " + str(instance.category) + " is updated to " + str(
            instance.impriest_level))

        return redirect("cash_items")
    context = {
        "instance": queryset,
        "form": form,
    }
    return render(request, "add_item.html", context)


@login_required
def issue_cash(request, pk):
    queryset = Cash.objects.get(id=pk)
    form = IssueCashForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        if instance.amount_out > instance.balance:
            messages.success(request, "Not Enough Cash")
        else:
            # instance.purchased_quantity = 0
            instance.balance -= instance.amount_out
            instance.issue_by = str(request.user)
            messages.success(request, "Issued SUCCESSFULLY. " + str(instance.balance) + " " + str(
                instance.category) + " balance left")
            instance.save()
            cash_issue_history = CashHistory(
                last_updated=instance.last_updated,
                category=instance.category,
                detail=instance.detail,
                recipient=instance.recipient,
                issue_by=instance.issue_by,
                amount_out=instance.amount_out,
                created_on=instance.created_on,
                balance=instance.balance,
            )
            cash_issue_history.save()

        return redirect('/cash_detail/' + str(instance.id))
    # return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "queryset": queryset,
        "form": form,
        "username": 'Issue By: ' + str(request.user),
    }
    return render(request, "add_item.html", context)


@login_required
def receive_cash(request, pk):
    queryset = Cash.objects.get(id=pk)
    form = ReceiveCashForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        # instance.purchased_quantity = 0
        instance.balance += instance.amount_in
        instance.recipient = str(request.user)
        messages.success(request, "Received SUCCESSFULLY. " + str(instance.balance) + " " + str(
            instance.category) + " balance left")
        instance.save()
        cash_receive_history = CashHistory(
            last_updated=instance.last_updated,
            category=instance.category,
            recipient=instance.recipient,
            detail=instance.detail,
            issue_by=instance.issue_by,
            amount_in=instance.amount_in,
            created_on=instance.created_on,
            balance=instance.balance,
        )
        cash_receive_history.save()

        return redirect('/cash_detail/' + str(instance.id))
    # return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "queryset": queryset,
        "form": form,
        "username": 'Received By: ' + str(request.user),
    }
    return render(request, "add_item.html", context)


@login_required
def cash_history(request):
    header = 'CASH HISTORY'
    queryset = CashHistory.objects.all()
    paginator = Paginator(queryset, 15)
    page_number = request.GET.get('page')
    queryset = paginator.get_page(page_number)
    form = CashHistorySearchForm(request.POST or None)
    context = {
        "header": header,
        "queryset": queryset,
        "form": form,
    }
    if request.method == 'POST':

        queryset = CashHistory.objects.filter(
            category__icontains=form['category'].value(),
            last_updated__range=[
                form['start_date'].value(),
                form['end_date'].value()
            ]
        )


        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="Stock History.csv"'
            writer = csv.writer(response)
            writer.writerow(
                ['CATEGORY',
                 'RECIPIENT',
                 'DETAIL',
                 'RECEIVED AMOUNT',
                 'PAID AMOUNT',
                 'BALANCE',
                 'ISSUED BY',
                 'LAST UPDATED'])
            instance = queryset
            for stock in instance:
                writer.writerow(
                    [stock.category,
                     stock.recipient,
                     stock.detail,
                     stock.amount_in,
                     stock.amount_out,
                     stock.balance,
                     stock.issue_by,
                     stock.last_updated])
            return response

        paginator = Paginator(queryset, 15)
        page_number = request.GET.get('page')
        queryset = paginator.get_page(page_number)

        context = {
            "form": form,
            "header": header,
            "queryset": queryset,
        }
    return render(request, "cash_history.html", context)