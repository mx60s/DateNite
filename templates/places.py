# Python program to get a set of 
# places according to your search 
# query using Google Places API 
# Written by referencing Geeksforgeeks website guide

# importing required modules 
import requests, json 

# Places API Key 
api_key = 'AIzaSyBFNSAxslWL0c9xPc223PJGJFCu2hIZlGU'

# url variable store url 
places_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

# The text string on which to search 
query = input('Search query: ') 

# return response object 
response = requests.get(places_url + 'query=' + query + '&key=' + api_key) 

# json method of response object convert 
# json format data into python format data 
convert_py = response.json() 

# store the value of result key  
store = convert_py['results'] 

# keep looping upto lenghth of store 
for i in range(len(store)): 
	
	# Print value corresponding to the 
	# 'name' key at the ith index of y 
	print(store[i]['name']) 
