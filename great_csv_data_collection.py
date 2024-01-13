from bs4 import BeautifulSoup
import requests
import csv
from random import choice
from time import sleep
from csv import writer
import wikipedia as wiki

'''
Next step:
Grab the review from each Great Movie link. 
Process:
1. Open link through Python
2. Scrape HTML
3. Compile only the words into a .txt document for that movie. 

'''


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

def scrape_reviews(url):
    '''
    Hopefully returns a list
    First entry contains list of actors
    Second entry contains the entire text of the review.
    '''

    response = requests.get(url)
    #'response' is now a 'response' type object filled with HTML
    #you can do all sorts of stuff with it

    html_string = response.text

    soup = BeautifulSoup(html_string, "html.parser")
    #The HTML code can now be parsed by BeautifulSoup in this variable "soup"
    #A quick glance at the HTML code shows that the movie title and the link to the movie review can be found in:
    #<h5 class="review-stack--title"> 


    review_soup = soup.find_all(class_ = "page-content--block_editor-content js--reframe")
    #Compiles the HTML code containing the reviews in segments. 

    review_text = ""

    for x in review_soup:
        review_text += x.text

    #review_text now contains the raw text of the review
    #It is split into paragraphs. I would like to remove the paragraphs.

    acting_soup = []
        #When reviews mention an actor or actress, there is a hyperlink associated with them.
        #This makes them easy to sort out for further analysis.
    for each in review_soup:
        acting_soup.append(each.find_all("a"))
        #Goes through EACH PARAGRAPH one at a time and compiles a list of all links tied to people names

    actoring_html = []
        #Gets together the HTML code associated with each actor
    for x in acting_soup:
        #for x paragraph in acting_soup:
        for each in x:
            #for each link found within the paragraph,
            try:
                if "cast-and-crew" in str(each.attrs['href']):
                    #if the link associated with the name has "cast-and-crew"
                    #in it, they are a human being. 
                    actoring_html.append(each)

            except:
                pass
                #I added this because in the review for Chimes at Midnight, 
                #Roger Ebert linked to an external site. 
                #This is a link, an href, that didn't match the above critera
                #and required a reset. 
        #It's compiled as HTML now.

    acting_list = [x.text for x in actoring_html]
        #makes the HTML code into pure text

    sleep(1)
        #to be polite

    return acting_list#, review_text]

def url_year(l):
    '''
    The variable gm_info is a list of lists.
    Each list has the following:
    ["Entry number, e.g. 1", "Title of Film", "Link to Film Review"]
    I want to add the year to each of these. 
    The year is in the URL for every single film but one. 
    I'll add that one in manually.
    '''
    #the input will be:
    #all the information I have for one film. 
    #Like the above example list.

    x = l
    #sets the input to a variable to play with

    url = x[2]
    year = ""

    if "Monsieur-Hire" in url:
        year = 1989
        x.append(str(year))
        return x
        #For some reason, the formatting on this URL
        #is unique, not including Great Movie, the year,
        #or the other cases below. Fortunately, it's just
        #this one. I looked up the year manually.
    elif "great-movie-bride-of-frankenstein" in url:
        year = 1935
        x.append(str(year))
        return x
        #just kidding, there were two uniqely formatted urls. 

    elif "ivan-the-terrible-parts-i-and-ii" in url:
        year = 1944
        x.append(str(year))
        return x
        #whatever.        

    elif "diva-2008" in url:
        x.append('1981')
        return x
    elif "vengeance-is-mine" in url:
        x.append('1979')
        return x


    if "great-movie" in url:
        #if "great-movie" is in the URL, the URL ends 
        #with the year the film was released

        year = str(x[2][-4:])
        x.append(year)
        return x
        #and I go ahead and add that to the film info

    elif "great-movie" not in url:
        #there's a few inconsistent formattings

        try:
            year = int(x[2][-4:])
            #if url doesn't end with four digits,
            #this throws an error, and we move to "except"

            #but if it does, 
            x.append(str(year))
            return x

        except:
            #it looks like some URLs end with "-1"
            #easy enough. since we're here, those are
            #all that's left. 
            year = url[-6:-2]
            x.append(str(year))
            return x



gm_info = gen_gm_list()
    #gets the list of Great Movies plus urls in a variable
    #i like this variable a lot

for movie in gm_info:
    movie = url_year(movie)
    #Adds the year mentioned in the review URL to the movie info


#each film now has:
#Entry #, Movie Title, URL, Year

#I'm going to add "Mentioned Cast and Crew" next.
#In the reiews, Ebert mentions directors, actors and actresses, 
#and occasionally mentions comparable people in the industry.
#I'm gonna add 'em to a list.'

#All that's needed is for the result of scrape_re\/iews() for each link
#to be appeneded to the result
#that will add mentioned actors to the gm_info



