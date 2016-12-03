# coding: utf-8
import  time
import requests
from bs4 import BeautifulSoup
import pickle

def parse_api_response(file_name, field='url'):

    with open(file_name) as f:
        data = pickle.load(f)
    return {f.id: f.url for f in data}

def createmap(one):
        dic = {
        'review_id': one["data-review-id"],
        'user_id': one['data-signup-object'].split(':')[1],
        'rating': float(one.find_all("div", class_="rating-large")[0]['title'].split()[0]),
        'date': one.find_all("span", class_="rating-qualifier")[0].getText().split()[0],
        'text': one.find_all("div", class_="review-content")[0].p.getText()
        }
        return dic
    
def parse_page(html):
    soup = BeautifulSoup(html,"html.parser")

    all_review = soup.find_all("div", class_="review")
    nextpage = soup.find_all("a", class_="next")
    if nextpage:
        nextpage = nextpage[0]["href"]
    else:
        nextpage = None
    reviews = map(createmap, all_review[1:])
    return reviews, nextpage

def extract_reviews(url):
    all_reviews = []
    nextpage = url
    while nextpage:
        res = requests.get(nextpage)
        html = res.content
        
        reviews, nextpage = parse_page(html)
        all_reviews += reviews
    return all_reviews

def extract_all_reviews(urls):
    reviews = {}
    print " start...."
    for k, v in urls.items():
        reviews[k]= extract_reviews(v)
    print " finished"
    with open('reviews.data', 'wb') as f:
        pickle.dump(reviews, f)

def extract_price(url):
    res = requests.get(url)
    html = res.content
    soup = BeautifulSoup(html,"html.parser")
    try:
        price = soup.find_all("span", class_="price-range")[0].getText()
    except:
        print url
        price = ''
    return price

def extract_all_prices(urls):
    res_prices = {k: extract_price(v) for k, v in urls.items()}
    with open('price.data', 'wb') as f:
        pickle.dump(res_prices, f)
