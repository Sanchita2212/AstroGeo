import os
import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
import re
import time
from urllib.parse import urljoin, urlparse

# --- Configuration ---
MOSDAC_BASE_URL = "https://www.mosdac.gov.in"
SEED_URLS = [
    f"{MOSDAC_BASE_URL}/",
    f"{MOSDAC_BASE_URL}/faq-page",
    f"{MOSDAC_BASE_URL}/insat-3d-references",
    f"{MOSDAC_BASE_URL}/insat-3s-references", # Example for INSAT-3DS
    f"{MOSDAC_BASE_URL}/oceansat-3-introduction", # Example for Oceansat-3 docs
    f"{MOSDAC_BASE_URL}/oceansat-3-payloads"
]

# Where to save the scraped content
OUTPUT_DIR = "mosdac_data" # This will be relative to data_ingestion/
HTML_OUTPUT_DIR = os.path.join(OUTPUT_DIR, "web_pages")
DOC_OUTPUT_DIR = os.path.join(OUTPUT_DIR, "documents")

# Create output directories if they don't exist
os.makedirs(HTML_OUTPUT_DIR, exist_ok=True)
os.makedirs(DOC_OUTPUT_DIR, exist_ok=True)

# To prevent infinite loops and re-processing
visited_urls = set()

def save_html_content(url, text, tables):
    """
    Saves the extracted HTML content to a file.
    """
    # Create a safe filename from the URL path
    parsed_path = urlparse(url).path.strip('/')
    if not parsed_path:
        filename_base = 'index'
    else:
        # Replace problematic characters with underscores
        filename_base = re.sub(r'[^\w\-_\.]', '_', parsed_path)
    
    # Ensure filename is not too long or empty after cleaning
    if not filename_base:
        filename_base = "untitled_page"
    
    filepath = os.path.join(HTML_OUTPUT_DIR, f"{filename_base}.txt")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"URL: {url}\n\n")
        f.write("--- EXTRACTED TEXT ---\n")
        f.write(text)
        f.write("\n\n--- EXTRACTED TABLES ---\n")
        # Save tables in a simple format, can be improved for structured parsing later
        for table in tables:
            f.write(f"Headers: {table['headers']}\n")
            f.write(f"Data: {table['data']}\n")
    print(f"Saved HTML content: {filepath}")


def extract_text_from_pdf(filepath):
    """
    Extracts text from a PDF file and saves it to a .txt file.
    """
    try:
        doc = fitz.open(filepath)
        pdf_text = ""
        for page in doc:
            pdf_text += page.get_text()
        
        # Save the extracted text to a text file
        output_path = os.path.join(DOC_OUTPUT_DIR, os.path.basename(filepath) + ".txt")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(pdf_text)
        
        print(f"Extracted text from PDF and saved to: {output_path}")
        doc.close()
        return pdf_text
    except Exception as e:
        print(f"Error extracting text from PDF {filepath}: {e}")
        return ""


def download_document(url):
    """
    Downloads a document (like PDF, DOCX, XLSX) from a URL and saves it locally.
    Also extracts text from PDFs.
    """
    if url in visited_urls:
        return
    
    visited_urls.add(url)
    
    try:
        print(f"Downloading document: {url}")
        response = requests.get(url, timeout=30, stream=True) # Use stream=True for large files
        response.raise_for_status()

        # Extract filename from URL
        filename = url.split('/')[-1]
        filepath = os.path.join(DOC_OUTPUT_DIR, filename)

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192): # Download in chunks
                f.write(chunk)
            
        print(f"Saved: {filepath}")
        
        # If it's a PDF, extract its text content
        if filename.lower().endswith('.pdf'):
            extract_text_from_pdf(filepath)

    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during document download/processing for {url}: {e}")


# ... (rest of your imports and code) ...

