# amazon-deals

A webscraping script that uses Python and the libraries BeautifulSoup and Requests-HTML to find products on Amazon. 

## Usage
To run the script:

```python3 amazon_deals.py [-p[r] | -r | -n] req1 req2```

The options ```-p[r] | -r | -n``` are how the results are sorted. They correspond to Prices low to high [high to low], Ratings, Number of reviews respectively. 

The inputs ```req1``` and ```req2``` are the amount of results displayed and the search item respectively.