# #Entry #, Movie Title, URL, Year, Cast and Crew
# #I am ready for a preliminary CSV.



def write_prelim_csv(database):
    with open('gm_info.csv', 'w', encoding = 'utf-8', newline='') as file:
        headers = ['Entry #', 'Movie Title', 'Year', 'Cast and Crew', 'URL']
        csv_writer = writer(file)
        csv_writer.writerow(headers)
        for x in database:
            url = x[2]
            cast_and_crew = scrape_reviews(url)
            x.append(cast_and_crew)
            csv_writer.writerow([x[0], x[1], x[3], x[4], x[2]])

#write_prelim_csv(gm_info)
    #not really needed once run the first time


# with open('great_urls.txt', 'w', encoding = 'utf-8', newline = '') as file:
#     file_writer = writer(file)
#     for x in gm_info:
#         file.write(x[2] + "\n")
#   we now have a txt file with all great movie urls

#next up, access the database, and see if we can pull the wiki html code 

def wiki_prelim(film, year):
    '''
    Gets me a description of the wiki page and some basic info.
    But I want the HMTL and URL.
    Gonna do a different thing to get the URL based off a search.
    '''

    language_code = 'en'
    search_query = film + ' ' + year
    number_of_results = 1


    base_url = 'https://api.wikimedia.org/core/v1/wikipedia/'
    endpoint = '/search/page'
    url = base_url + language_code + endpoint

    headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJhZDg2NjU0ZThjN2RlZmM0YmExZDNhZjI0ZjM2NDIyYiIsImp0aSI6ImZiM2Q3NzVlY2FmOTgyOGJiN2EwNTM0ODIxMTdjNTFmM2VmMDBjYjg3YzA5ZGNjYTdhN2U2M2Y5YmYwYzlhNWE0MWNiZTdlZjVhZjMxMDg3IiwiaWF0IjoxNzA0NTE3NjU1LjMxNjk5OCwibmJmIjoxNzA0NTE3NjU1LjMxNzAwMSwiZXhwIjozMzI2MTQyNjQ1NS4zMTU4NTMsInN1YiI6IjQ3NDkzNTMyIiwiaXNzIjoiaHR0cHM6Ly9tZXRhLndpa2ltZWRpYS5vcmciLCJyYXRlbGltaXQiOnsicmVxdWVzdHNfcGVyX3VuaXQiOjUwMDAsInVuaXQiOiJIT1VSIn0sInNjb3BlcyI6WyJiYXNpYyJdfQ.f0AclqiiflydwcQyZpVLBqcmoWp12r-4CE64LKoIYdyBvYapmoAG0OuU-38wuPIVBEDFeYUOw6eCMFjGauNE7PLRlKUOxN6U0qcGA4cX9Mz4VzxeD62g8olxdpRlkGFaogeZQ1aVEenwiljxuDAv1K12uDN6fj_RWhErQrkCrpwtEphs7DGmbAYzC9jych32_Vh0zn-',
        'User-Agent': 'great_cvs_data_collection (https://api.wikimedia.org/wiki/User:Lreinirz)'
    }
    parameters = {'q': search_query, 'limit': number_of_results}
    response = requests.get(url, params = parameters)

    html_string = response.text
    soup = BeautifulSoup(html_string, "html.parser")

    return soup


def wiki_scrape(film, year):
    '''
    End result:
    We will get the BeautifulSoup object from an inputted film.
    In other words,
    we'll get the HTML for the wikipedia page for a searched for film. 
    '''

    language_code = 'en'
    search_query = film + ' ' + year
    number_of_results = 1

    s = requests.Session()

    url = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "opensearch",
        "search": search_query,
        "limit": "5"
    }

    film_url = None


    r = s.get(url=url, params=params)
    print(r.text)
    data = r.json()
    if len(data) > 1:
        print(data)
        for x in data[1]:
            print("bing")
            if "film" in x:
                print("yup")
                print(x)
                ind = data[1].index(x)
                film_url = data[-1][ind]
    else:
        print("bong")
        film_url = data[-1][0]

    return film_url
    response = requests.get(film_url)

    html_string = response.text
    soup = BeautifulSoup(html_string, "html.parser")

    return soup


