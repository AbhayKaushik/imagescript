#Initial Things to Load each Time
last_link = []

#Last Link list loaded
check_list = []
with open('./check.txt', 'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        link = ''.join(row)
        check_list.append(link)
csvFile.close()

#list to store the responses
response_list = []

#--Part 1: The Reddit Script--

response = requests.get('https://www.reddit.com/r/comics/')
tries = 0

#Make multiple requests to busy server 
while not response.ok and tries < 20:
    time.sleep(1)
    response = requests.get('https://www.reddit.com/r/comics/')
    tries += 1
    
print("Response recieved")
soup = BeautifulSoup(response.text, 'html.parser').findAll('img')
for i in range(len(soup)-1,-1,-1):
    tag = soup[i]
    link = tag['src']
    if 'external' in link or 'static' in link:
        continue
    n_link = link.split('?')[0].replace('preview','i')
    if not n_link in check_list:
        response_list.append(n_link)
    else:
        break
        
print(response_list)
last_link.append(response_list[::-1][0])

#--Part 2 : The Everything Else Script--

#list of urls
url_list = [
    'https://turnoff.us/feed.xml',
    'http://www.incidentalcomics.com/',
    'https://xkcd.com/'
    ]

idx = 0
for url in url_list: 
    response = requests.get(url)
    if(response.ok):
        soup = BeautifulSoup(response.text, 'html.parser').findAll('img')
        tag = soup[idx]
        link = tag['src']
        if idx < 1:
            idx += 1
        if not link.startswith('h'):
            #Adding https in the start to create a valid link
            link = 'https:' + str(link)
        last_link.append(link)
        if not link in check_list:
            response_list.append(link)
            

#--Saving the last links to a file --

#We will overwrite the file and enter new contents
with open("./check.txt",'w') as file:
    for l in last_link:
        file.write(l)

##Load the new images to the folder
if 'Blog-Images' not in os.listdir('./'):
    os.mkdir('./Blog-Images/')

for link in response_list:
    img_name = link.split('/')
    for n in img_name :
        if 'jpg' in n or 'png' in n:
            name = n
    value = urllib.request.urlretrieve(link, filename = './Blog-Images/'+ name)

