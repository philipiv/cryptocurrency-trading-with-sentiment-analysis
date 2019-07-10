import argparse

from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from fredapi import Fred
from sklearn.model_selection import train_test_split

from util import *


# set constants and initial configuration

parser = argparse.ArgumentParser(
    description='Cryptocurrency trading algorithm with twitter sentiment analysis and machine learning predictions.')
parser.add_argument('--date_init', nargs='?', help='backtesting initial date', default='2019-04-01')

args = parser.parse_args()

date_init = args.date_init

frequency = 'd'

date_init_plus_one = str(pd.datetime.strptime(date_init, "%Y-%m-%d") + pd.Timedelta(days=1)).split(' ')[0]

config = get_config('../config.json')

fred_api_key = config['fred']['api-key']
tweepy_keys = config['tweepy']

fred = Fred(api_key=fred_api_key)

# get signals

sp_index_ = fred.get_series('SP500', observation_start=date_init, frequency=frequency)
bitcoin_price_ = fred.get_series('CBBTCUSD', observation_start=date_init, frequency=frequency)
ethereum_price_ = fred.get_series('CBETHUSD', observation_start=date_init, frequency=frequency)
litecoin_price_ = fred.get_series('CBLTCUSD', observation_start=date_init_plus_one, frequency=frequency)

# dates from date_init to yesterday
# this array is used as a common index to all signals

index_norm = pd.date_range(date_init, pd.datetime.today() - pd.Timedelta(days=1))

# takes signals to common index

sp_index = get_signal_norm_dates(sp_index_, index_norm)[:-1]
bitcoin_price = get_signal_norm_dates(bitcoin_price_, index_norm)[:-1]
ethereum_price = get_signal_norm_dates(ethereum_price_, index_norm)[:-1]
litecoin_price = get_signal_norm_dates(litecoin_price_, index_norm)[1:]

# calculates sentiment

sentiment = get_sentiment(index_norm, "#litecoin", tweepy_keys)

# set data and labels tests

X = []
y = []

size = np.shape(index_norm)[0] - 1

for j in range(size):
    X.append([sp_index[j], bitcoin_price[j], ethereum_price[j], sentiment[j]])
    y.append(litecoin_price[j])

# splits data and labels into train and test set

test_size = 0.20
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=0)

# Create linear regression object
regr = linear_model.LinearRegression()

# Train the model using the training sets
regr.fit(X_train, y_train)

# Make predictions using the testing set
y_pred = regr.predict(X_test)

# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean squared error
print("Mean squared error: %.2f"
      % mean_squared_error(y_test, y_pred))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % r2_score(y_test, y_pred))

