'''
If you run this, the file will be filled with the text 
of all his Great Movie reviews.
It goes to the site, pulls the review text out of the HTML code,
then saves it to a .txt, for all like 361 films.


#Prerequisites:
#the great_html.txt file, which
#contains the html code of all great movies
#on the site
'''

from bs4 import BeautifulSoup
import requests
from csv import writer


def gen_gm_list():
    '''
    Copy pasted from previous file, minor adjustments made to make it all in one formula.
    Specifically, put global variables that are function specific into the function.
    '''
    url = "https://www.rogerebert.com"
    great_movies = []
    i = 0
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
        i += 1
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
        great_movies.append([i, movie_title, movie_link])
            #great_movies is now a list containing movie title and link to movie review.
    return great_movies


def catch_hteml_all(url, file_name):
    '''
    Should accept a URL, gets the HTML, then writes review text to a txt.

    Includes a hilarious and witty pun in the function name.
    '''
    html_code = requests.get(url)
        #grabs the HTML code for the URL
    soup = BeautifulSoup(html_code.text, "html.parser")
        #note how the first argument is ".txt".
        #This puts the requested HTML code into a string, where we can pull from.

    review_soup = soup.find_all(class_ = "page-content--block_editor-content js--reframe")
    #Compiles the HTML code containing the reviews in segments. 

    review_text = ""

    for x in review_soup:
        review_text += x.text
        #review_text now contains the raw text of the review

    with open(f'{file_name}.txt', 'w', encoding = 'utf-8', newline='') as file:
        file_writer = writer(file)
        file.write(review_text)


gm_urls = gen_gm_list()

baddies = [
    "https://www.rogerebert.com/reviews/great-movie-cleo-from-5-to-7-1962", 
    "https://www.rogerebert.com/reviews/great-movie-cache-2005"
    ]
    #these film names would cause errors in the file name.
    #Gotta do those myself

forbidden_chars = '*"/\\<>:|?'
    #these can't be used in file names
    #\\ needs to be done so python recognizes it as a character

for movie in gm_urls:
    title = movie[1]
    #grabbed the title in a variable
    for x in forbidden_chars:
        if x in title:
            print(title)
            title = title.replace(x,"")
        #deletes any characters that can't be used in file names from moie title

    url = movie[2]
    if url == baddies[0]:
        title = "Cleo_from_5_to_7"
    elif url == baddies[1]:
        title = "Cache"

    for char in title:
        if char == " ":
            title = title.replace(" ", "_")
    print(title)
    # file_name = #i want to swap spaces with an underscore
    catch_hteml_all(url, title)