def wiki_url_desparation(film, year):
    #returned format:
    #0: The searched for term
    #1: Full list of results
    #2: Comes up blank
    #3: Bunch of URLS 

    #catches odd cases
    if film == "Ivan the Terrible, Parts I & II":
        return "https://en.wikipedia.org/wiki/Ivan_the_Terrible_(1944_film)"
    elif film == 'Blade Runner: The Final Cut':
        return "https://en.wikipedia.org/wiki/Blade_Runner"
    elif film == "The River (Le Fleuve)":
        return "https://en.wikipedia.org/wiki/The_River_(1951_film)"
    elif film == "Sunrise":
        return 'https://en.wikipedia.org/wiki/Sunrise:_A_Song_of_Two_Humans'
    elif film == "M":
        return 'https://en.wikipedia.org/wiki/M_(1931_film)'

    elif film == "Red Beard":
        return "https://en.wikipedia.org/wiki/Red_Beard"
        #it returned a 2002 film called "red bear"
        #there has to be a better way.

    elif film == "The Decalouge":
        return "https://en.wikipedia.org/wiki/The_Decalogue_(film_series)"
 
    elif film == "The Hustler":
        return "https://en.wikipedia.org/wiki/The_Hustler"
    elif film == "Rififi":
        return "https://en.wikipedia.org/wiki/Rififi"

    # elif film == "Star Wars":
    #     return "https://en.wikipedia.org/wiki/Star_Wars_(film)"    
    # elif film == "Jaws":
    #     return "https://en.wikipedia.org/wiki/Jaws_(film)"
    # elif film == "After Hours":
    #     return "https://en.wikipedia.org/wiki/After_Hours_(film)"
    #     #this one was neat.
    #     #it originally returned this link:
    #     #https://en.wikipedia.org/wiki/The_After_Hours_(The_Twilight_Zone,_1985)
    #     #which, yup, was the same year. ya got me good. 



    year_sub = str(int(year) - 1)
        #Departures was released in 2008.
        #Ebert listed it in 2009.
        #Hopefully this won't be a problem
    year_dub_sub = str(int(year) - 2)
    year_blub = str(int(year) + 1)


    s = requests.Session()
        #Initiates API interface

    base_url = "https://en.wikipedia.org/w/api.php"
        #accesses the Wikipedia API

    parameters_ = {
        #Required for Wikipedia's OpenSearch
        "action": "opensearch",
        "namespace": "0",
        "search": f"{film}",
        "limit": "100",
        #thank you, films like "Laura" and "Shane".
        #actually, most of all, thank you "sunrise".
        #it used to be 50.
        #it used to be 30.
        #it used to be 5.
        "format": "json"
    }

    r = s.get(url=base_url, params=parameters_)
        #The API Interface session begins, with the base URL and parameters
    data = r.json()
        #We get back search results as JSON.

    found_film_URLs = [data[3][0]]
        #throws first url into a list for later use.
    if len(data[1]) > 1:
        #if the search yields more than one result:

        for result in data[3]:
            #go through each result and see,

            if f"{year}_film" in result:
                #1. If the link has the film year specified by Ebert in it,
                #E.G. https://en.wikipedia.org/wiki/Harakiri_(1962_film)
                #then that's our film
                #every time.
                #We're done with this movie and can move to the next.
                
                return result

            elif "film" in result:
                #we add it to a list to do further work on.

                #2. If we have multiple results and only one of them is a film,
                #E.G. https://en.wikipedia.org/wiki/Mulholland_Drive_(film)
                #then that's our film
                found_film_URLs.append(result)




    else:
        #only one result means we got a unique one first try.
        return data[3][0]



    for x in found_film_URLs:
        if "(film)" in x:
            #if a film does not specify a year
            #then it is the only film with that name.
            #that's ours.
            #badlands solved.
            return x
        elif f"{year}" in x:
            #if out of all films,
            #this one has the correct year in the URL,
            #then wikipedia has differentiated
            #and that is ours.
            return x

        elif f"{year_sub}" in x:
            #Like with Departures, Ebert got the year wrong,
            #somehow. I don't know. International release
            #schedules are strange.
            #This corrects for that. 
            return x
        elif f"{year_dub_sub}" in x:
            #Like with The Terrorist.
            #I don't know maybe it was held back for release.
            #Whatever.
            return x
        elif f"{year_blub}" in x:
            return x
            #fuck my life

    for x in found_film_URLs:
        #if the year of our film is not found in any of them
        #e.g. 
        #https://en.wikipedia.org/wiki/Nosferatu
        #https://en.wikipedia.org/wiki/Nosferatu_(2024_film)
        #then the original first result is ours.
        if f"{year}" in x:
            return x
        elif f"{year_sub}" in x:
            return x
    
    return found_film_URLs[0]




def if_this_works_we_are_in_business(gm_info):
    #need [1] and [3]
    i = -1
    for x in range(len(gm_info)):
        i += 1
        print(i)
        #testing if this idea is crazy enough to work.
        f = gm_info[x][1]
            #grabs film title
        y = gm_info[x][3]
            #grabs film year
        innit = wiki_url_desparation(f, y)
        print(innit)
        print(gm_info[x][2])
        print()

if_this_works_we_are_in_business(gm_info)


wiki_base_url = "https://en.wikipedia.org/wiki/"


#next up:
#scraping the release date for each film, wherever possible
#i need to verify that i grabbed the correct wiki page for each ebert film.