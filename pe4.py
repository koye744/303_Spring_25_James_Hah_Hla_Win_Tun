#Pair Exercise #4
#Hla Win Tun
#James Hah 
#Create code as outlined below in a file named pe4.py and push it to a github repository (you can use the same repo as previous pair exercises if you are paired with the same partner, something like 303_Spring_25).
#Your file will have code that addresses Section A as well as Section B.
#The wikipedia package enables access to and extraction of Wikipedia content using Python. More details on how the package works, including syntax, can be found here:
#https://www.thepythoncode.com/article/access-wikipedia-python.
#You can install the package in your virtual environment using pip as you would any other package: pip install wikipedia Use this package as described below.

#Import the wikipedia, time and concurrent.futures packages.
import wikipedia
import time
from concurrent.futures import ThreadPoolExecutor
import os

#Section A: Sequentially downolad wikipedia content 
#1. Use the wikipedia.search method to return a list of topics related to 'generative artificial intelligence'.
#2. Iterate over the topics returned in #1 above using a for loop. For each topic, do the following:
# - assign the page contents to a variable named 'page' using the wikipedia.page method. Be sure to use auto_suggest=False when using this method.
# -assign the page title to a variable (using page.title)
# - retrieve the references for that page (using page.references)
# - write the references (with each reference on its own line) to a .txt file where the name of the file is the title of the topics. For example, the topic "Music adn artifical intelligence" would be written to a file named "Music and artificial intelligence.txt".
# You may need to pay attention to the variable type returned by page.references, as only certain objects can be written to .txt fiels using the OBJECT.write method. 
# You may also need to manipulate what is returned to ensure each link is on its own line.
#3. Print to the console the amount of time it took the above code to excute, using time.perf_counter() (to finish step 2 for ALL topics in the list).

print("\n--- Starting Section A Starting Sequential Download ---")
start_sequential = time.perf_counter()

#1. Search for topics related to 'generative artificial intelligence'
topics = wikipedia.search('generative artificial intelligence')

#2 . Iterate over the topics and download references
for topic in topics:
    try:
        # Assigning the page contents to a variable using wikipedia.page method
        page = wikipedia.page(topic, auto_suggest=False)
        
        # Assigning the page title to a variable
        page_title = page.title
        
        # Retrieving the references for that page
        references = page.references
        
        # Write the references to a .txt file with the name of the topic
        with open(f"{page_title}.txt", "w", encoding="utf-8") as file:
            for reference in references:
                file.write(reference + "\n")

    except Exception as e:
        print(f"[Sequetnial] Skipping {topic} due to error: {e}")

end_sequential = time.perf_counter()
print(f"[Sequential] Finished downloading references for all topics in {end_sequential - start_sequential:.2f} seconds.")

#Section B: Concurrently download wikipedia content
# 1. Use the wikipedia.search method to return a list of topics related to 'generative artificial intelligence'.
# 2. Create a function def wiki_dl_and_save(topic) that:
# - retrieves the wikipedia page for the topic
# - gets the title and the references for the topic
# - writes the references to the file created in the preceding step (each reference on its own line)
# 3. Use the ThreadPoolExecutor from the concurrent.futures library to execute concurrently the function defiend in step 2.
# - you can call the .map() method of the ThreadPoolExecutor object with the function and the list of topics to assit with this step (the map method will execute a specified function for each object in an iterable that is passed in)
# 4. Print to the console the amount of time it took the above code to execute, using time.perf_counter() 
# Additional information
# The only function defined by nmae is the wiki_dl_and_save(topic) function. You are fee to write additional helper functions or abstracted functions if it makes more sense for you.

# Section B: Concurrently download Wikipedia content
# print("\n--- Starting Section B: Concurrent Download ---"
print("\n--- Starting Section B: Concurrent Download ---")
start_concurrent = time.perf_counter()

# 2. Define the function to download and save Wikipedia content
def wiki_dl_and_save(topic):
    try:
        # Retrieving the Wikipedia page for the topic
        page = wikipedia.page(topic, auto_suggest=False)
        
        # Getting the title and references for the topic
        page_title = page.title
        references = page.references
        
        # Writing the references to a .txt file with the name of the topic
        with open(f"{page_title}.txt", "w", encoding="utf-8") as file:
            for reference in references:
                file.write(reference + "\n")

    except Exception as e:
        print(f"[Concurrent] Skipping {topic} due to error: {e}")

# 3. Use ThreadPoolExecutor to execute the function concurrently
with ThreadPoolExecutor() as executor:
    # Map the function to the list of topics
    executor.map(wiki_dl_and_save, topics)

end_concurrent = time.perf_counter()
print(f"[Concurrent] Finished downloading references for all topics in {end_concurrent - start_concurrent:.2f} seconds.")





    

        