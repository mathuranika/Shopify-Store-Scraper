from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import re
from app.gemini_utils import summarise_shopify_info

app = FastAPI()

class StoreRequest(BaseModel):
    website_url: str

@app.post("/extract_insights")
def extract_insights(payload: StoreRequest):
    base_url = payload.website_url.rstrip("/")
    try:
        res = requests.get(base_url, timeout=10)
        if res.status_code != 200:
            raise HTTPException(status_code=401, detail="Website not found.")

        # Step 1: Try to fetch products.json
        product_url = f"{base_url}/products.json"
        products_res = requests.get(product_url, timeout=10)

        products_data = []
        if products_res.status_code == 200:
            try:
                products_json = products_res.json()
                products_data = products_json.get("products", [])
            except Exception:
                products_data = []

        # Step 2: Parse Homepage HTML
        soup = BeautifulSoup(res.text, "lxml")

        # Extract Hero Product Names
        hero_products = []
        for tag in soup.find_all(["h2", "h3", "p", "span", "a"]):
            if tag and tag.text and any(keyword in tag.text.lower() for keyword in ["bestseller", "featured", "shop now", "hero", "new arrival", "popular"]):
                hero_products.append(tag.text.strip())

        # Extract About Brand Section
        about_text = ""
        about_sections = soup.find_all("section")
        for section in about_sections:
            if "about" in section.text.lower() and len(section.text.strip()) > 50:
                about_text = section.text.strip()
                break

        # Extract Emails and Phone Numbers
        emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", res.text)
        phones = re.findall(r"\+?\d[\d\s\-]{7,15}", res.text)

        # Extract Social Media Links
        socials = {
            "instagram": None,
            "facebook": None,
            "tiktok": None,
            "youtube": None,
            "linkedin": None,
            "twitter": None
        }
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if "instagram.com" in href:
                socials["instagram"] = href
            elif "facebook.com" in href:
                socials["facebook"] = href
            elif "tiktok.com" in href:
                socials["tiktok"] = href
            elif "youtube.com" in href:
                socials["youtube"] = href
            elif "linkedin.com" in href:
                socials["linkedin"] = href
            elif "twitter.com" in href:
                socials["twitter"] = href

        # Step 3: Extract Policy and Info Page Links
        policies = {
            "privacy_policy": None,
            "return_policy": None,
            "refund_policy": None,
            "faqs": None,
            "contact_us": None,
            "order_tracking": None,
            "blog": None
        }
        for link in soup.find_all("a", href=True):
            href = link["href"].lower()
            full_url = href if href.startswith("http") else f"{base_url}{href if href.startswith('/') else '/' + href}"
            if "privacy" in href and not policies["privacy_policy"]:
                policies["privacy_policy"] = full_url
            elif "return" in href and not policies["return_policy"]:
                policies["return_policy"] = full_url
            elif "refund" in href and not policies["refund_policy"]:
                policies["refund_policy"] = full_url
            elif "faq" in href and not policies["faqs"]:
                policies["faqs"] = full_url
            elif "contact" in href and not policies["contact_us"]:
                policies["contact_us"] = full_url
            elif "track" in href and not policies["order_tracking"]:
                policies["order_tracking"] = full_url
            elif "blog" in href and not policies["blog"]:
                policies["blog"] = full_url

        # Step 4: Extract Text from Policy Pages
        def extract_page_text(url):
            try:
                res = requests.get(url, timeout=10)
                soup = BeautifulSoup(res.text, "lxml")
                return soup.get_text(separator="\n", strip=True)[:1500]
            except:
                return None

        extracted_policies = {}
        for key, url in policies.items():
            if url:
                extracted_policies[key] = {
                    "url": url,
                    "text": extract_page_text(url)
                }

        # Step 5: Prepare Data for Gemini Summary
        combined_text = f"""
ABOUT SECTION:
{about_text}

PRODUCT NAMES:
{[p.get("title") for p in products_data]}

HERO SECTION HEADLINES:
{hero_products}

EMAILS:
{emails}

PHONES:
{phones}

SOCIAL MEDIA LINKS:
{socials}

POLICIES CONTENT:
{extracted_policies}
"""

        llm_summary = summarise_shopify_info(combined_text)

        return {
            "message": f"Successfully accessed {base_url}",
            "structured_summary": llm_summary,
            "product_catalog": products_data,
            "hero_products": hero_products,
            "about": about_text,
            "contact": {
                "emails": emails,
                "phones": phones
            },
            "social_links": socials,
            "policies": extracted_policies,
            "important_links": {k: v for k, v in policies.items() if v}
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
