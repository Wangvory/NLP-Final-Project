# STEP 1: install python3.7 and python3.7-dev
$ sudo apt-get install python3.7-dev
# if return apt-get: command not found error:
* First, you need to install the Xcode command-line tool by using the following command:
$ xcode-select �install
* After the Xcode tool installation, now type/copy the following command to install Homebrew on macOS:
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
* The installation will ask for Return (Enter) key and password for confirmation.
$ brew install python3

# STEP 2: install ML packages
$ pip3 install spacy / or pip install spacy
$ pip3 install pycld2
$ pip3 install pyicu
# if pip cannot install pycld2 and pyicu directly, try: 
$ CFLAGS=-stdlib=libc++ pip install pycld2
$ brew install icu4c
$ ls /usr/local/Cellar/icu4c/
$ export ICU_VERSION=64
$ export PYICU_INCLUDES=/usr/local/Cellar/icu4c/64.2/include
$ export PYICU_LFLAGS=-L/usr/local/Cellar/icu4c/64.2/lib
$ export PATH="/usr/local/opt/icu4c/bin:$PATH"
$ pip install pyicu 

# STEP 3: install spacy packages
$ YOUR_INTERPRETER_PATH  -m spacy download en(You can find the path by opening the terminal and typing �which python3� in Mac and �where python� in Windows)
# i.e.
$ C:\Users\Li Xiang\Anaconda3\python -m spacy download en
 
# STEP 4: install nltk packages
>import nltk
>nltk.download('vader_lexicon')
>nltk.download('punkt')
 
# STEP 5: install polyglot packages
$ polyglot download embeddings2.en
$ polyglot download ner2.en
 
#STEP 6:  run the scraper
Change your directory to the root direct of �stock_news_analyzer�(The same directory with the file �scrapy.cfg�) and type:
$ scrapy crawl nlp_news

Notification: it may take some time to scrape all the news
