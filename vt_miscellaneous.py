#############################################
# VirusTotal Public API v2.0 miscellaneous 
# functions.
# 
# Author: @michael_yip
# Email:  jiachongzhi@gmail.com
# Date: 08/03/2015
#############################################
from os import getcwd, listdir
from os.path import isfile, join, getmtime
from datetime import datetime, timedelta
import pickle
import md5

# API KEY
API_KEY = '<INSERT YOUR API KEY>'

# Cache directory
CACHE_DIR = 'cache'
CACHE_PATH = join(getcwd(), CACHE_DIR)

def is_modified_today(filename):
	''' Check if cache was modified today. '''
	modfied_time = getmtime(join(CACHE_PATH, filename))
	return (datetime.today() - datetime.fromtimestamp(modfied_time)) < timedelta(days = 1)

def load_cache(term):
	''' Check if a term has already been searched.'''
	term = md5.new(term).hexdigest()
	# List files in cache directory
	try:
		cache_files = [ f for f in listdir(CACHE_PATH) if isfile(join(CACHE_PATH, f)) ]
		if term in cache_files:
			# If cache exists, if it was made today:
			if is_modified_today(term):
				with open(join(CACHE_PATH,term), 'rb') as cache_file:
					return pickle.load(cache_file)
	except Exception as e:
		print e
	return None

def dump_cache(term, json):
	''' Cache VT result for the given term. '''
	term = md5.new(term).hexdigest()
	try:
		with open(join(CACHE_PATH,term), 'wb') as cache_file:
				pickle.dump(json, cache_file)
				return True
	except Exception as e:
		print e
	return False