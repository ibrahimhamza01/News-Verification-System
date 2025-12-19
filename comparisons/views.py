from django.http import JsonResponse
from django.views import View
from .models import Comparison
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from sentence_transformers import SentenceTransformer, util
import torch
from transformers import pipeline
import os
import json
from django.views.decorators.csrf import csrf_exempt

# Initialize resources that don't need to be recreated per request
embedder = SentenceTransformer("all-MiniLM-L6-v2")

pipe = pipeline(
        "text-generation", 
        model='../nlp_proj/llama',
        torch_dtype=torch.bfloat16, 
        device_map="auto"
    )

@csrf_exempt  # Remove CSRF validation for testing purposes (not recommended for production)
def handle_post_request(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON body
            print(data)
            prompt = data.get('prompt')

            # Initialize Selenium WebDriver inside the method
            chrome_options = Options()
            # chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            driver.set_page_load_timeout(15)
            print('1')

            search_term = prompt
            query_filters = (
                f"-site:youtube.com -site:books.google.com -filetype:pdf "
                f'-inurl:search -inurl:category inurl:article OR intitle:"{search_term}"'
            )
            search_query = f"{search_term} {query_filters}"

            print('2')

            # Open Google
            driver.get("https://www.google.com")

            print('3')

            # Wait for the search bar to appear
            search_bar = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )

            print('4')

            # Enter the search query into the search bar
            search_bar.send_keys(search_query)
            search_bar.send_keys(Keys.RETURN)

            print('5')

            # Wait for the search results to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3.LC20lb.MBeuO.DKV0Md"))
            )

            print('6')

            num_results = 12

            # Retrieve the first results (more than 6 to handle skips)
            results = driver.find_elements(By.CSS_SELECTOR, "h3.LC20lb.MBeuO.DKV0Md")[:num_results]
            articles = []

            print('7')

            for result in results:
                # Navigate up to the <a> tag containing the link
                link_element = result.find_element(By.XPATH, "./ancestor::a")
                article_link = link_element.get_attribute("href")
                articles.append(article_link)

            print('8')

            # List to store article data
            article_data = []

            # Encode the search term
            search_term_vector = embedder.encode(search_term, convert_to_tensor=True)

            print("8.5")

            # Fetch and process each article
            for article_url in articles:
                if len(article_data) >= 6:
                    break

                article_content = get_article_text(driver, article_url)
                if article_content:
                    try:
                        # Encode the article content
                        article_vector = embedder.encode(
                            article_content, convert_to_tensor=True
                        )


                        # Calculate cosine similarity
                        cosine_similarity = util.cos_sim(
                            search_term_vector, article_vector
                        ).item()


                        # Store the article text, embedding, similarity score, and link
                        article_data.append(
                            {
                                "text": article_content,
                                "embedding": article_vector.tolist(),
                                "similarity_score": cosine_similarity,
                                "link": article_url,
                            }
                        )
                    except Exception as e:
                        continue  # Skip if processing fails


            print('9')

            sum_similarity = 0

            for article in article_data:
                sum_similarity += article["similarity_score"]

            average_similarity = sum_similarity / len(article_data) if article_data else 0

            print(average_similarity)
            


                    # Format the output data
            output_data = {"Prompt": search_term, "comparisons": article_data}
            driver.quit()
            return JsonResponse({"prompt": search_term, "output": article_data, "average": average_similarity}, status=200)

            print(output_data)

  

            # Close the driver after processing
            

            return JsonResponse({"response": results}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

def get_article_text(driver, url):
    try:
        print('test0.5')
        # Navigate to the article URL
        driver.get(url)

        print('test')
        # Wait for the main content to load (customize selectors for each site if needed)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )


        print(url)

        print('Done url')
        # Extract the main content (fallback approach using <p> tags)
        paragraphs = driver.find_elements(By.TAG_NAME, "p")
        print('test2')
        article_text = " ".join([para.text for para in paragraphs])

        return article_text
    except Exception as e:
        print(f"Failed to fetch content from {url}: {e}")
        return None
