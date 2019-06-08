from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.db.models import Avg, Count, Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import UserRegisterForm
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def homepage(request):
    template = 'review/homepage.html'
    categories = Category.objects.all()
    cat_with_restaurant = []
    for category in categories:
        rests = Restaurant.objects.filter(category=category.id)
        rest_with_count = []
        for rest in rests:
            review = Review.objects.filter(restaurant=rest.id)
            reviews_count = review.count()
            if (reviews_count != 0):
                reviews_avg_rating = review.aggregate(Sum('rate'))['rate__sum']/reviews_count
            else:
                reviews_avg_rating = 'NIL'
            rest_with_count.append({
                'restaurant': rest,
                'reviews_count':reviews_count,
                'reviews_avg_rating':reviews_avg_rating,
            })
        cat_with_restaurant.append({
            'category': category,
            'restaurants': rest_with_count,
        })

    context_data = {
        'categories':cat_with_restaurant,
    }
    return render(request, template, context_data)


def register(request):
    template = 'review/register.html'
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            msg = 'Create '+username+' account successfully'
            messages.success(request, msg)

            return redirect('login')
        else:
            messages.error(request, 'wrong')
    else:
        form = UserRegisterForm()
        

    context_data = {
        'form': form,
    }

    return render(request, template, context_data)


def restaurant_content(request, cat_id, rest_id):
    template = 'review/restaurant_content.html'
    r = Restaurant.objects.get(id=rest_id)
    reviews = Review.objects.filter(restaurant=rest_id)
    
    review_plus_likes_count=[]
    for review in reviews:
        review_plus_likes_count.append({
            'review': review,
            'likes_count_for_review': LikeForReview.objects.filter(review=review.id).count(),
            'is_review_liked_by_user': LikeForReview.objects.filter(review=review.id,user=request.user).exists(),
            'comments_on_review': Comment.objects.filter(review=review.id),
        })
    
    if request.method == 'POST':
        if request.POST['action'] == 'like-review':
            reviewID = request.POST.get('reviewID')
            if LikeForReview.objects.filter(review=reviewID,user=request.user):
                LikeForReview.objects.filter(review=reviewID,user=request.user).delete()
                return HttpResponseRedirect(request.path_info)
            else:
                LikeForReview.objects.create(
                    review=Review.objects.get(id=reviewID),
                    user=request.user,
                )
                return HttpResponseRedirect(request.path_info)
        if request.POST['action'] == 'submit-review':
            Review.objects.create(
                user=request.user,
                description = request.POST.get('description'),
                restaurant = r,
                rate = request.POST.get('rating'),
            )
            return HttpResponseRedirect(request.path_info)
    
    context_data = {
        'restaurant': {
            'rest': r,
            'reviews': review_plus_likes_count,
        }
    }
    return render(request, template, context_data)


def restaurant_list(request, cat_id):
    template = 'review/restaurant_list.html'
    restaurants = Restaurant.objects.filter(category=cat_id).prefetch_related('review_set').annotate(count=Count('review')).annotate(avg_rating=Avg('review__rate'))
    
    reviews = Review.objects.select_related('restaurant').filter(restaurant__category=cat_id).values('restaurant')\
    .annotate(count=Count('restaurant')).annotate(avg_rating=Avg('rate'))

    count = reviews.count()
    avg_rating = (reviews.aggregate(Avg('rate')))['rate__avg']

    context_data = {
        'restaurants': restaurants,
        'reviews': reviews,
        'count': count,
        'avg_rating': avg_rating,
    }
    return render(request, template, context_data)

def search_result(request):
    template = 'review/search_result.html'  

    query = request.GET.get('q')
    
    result = []
    
    try:
        r = Restaurant.objects.get(id__iexact=query)
        result.append(r)
    except Restaurant.DoesNotExist:
        result = Restaurant.objects.all()
        
    context = {
        'result': result,
    }
    
    return render(request, template, context)