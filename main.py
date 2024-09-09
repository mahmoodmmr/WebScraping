import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

response = requests.get('https://www.dotabuff.com/heroes/alchemist/counters', headers=headers, verify=False)


# Write the full HTML response to a file
with open('response_content.html', 'w', encoding='utf-8') as file:
    file.write(response.text)

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')
with open('response_content.html', 'w', encoding='utf-8') as file:
    file.write(soup.text)

# Locate the section with class 'sortable'
matchups_section = soup.find('section', {'class': 'sortable'})

# Check if the matchups_section was found
if matchups_section:
    article = matchups_section.find('article')
    
    # If article is found, write its content to a file
    if article:
        with open('article_content.txt', 'w', encoding='utf-8') as file:
            file.write(article.text)
        print("Article content written to 'article_content.txt'")
    else:
        print("Could not find 'article' within the section")
else:
    print("Could not find 'section' with class 'sortable'")
