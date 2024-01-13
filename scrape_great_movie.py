from bs4 import BeautifulSoup
import requests
import csv
from random import choice
from time import sleep
from selenium import webdriver

'''
1. I went to https://www.rogerebert.com/great-movies
    and scrolled down until all Great Movies loaded
    onto the page.
2. I clicked "Inspect Element", found the element that contained
    all Great Movies
        <div class="js--reviews">
3. I copied the HTML and pasted it into a .txt, which I called "great_html.txt"

'''
url = "https://www.rogerebert.com"
entry_num = 0
great_movies = []

great_html = open("great_html.txt")
    #The .txt file containing the needed HTML is now open and actie.

soup = BeautifulSoup(great_html, "html.parser")
    #The HTML code can now be parsed by BeautifulSoup in this variable "soup"
    #A quick glance at the HTML code shows that the movie title and the link to the movie review can be found in:
    #<h5 class="review-stack--title"> 

great_html.close()
    #We now have the HTML code saved in a variable, so the file does not need to be opened anymore. 

great_soup = soup.find_all(class_ = "review-stack--title")
    #compiles a list of all relevant elements for each Great Movie. 
    #This includes movie title and a link to the Great Movie review.

for movie in great_soup:
    movie_title = movie.get_text()[1:-2]
        #DONE, we now have the film title.
        #Also removes extraneous line breaks.
    movie_href = movie.find("a").attrs['href']
        #The end result of this step is that the variable "href", when combined with "www.rogerebert.com", 
        #is a resolvable url to the Great Movie review.
        #Here's how:
        #movie.find("a") locates the element within "movie" that is an anchor element, denoted by "a". 
        #e.g.: "<a href="/reviews/great-movie-the-ballad-of-narayama-1958">Ballad of Narayama</a>"
        #.attrs['href'] then gets the text associated with the attribute href. Badda bing.
        #This can be broken into two for visual readability, like
        #dummy = movie.find("a")
        #href = dummy.attrs['href']
        #where dummy pulls the anchor element a, and href pulls the name associated. 
    movie_link = url + movie_href
        #this is a resolvable url containing the Great Movie review.
    great_movies.append([movie_title, movie_link])
        #great_movies is now a list containing movie title and link to movie review.

with open('Great_Movies_URL.csv', 'w', encoding = "utf8") as file:
        #creates a csv file, ready for data. Final argument avoids formatting errors.
    csv_writer = csv.writer(file)
        #creates an object that enables writing data to the created cs file
    csv_writer.writerow(['Entry #', 'Title', 'URL'])
        #With this step, the csv writer object has created the headers of three columns.
    for each in great_movies:
            #Goes through the Great Movies list one at a time. 
        entry_num += 1
            #Numbers each entry.
        csv_writer.writerow([entry_num, each[0], each[1]])
            #Adds a row with "Entry Number", "Movie Title", "Movie Review URL"


#Entry number 7, Cleo from 5 to 7, and
#Entry number 48, Cache
#have an e with an accent which is not unicode compatible. I have fixed these manually.