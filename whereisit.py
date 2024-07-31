import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def get_search_results(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'referer': 'https://www.google.com'
    }
    target_url = f'https://www.google.com/search?q={query}&num=20'
    resp = requests.get(target_url, headers=headers)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        results = soup.find_all("div", {"class": "jGGQ5e"})
        urls = [result.find("div", {"class": "yuRUbf"}).find("a").get('href') for result in results]
        return urls, results
    else:
        return [], []

st.title('Search and Position Checker')

search_query = st.text_input('Enter a search term:', '')
target_domain = st.text_input('Enter a domain to check (optional):')

if st.button('Search'):
    if search_query:
        with st.spinner('Searching...'):
            urls, results = get_search_results(search_query)
            if urls:
                st.success(f"Found {len(urls)} results:")
                for url in urls:
                    st.write(url)
                
                # Checking for domain presence if provided
                if target_domain:
                    found = False
                    for index, result in enumerate(results):
                        href = result.find("div", {"class": "yuRUbf"}).find("a").get('href')
                        domain = urlparse(href).netloc
                        if domain == target_domain:
                            found = True
                            position = index + 1
                            break
                    if found:
                        st.write(f"Domain {target_domain} found at position {position}.")
                    else:
                        st.error(f"Domain {target_domain} not found in the top {len(results)}.")
            else:
                st.error('No results found.')
    else:
        st.error('Please enter a search term to proceed.')
