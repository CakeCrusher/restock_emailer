# Restock Emailer
## set up
1. clone the repo ```git clone https://github.com/CakeCrusher/restock_emailer.git```
2. cd into the repo ```cd restock_emailer```
3. ```pip install scrapy```
4. reccomended to get a free proxy API from https://www.scraperapi.com/ (otherwise use the alternative code under [get_url](restock_checker/spiders/stock_status.py))
5. fill in [API_KEY and sites_data](restock_checker/spiders/stock_status.py)
6. fill in [sites_data](restock_checker/spiders/stock_status.py) many examples provided play around with them!
7. activate [less secure app access](https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqblg5VktZWmM2OFNqTE9hWTFWOTY0Y2NhcXV1d3xBQ3Jtc0tuLUsybTd3cGxXNjZsaGNVMzUzS19ReXBVQV9zT0xiemJneDF2S0FaN2QycE5OVHBaaE81QnFYMjRZSGdKTXhaZ01oR1RXbjNkZk9lNmZXWUJTRGY0Mm1GblhwUVlzQ3BaV29FNEtvNzRCSy15SVJZbw&q=https%3A%2F%2Fmyaccount.google.com%2Flesssecureapps) to the email which will deliver emails
8. fill in [EMAIL_ADDRESS and EMAIL_PASSWORD](send_email.py)
9. fill in [START_TIME, ITERATE_SECONDS, and START_TIME_PRECISION](scrape_trigger.py)
10. start the script with ```python scrape_trigger.py``` watch it go! (data on the results can be accessed in [availability.jsonlines](availability.jsonlines))
