import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from requests.compat import quote_plus
from . import models

# Base URL to capture the searches dynamically.
BASE_CRAIGSLIST_URL = 'https://charlotte.craigslist.org/search/ata?query={}'
# Base URL to capture the images of each search
BASE_IMAGE_URL='https://images.craigslist.org/{}_300x300.jpg'
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
    # Test to check if the soup object is working correctly.  Pull the first item in the object
    # post_title = post_listings[0].find(class_='result-title hdrlnk').text
    # post_url = post_listings[0].find('a').get('href')
    # post_price = post_listings[0].find(class_='result-price').text

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title hdrlnk').text
        post_url = post.find('a').get('href')
        post_price = post.find(class_='result-price').text
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            print(post_image_id)
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        final_postings.append((post_title,post_url,post_price,post_image_url))

    stuff_for_front_end = {
        'search': search,
        'final_postings':final_postings,
    }
    return render(request, 'my_app/new_search.html',stuff_for_front_end)