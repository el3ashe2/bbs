import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

# Function to scrape news articles from BBC's front page
def scrape_bbc_news():
    url = 'https://www.bbc.com/news'
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # Fetch the page content
    response = requests.get(url, headers=headers)
    
    # Parse the content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the articles (this selector may change based on BBC's layout)
    articles = soup.find_all('h3', class_='gs-c-promo-heading__title')

    news_items = []
    
    # Extract the headlines and links to the articles
    for article in articles[:10]:  # Limit to top 10 articles
        title = article.get_text()
        link = article.parent.get('href')
        
        # Ensure link is absolute
        if not link.startswith('http'):
            link = 'https://www.bbc.com' + link

        news_items.append({'title': title, 'link': link})
    
    return news_items

# Function to save news items to an XML file
def save_to_xml(news_items, filename='news_articles.xml'):
    root = ET.Element('news')

    for item in news_items:
        news_item = ET.SubElement(root, 'article')
        
        title = ET.SubElement(news_item, 'title')
        title.text = item['title']
        
        link = ET.SubElement(news_item, 'link')
        link.text = item['link']
    
    tree = ET.ElementTree(root)
    tree.write(filename, encoding='utf-8', xml_declaration=True)

if __name__ == "__main__":
    # Scrape the news and save them to an XML file
    news_items = scrape_bbc_news()
    save_to_xml(news_items)
    print("News articles saved to news_articles.xml")