def crawl_and_extract(url, crawl_depth_limit=3, current_depth=0):
    if url in visited_urls or current_depth > crawl_depth_limit:
        print(f"Skipping {url}: Already visited or max depth reached.")
        return []
    
    visited_urls.add(url)
    print(f"\n--- Starting Crawl (Depth {current_depth}): {url} ---")

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        print(f"Successfully fetched URL. Status Code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    print("HTML parsed successfully.")

    # --- 1. Extract Main Text Content ---
    text_content = ""
    main_content_div = soup.find('div', class_='main-content')
    if main_content_div:
        for tag in main_content_div.find_all(['p', 'h1', 'h2', 'h3', 'li', 'span', 'div']):
            text_content += tag.get_text(separator=' ', strip=True) + "\n"
    else:
        for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'li']):
            text_content += tag.get_text(separator=' ', strip=True) + "\n"
    print(f"Extracted a total of {len(text_content)} characters of text.")

    # --- 2. Extract Tables ---
    extracted_tables = []
    # (Your table extraction code remains the same here)
    for table in soup.find_all('table'):
        headers = [th.get_text(strip=True) for th in table.find_all('th')]
        rows = []
        for tr in table.find_all('tr'):
            row_data = [td.get_text(strip=True) for td in tr.find_all('td')]
            if row_data:
                rows.append(row_data)
        if headers or rows:
            extracted_tables.append({"headers": headers, "data": rows})
    print(f"Found {len(extracted_tables)} tables.")

    # Save the extracted content to a file
    save_html_content(url, text_content, extracted_tables)

    # --- 3. Find New Links to Crawl and Documents to Download ---
    new_links_to_crawl = []
    print("Looking for new links...")
    
    all_a_tags = soup.find_all('a', href=True)
    print(f"Found {len(all_a_tags)} potential links.")

    for a_tag in all_a_tags:
        href = a_tag['href']
        full_url = urljoin(url, href)
        parsed_url = urlparse(full_url)
        
        # DEBUGGING: Print all the URLs found and why they're filtered
        # print(f"Found: {full_url}")

        if parsed_url.scheme in ['http', 'https'] and parsed_url.netloc == urlparse(MOSDAC_BASE_URL).netloc:
            # Check for document file extensions
            if href.lower().endswith(('.pdf', '.docx', '.xlsx', '.doc')):
                download_document(full_url)
            # Add to the list of new links to crawl (only HTML pages)
            elif not any(full_url.lower().endswith(ext) for ext in ['.pdf', '.docx', '.xlsx', '.doc', '.zip', '.tar', '.rar']) \
                 and full_url not in visited_urls and parsed_url.path != '':
                print(f"Adding new link to queue: {full_url}")
                new_links_to_crawl.append(full_url)
            else:
                pass
                # print(f"Filtering out: {full_url} (already visited, not a page, or a non-doc file)")
        # else:
            # print(f"Filtering out: {full_url} (external link)")

    print(f"Found {len(new_links_to_crawl)} new links to crawl.")
    return new_links_to_crawl

# ... (rest of your main block) ...
if __name__ == "__main__":
    # Max depth for crawling. Be careful with this, higher numbers mean much longer crawls.
    # For initial testing, keep it low (e.g., 2 or 3).
    MAX_CRAWL_DEPTH = 2 # This means it crawls seed URLs (depth 0), then links on those pages (depth 1), etc.

    url_queue = [(url, 0) for url in SEED_URLS] # Store (url, depth) tuples
    
    while url_queue:
        current_url, current_depth = url_queue.pop(0)
        
        if current_depth > MAX_CRAWL_DEPTH:
            continue # Skip if beyond max depth

        new_links = crawl_and_extract(current_url, MAX_CRAWL_DEPTH, current_depth)
        
        # Add new links to the queue with incremented depth
        for link in new_links:
            url_queue.append((link, current_depth + 1))
        
        # Optional: Add a small delay between requests to be polite to the server
        time.sleep(0.5) 
    
    print("\n--- Data Ingestion complete ---")
    print(f"Total unique URLs/Documents processed: {len(visited_urls)}")
    print(f"Raw web pages saved to: {HTML_OUTPUT_DIR}")
    print(f"Documents and extracted text saved to: {DOC_OUTPUT_DIR}")