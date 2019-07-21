#Initial Things to Load each Time

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

#List to store the last links obtained from each site
last_link = []

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
current_time = int(time.localtime()[1])*100+int(time.localtime()[2])
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
            response_list.append((current_time,link))
            

#--Saving the last links to a file --

#We will overwrite the file and enter new contents
with open("./check.txt",'w') as file:      
    for l in last_link:
        file.write(l)

#Deleting file content older than 30 days

older_than_days = 30
#Check for older images and delete those links
with open("response.txt",'r') as file:
    storage = file.readlines()
with open("response.txt",'w') as file:    
    for response in storage:
        if current_time - int(response.split('\'')[0]) <= older_than_days:
            file.write(response) #\n not added as previously added strings would already contain it
            
#Add the new responses to the file
with open("response.txt",'a') as file:      
    for r in response_list:
        file.write(str(r) + "\n")
        
#Overwrite the new file with the links now in response_list:
insert_list = []

with open("response.txt",'r') as file:      
    for l in file:
        insert_list.append(l.split('\'')[1])

#Add the links to image tags in the html page        
with open('index.html','w') as page:
    open_tags = "<html>\n<head>Meme Page</head>\n<body>\n<p>Hey! This is a page for some blogs that feature meme content.</p>\n"
    css_code = "<style> img.resize{\nmax-width:50%;\nmax-height:50%;\n}\n </style>\n"
    image_tags = ""
    for link in insert_list:
        image_tags += "<div><img style = 'max-width:800px;' src = '" + link[1] + "'></div>\n"
    end_tags = "</body>\n</html>"

    code = open_tags + css_code + image_tags +end_tags
    page.write(code)    
page.close()        

