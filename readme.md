# Cryptocurrency trading with twitter sentiment analysis and machine learning

Simple implementation of a cryptocurrency trading algorithm with twitter sentiment analysis and machine learning predictions.

It is for made for litecoin prediction but it can be easily edited to other cryptocurrencies. 

## Getting Started

### Clone repository

    ~ $ git clone 
    ~ $ cd cryptocurrency-trading-with-sentiment-analysis

### Project requirements 

It is strongly advised you work in a virtual environment.\
First step is to create one and install all necessary project requirements.
       
    ~ $ virtualenv env --python=python3
    ~ $ source env/bin/activate
    ~ $ pip install -r requirements.txt

## Execution

    ~ $ cd scripts
    ~ $ python main.py [--date_init some-date]
    
Optionaly, you can set the backtesting initial date as an argument. If not, a dates is set by default.

For example:

    ~ $ python main.py --date_init 2019-04-01


