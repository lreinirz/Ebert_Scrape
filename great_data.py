'''I want the year.
And to get the year, I need to get back the list of moies
and compile which 


And at some point, I need to reconcile how there's
a list on IMDB that lists 364 films while I only
have 361.
'''

from bs4 import BeautifulSoup

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

#pulled straight from great_csv_data_collection.py

gm_urls = gen_gm_list()

for x in gm_urls:
    url = x[2]
    if "great-movie" not in url:
        print(x[2])

print("\n\n\n")

for x in gm_urls:
    url = x[2]
    year = ""

    if "Monsieur-Hire" in url:
        year = 1989
        x.append(str(year))
        #For some reason, the formatting on this URL
        #is unique, not including Great Movie, the year,
        #or the other cases below. Fortunately, it's just
        #this one. I looked up the year manually.

    if "great-movie" in url:
        #if "great-movie" is in the URL, the URL ends 
        #with the year the film was released

        year = str(x[2][-4:])
        x.append(year)
        #and I go ahead and add that to the film info

    elif "great-movie" not in url:
        #there's a few inconsistent formattings

        try:
            year = int(x[2][-4:])
            #if url doesn't end with four digits,
            #this throws an error, and we move to "except"

            #but if it does, 
            x.append(str(year))

        except:
            #it looks like some URLs end with "-1"
            #easy enough. since we're here, those are
            #all that's left. 
            year = url[-6:-2]
            x.append(str(year))
            print(x[3])

for x in gm_urls:
    print(x[3])