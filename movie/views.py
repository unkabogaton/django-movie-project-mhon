from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Transaction, TicketPurchase, Customer, Schedule
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import SignupForm 

@login_required
def dashboard(request):
    # Fetch the top 5 highest-rated movies (You can adjust this based on your needs)
    top_movies = Movie.objects.order_by('-ratings')[:5]
    
    # Fetch the most recent transactions (again, adjust based on your needs)
    recent_transactions = Transaction.objects.order_by('-createdAt')[:5]
    
    # For dashboard statistics, you can also add total movies, total transactions, etc.
    total_movies = Movie.objects.count()
    total_transactions = Transaction.objects.count()

    # Pass data to the template
    return render(request, 'dashboard.html', {
        'top_movies': top_movies,
        'recent_transactions': recent_transactions,
        'total_movies': total_movies,
        'total_transactions': total_transactions,
    })
    
@login_required
def transactions_list(request):
    search = request.GET.get("search", "")
    status = request.GET.get("status", "")
    purchase_method = request.GET.get("purchase_method", "")

    transactions = Transaction.objects.select_related('customer').all()

    if search:
        transactions = transactions.filter(
            Q(id__icontains=search) | Q(customer__email__icontains=search)
        )
    if status:
        transactions = transactions.filter(status=status)
    if purchase_method:
        transactions = transactions.filter(purchase_method=purchase_method)

    transactions = transactions.order_by("-createdAt")

    return render(request, "transactions.html", {
        "transactions": transactions,
    })

def transaction_detail_modal(request, transaction_id):
    txn = get_object_or_404(Transaction.objects.select_related('customer', 'movie'), id=transaction_id)
    return render(request, "partials/transaction_detail.html", {
        "txn": txn
    })

@csrf_exempt
def update_transaction_status(request):
    if request.method == "POST":
        txn_id = request.POST.get("transaction_id")
        new_status = request.POST.get("new_status")

        txn = get_object_or_404(Transaction, id=txn_id)
        movie = get_object_or_404(Movie, id=txn.movie_id)

        if txn.status == "Pending" and new_status == "Paid":
            txn.status = "Paid"
            txn.save()

            # Generate tickets
            TicketPurchase.objects.bulk_create([
                TicketPurchase(transaction=txn, ticket_status="Valid", movie=movie)
                for _ in range(txn.quantity)
            ])

        return redirect("transactions")

@login_required    
def ticket_purchases(request):
    query = request.GET.get("q", "")
    status_filter = request.GET.get("status", "")

    ticket_list = TicketPurchase.objects.select_related("movie", "transaction")

    if query:
        ticket_list = ticket_list.filter(
            Q(id__icontains=query) |
            Q(transaction__id__icontains=query) |
            Q(movie__title__icontains=query)
        )

    if status_filter in ['Valid', 'Redeemed', 'Expired']:
        ticket_list = ticket_list.filter(ticket_status=status_filter)

    ticket_list = ticket_list.order_by("-updatedAt")

    return render(request, "ticket_purchases.html", {
        "tickets": ticket_list,
        "query": query,
        "status_filter": status_filter,
    })

def redeem_ticket(request, ticket_id):
    ticket = get_object_or_404(TicketPurchase, id=ticket_id)
    ticket.ticket_status = 'Redeemed'
    ticket.save()
    return redirect('ticket_purchases')

@login_required
def customers_list(request):
    search_query = request.GET.get('q', '')

    customers = Customer.objects.all()
    if search_query:
        customers = customers.filter(
            Q(name__icontains=search_query) | Q(email__icontains=search_query)
        )

    customers = customers.order_by('-createdAt')

    return render(request, 'customers.html', {'customers': customers, 'search_query': search_query})

@login_required
def showrooms(request):
    schedules = Schedule.objects.select_related('movie').order_by('showroom_number')
    movies = Movie.objects.all()
    return render(request, 'showrooms.html', {'schedules': schedules, 'movies': movies})

@csrf_exempt
def update_schedule(request, schedule_id):
    if request.method == "POST":
        schedule = get_object_or_404(Schedule, id=schedule_id)
        schedule.movie_id = request.POST.get("movie_id")
        schedule.showtimes = request.POST.get("showtimes")
        schedule.intermission = request.POST.get("intermission")
        schedule.price = request.POST.get("price")
        schedule.capacity = request.POST.get("capacity")
        schedule.save()
        return redirect('showrooms')

@login_required    
def movie_list(request):
    search_query = request.GET.get('search', '')
    view_type = request.GET.get('view', 'list')

    movies = Movie.objects.filter(title__icontains=search_query)

    context = {
        'movies': movies,
        'search_query': search_query,
        'view_type': view_type,
    }

    return render(request, 'movies.html', context)

def movie_detail(request, id):
    movie = get_object_or_404(Movie, id=id)
    return render(request, 'partials/movie_detail.html', {'movie': movie})

@csrf_exempt
def add_movie(request):
    data = request.POST
    try:
        Movie.objects.create(
            title=data.get('title'),
            year=int(data.get('year')),
            awards=data.get('awards'),
            description=data.get('description'),
            actors=data.get('actors'),
            ratings=data.get('ratings'),
            link_to_pictures=data.get('link_to_pictures'),
            duration=data.get('duration'),
            producer=data.get('producer'),
        )
        return redirect('movies')
    except Exception as e:
        return HttpResponseBadRequest(str(e))

@csrf_exempt
def edit_movie(request):
    movie_id = request.POST.get('movie_id')
    movie = get_object_or_404(Movie, id=movie_id)

    try:
        movie.title = request.POST.get('title')
        movie.year = int(request.POST.get('year'))
        movie.awards = request.POST.get('awards')
        movie.description = request.POST.get('description')
        movie.actors = request.POST.get('actors')
        movie.ratings = request.POST.get('ratings')
        movie.link_to_pictures = request.POST.get('link_to_pictures')
        movie.duration = request.POST.get('duration')
        movie.producer = request.POST.get('producer')
        movie.save()
        return redirect('movies')
    except Exception as e:
        return HttpResponseBadRequest(str(e))

def delete_movie(request, id):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, id=id)
        movie.delete()
        return redirect('movies')
    
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Log the user in immediately after sign-up
            return redirect('dashboard')  
    else:
        form = SignupForm()  # Empty form for GET request

    return render(request, 'signup.html', {'form': form})