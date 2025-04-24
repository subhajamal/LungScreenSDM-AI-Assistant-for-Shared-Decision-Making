import requests
from bs4 import BeautifulSoup
import json
import hashlib
from urllib.parse import urlparse

urls = [
    # cancer.gov
    "https://www.cancer.gov/types/lung/patient/lung-screening-pdq",
    "https://www.cancer.gov/types/lung/hp/lung-screening-pdq",
    "https://www.cancer.gov/types/lung/research/nlst",
    "https://dceg.cancer.gov/tools/risk-assessment/screen-lung-cancer",
    "https://prevention.cancer.gov/major-programs/lung-cancer-screening-image-library",
    "https://www.cancer.gov/about-cancer/screening/hp-screening-overview-pdq",
    "https://www.cancer.gov/about-cancer/screening/screening-tests",
    "https://progressreport.cancer.gov/detection/lung_cancer",
    "https://www.cancer.gov/news-events/cancer-currents-blog/2019/lung-cancer-screening-complications-diagnostic-follow-up",
    "https://prescancerpanel.cancer.gov/reports-meetings/cancer-screening-report-2022/challenges-opportunities",
    # lung.org
    "https://www.lung.org/lung-health-diseases/lung-disease-lookup/lung-cancer/saved-by-the-scan",
    "https://www.lung.org/lung-health-diseases/lung-disease-lookup/lung-cancer/screening-resources",
    "https://www.lung.org/lung-health-diseases/lung-disease-lookup/lung-cancer/screening-resources/what-to-expect-from-lung-cancer-screening",
    "https://www.lung.org/lung-health-diseases/lung-disease-lookup/lung-cancer/screening-resources/is-lung-cancer-screening-right",
    "https://www.lung.org/lung-health-diseases/lung-disease-lookup/lung-cancer/screening-resources/screening-qa",
    "https://www.lung.org/lung-health-diseases/lung-disease-lookup/lung-cancer/saved-by-the-scan/getting-screened",
    "https://www.lung.org/help-support/lung-helpline-and-tobacco-quitline/screening",
    "https://www.lung.org/blog/new-lung-cancer-screening-guidelines",
    "https://www.lung.org/lung-health-diseases/lung-disease-lookup/lung-cancer/screening-resources/what-to-look-for-in-a-screening-facility",
    "https://www.lung.org/professional-education/professional-education-materials/lung-cancer-screening-resources",
    "https://www.lung.org/lung-health-diseases/lung-disease-lookup/lung-cancer/screening-resources/lung-cancer-screening-insurance-coverage",
    "https://www.lung.org/lung-health-diseases/lung-disease-lookup/lung-cancer/saved-by-the-scan/facilities",
    "https://www.lung.org/lung-health-diseases/lung-disease-lookup/lung-cancer/saved-by-the-scan/doctor-discussion-guide",
    "https://www.lung.org/lung-health-diseases/lung-disease-lookup/lung-cancer/screening-resources/lung-cancer-screening-insurance-checklist",
    "https://www.lung.org/blog/why-lung-cancer-screening-isnt-for-never-smokers",
    "https://www.lung.org/research/trends-in-lung-disease/lung-cancer-screening-data",
    "https://www.lung.org/quit-smoking/helping-others-quit/lung-cancer-screening-and-tobacco-cessation",
    "https://www.lung.org/lung-health-diseases/lung-disease-lookup/lung-cancer/saved-by-the-scan"
]

def generate_id(url):
    return hashlib.md5(url.encode()).hexdigest()[:10]

metadata = []
for url in urls:
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string.strip() if soup.title else "No Title"
        paragraphs = soup.find_all("p")
        abstract = paragraphs[0].get_text(strip=True) if paragraphs else "No abstract found."
        combined_text = "\n\n".join(p.get_text(strip=True) for p in paragraphs[:10])
        metadata.append({
            "id": generate_id(url),
            "title": title,
            "abstract": abstract,
            "year": "2025",
            "journal": urlparse(url).netloc,
            "doi": None,
            "authors": [],
            "keywords": ["lung cancer", "screening", "web"],
            "pages": "",
            "combined_text": combined_text,
            "url": url
        })
    except Exception as e:
        metadata.append({
            "id": generate_id(url),
            "title": "Error fetching page",
            "abstract": str(e),
            "year": "2025",
            "journal": urlparse(url).netloc,
            "doi": None,
            "authors": [],
            "keywords": ["error"],
            "pages": "",
            "combined_text": "",
            "url": url
        })

# Save to file
with open("lung_metadata_web_fetched.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=4, ensure_ascii=False)

print("✅ Metadata saved to lung_metadata_web_fetched.json")
