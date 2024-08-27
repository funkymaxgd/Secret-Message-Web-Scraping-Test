# Google Docs Message Decoder
# by Max Giroux Davis
# August 27th 2024 for Data Annotation coding assessment

# This script should:
# * accept a Google docs URL
# * retrieve and parse the information in the table
# * display sequence of characters based on Unicode characters and their position (x & y)
#

# Function to receive a Google Doc URL

import requests # for HTTP requests
from bs4 import BeautifulSoup # to parse HTML tree

google_doc_url = input("Enter a URL please: ")

def getURL(google_doc_url):
  # list to be filled with data
  data_list = []
  # grid to create display
  grid = []
  # extract the data from the HTML table
  url = google_doc_url 
  response = requests.get(url)
  html_doc = response.content
  soup = BeautifulSoup(html_doc, 'html.parser')
  data = soup.find_all('tr') # find all the table rows in the HTML content
  data.pop(0) # remove the top row with titles

  # X-coordinate, Unicode char, and Y-coordinate found between: <span class="c2"> .. <

  # go through each element in 'data'
  for i in data:
    tr_line = str(i)

    # find the items by searching for '<span class=', '>' and then '<', extracting what is between
    # extract X
    tr_line = tr_line[tr_line.find('span class='):]    
    tr_line = tr_line[tr_line.find('>')+1:]
    closing_tag = tr_line.find('<')
    x_pos = int(tr_line[0:closing_tag])
    # extract unicode
    tr_line = tr_line[tr_line.find('span class='):]    
    tr_line = tr_line[tr_line.find('>')+1:]
    closing_tag = tr_line.find('<')
    unicode = tr_line[0:closing_tag]
    # extract Y
    tr_line = tr_line[tr_line.find('span class='):]    
    tr_line = tr_line[tr_line.find('>')+1:]
    y_pos = int(tr_line[0:closing_tag])

    # create subList to add to data_list
    subList = [y_pos,x_pos,unicode]

    # append list to data_list
    data_list.append(subList)

  # sorting based on descending y-value and ascending x-value for orientation
  data_list.sort(key=lambda x: (-x[0], x[1]))

  max_y_value = max(data_list, key=lambda x: x[0])[0]
  max_x_value = max(data_list, key=lambda x: x[1])[1]

  # instantiate an xy grid with which to build the display

  for i in range(max_y_value,-1,-1):
    for a in range(max_x_value+1):
      item = [i,a," "]
      grid.append(item)

  # modify grid list with known values in data_list

  for i in data_list:
    for a in grid:
      if i[0] == a[0] and i[1] == a[1]:
        a[2] = i[2]

  # draw display based on grid and data_list

  for a in range(max_y_value,-1,-1):
    print()
    for b in range(max_x_value+1):
      for i in range(len(grid)):
        if grid[i][0]==a and grid[i][1]==b:
          print(grid[i][2], end="")

  
getURL(google_doc_url)



