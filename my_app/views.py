import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from requests.compat import quote_plus
from . import models

# Base URL to capture the searches dynamically.
BASE_CRAIGSLIST_URL = 'https://charlotte.craigslist.org/search/ata?query={}'
# Create your views here.
def home(request):
    return render(request,'base.html')

def new_search(request):
    # POST request to get the contents of the search
    search = request.POST.get('search')
    # Create a new object that will capture all of the searches
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    print(final_url)
    response = requests.get(final_url)
    data = response.text
    # Create a Beautiful Soup object of the html
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li',{'class':'result-row'})
    post_title = post_listings[0].find(class_='result-title hdrlnk').text
    post_url = post_listings[0].find('a').get('href')
    post_price = post_listings[0].find(class_='result-price').text
    #
    print(post_title)
    print(post_url)
    print(post_price)

    stuff_for_front_end = {
        'search': search,
    }
    return render(request, 'my_app/new_search.html',stuff_for_front_end)