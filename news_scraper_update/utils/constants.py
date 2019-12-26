import os

"""
Scraper Project Root Directory:
"""
ROOT_DIR = '/'.join((os.path.dirname(os.path.abspath(__file__))).split('/')[:-1])


AD_BLOCK_SOURCES = ["9to5google.com",
                    "9to5toys.com",
                    "Bleacher Report",
                    "Boardgamegeek.com",
                    "Boardingarea.com",
                    "Boardingarea.com",
                    "Checkpoint.com",
                    "Collider.com",
                    "commingsoon.net",
                    "Commonsensewithmoney.com",
                    "Deadline.com",
                    "Dealcatcher.com",
                    "Dealnews.com",
                    "Disneyfashionista.com",
                    "Elitedaily.com",
                    "extratv.com",
                    "Hotnewhiphop.com",
                    "Hotukdeals.com",
                    "Insideflyer.com",
                    "Internetmarketinginc.com",
                    "Ipadinsight.com",
                    "Jeffsetter.com",
                    "Justjared.com",
                    "Kicksonfire.com",
                    "Kinja.com",
                    "Livingrichwithcoupons.com",
                    "Loyaltylobby.com",
                    "Millionmilesecrets.com",
                    "Moneysavingmom.com",
                    "Onemileatatime.com",
                    "Ozbargain.com.au",
                    "Qooah.com",
                    "Queenbeecoupons.com",
                    "Redflagdeals.com",
                    "Road.cc",
                    "Secretflying.com",
                    "Slickdeals.net",
                    "Smartcanucks.ca",
                    "Smartinsights.com",
                    "Socialmediaexaminer.com",
                    "Sonyalpharumors.com",
                    "Southernsavers.com",
                    "sweettoothsweetlife.com",
                    "Thepointsguy.com",
                    "Trustedreviews.com",
                    "Yourmileagemayvary.net"]


"""
GCP Cloud MySQL DB Connection:
"""
# switch between production and development mode by commenting out

# development sql server public ip address: 34.74.131.247
# GCP_MYSQL_HOST = "34.74.131.247"
# production sql server public ip address: 35.225.155.245
GCP_MYSQL_HOST = "35.225.155.245"
GCP_MYSQL_USER = "scraper"
GCP_MYSQL_PASS = "unibitScraper2019"
GCP_MYSQL_DB = "unibitDB"
GCP_MYSQL_CHARSET = "utf8"
GCP_MYSQL_PORT = 3306


# SQLAlchemy connection config
MYSQL_CONNECTION_STRING = "{drivername}://{user}:{passwd}@{host}:{port}/{db_name}?charset={charset}".format(
    drivername="mysql+pymysql",
    user=GCP_MYSQL_USER,
    passwd=GCP_MYSQL_PASS,
    host=GCP_MYSQL_HOST,
    port=GCP_MYSQL_PORT,
    db_name=GCP_MYSQL_DB,
    charset=GCP_MYSQL_CHARSET
)


"""
GCP Cloud MySQL Tables:
"""
# stock
COMPANY_INFORMATION = "company_information"
COMPANY_INFORMATION_WTD = "company_information_wtd"

# crypto
CRYPTO_INFORMATION = 'crypto_information'

# World Exchanges Trading Hours
WORLD_EXCHANGES_TRADING_HOURS = "world_exchanges_trading_hours"

"""
GCP Cloud MySQL Table Names by API:
"""
# 1. Company Financials API
COMPANY_FINANCIALS_ANNUAL = "financials_annual"
COMPANY_FINANCIALS_QUARTER = "financials_quarter"
# 2. Company Profile API

# 3. Company Financial Summary API
COMPANY_FINANCIAL_SUMMARY = "company_profile"
# 4. Ownership Structure API
OWNERSHIP_STRUCTURE_MAJORITY = "majority_holder"
OWNERSHIP_STRUCTURE_TOP_INST = "top_institutional_holder"
OWNERSHIP_STRUCTURE_TOP_MUTUAL = "top_mutual_fund_holder"
# 5. Insider Transaction API
INSIDER_TRANSACTION = "insider_trading"
# 6. CIK Number API
CIK_NUMBER = "cik_table"
# 7. SEC Filing Link API
SEC_FILING_LINK = "sec"
# 8. Latest Stock News API

# 9. Stock News Analysis API

# 10. Historical Stock Price API
HISTORICAL_STOCK_PRICE = "historical_stockprice"
# 11. Historical Crypto Price API
HISTORICAL_CRYPTO_PRICE = "historical_cryptoprice"

#12. Company Information Profile
COMPANY_INFORMATION_PROFILE = "company_information_profile"

#13. Corporate Action table names
CORPORATE_ACTION_SPLITS = 'corporate_action_splits'
CORPORATE_ACTION_DIVIDENDS = 'corporate_action_dividends'

"""
Multithreading Config:
"""
NUM_OF_THREADS = 20

"""
Historical Stock Price Constants:
"""
YAHOO_HISTORICAL_STOCK_PRICE_DOWNLOAD_LINK = "https://query1.finance.yahoo.com/v7/finance/download/{ticker}?" \
                                             "period1={start_time}&period2={end_time}&interval=1d&events=history&crumb={user_crumb}"

YAHOO_HISTORICAL_STOCK_PRICE_START_DATE = "2001-01-01"

YAHOO_HISTORICAL_STOCK_PRICE_REQUEST_HEADERS = {
    # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}


"""
Insider Trading Constants:
"""
INSIDER_TRADING_POST_URL = "http://35.245.8.88:8888/api/company/add/insider_trading"

"""
Crypto Constants:
"""
# up2date input start date
# CRYPTO_HISTORICAL_UP2DATE_START_DATE = date(2000, 1, 1)
CRYPTO_HISTORICAL_UP2DATE_START_DATE  = '2000-01-01'
