import requests
from bs4 import BeautifulSoup

def fetch_arxiv_summaries(query):
    url = f"https://arxiv.org/search/?query={query}&searchtype=all&order=-announced_date_first"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # arXiv search results are usually in li elements with class 'arxiv-result'
    results = soup.find_all('li', class_='arxiv-result')
    
    summaries = []
    for res in results[:15]:
        # Extract title and abstract
        title_elem = res.find('p', class_='title')
        abstract_elem = res.find('p', class_='abstract-full')
        
        title = title_elem.text.strip() if title_elem else "No Title"
        abstract = abstract_elem.text.strip() if abstract_elem else "No Abstract"
        
        summaries.append(f"Title: {title}\nAbstract: {abstract}\n")
        
    return summaries

if __name__ == "__main__":
    query = "agentic workflow"
    summaries = fetch_arxiv_summaries(query)
    with open("arxiv_summaries.txt", "w", encoding="utf-8") as f:
        for s in summaries:
            f.write(s + "\n---\n")
    print(f"Successfully wrote {len(summaries)} summaries to arxiv_summaries.txt")
