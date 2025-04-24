import os
import json
import faiss
import numpy as np
import lxml.etree as ET
from sentence_transformers import SentenceTransformer
from typing import List, Dict

# ---------------- CONFIG ----------------
XML_FOLDER = r"C:\Users\subha\Downloads\LungCancerChatbot\PMC_XML_Files"
OUTPUT_INDEX = r"C:\Users\subha\Downloads\LungCancerChatbot\lung_faiss.index"
OUTPUT_META = r"C:\Users\subha\Downloads\LungCancerChatbot\lung_metadata.json"

# ---------------- Load Model ----------------
embedding_model = SentenceTransformer("all-mpnet-base-v2")

# ---------------- Helpers ----------------
def clean_text(text: str) -> str:
    return text.replace("\n", " ").replace("\t", " ").strip()

def parse_bioc_xml(file_path: str) -> List[Dict]:
    parser = ET.XMLParser(recover=True)
    try:
        tree = ET.parse(file_path, parser)
    except Exception as e:
        print(f"❌ Failed to parse {file_path}: {e}")
        return []

    root = tree.getroot()
    articles = []

    for doc in root.findall("document"):
        article = {
            "id": doc.findtext("id", default="Unknown"),
            "title": "No Title",
            "abstract": "",
            "introduction": "",
            "methods": "",
            "results": "",
            "year": "Unknown",
            "journal": "Unknown",
            "doi": "",
            "authors": [],
            "keywords": [],
            "pages": "Unknown-Unknown"
        }

        for passage in doc.findall("passage"):
            section = passage.findtext("infon[@key='section_type']", default="").lower()
            text = clean_text(passage.findtext("text", default=""))

            if not text:
                continue

            if "title" in section and len(text) > 5:
                article["title"] = text
            elif "abstract" in section:
                article["abstract"] += text + " "
            elif "intro" in section:
                article["introduction"] += text + " "
            elif "method" in section:
                article["methods"] += text + " "
            elif "result" in section:
                article["results"] += text + " "

            for infon in passage.findall("infon"):
                key = infon.get("key", "").lower()
                val = infon.text.strip() if infon.text else ""

                if key == "journal-title":
                    article["journal"] = val
                elif key == "year":
                    if val.isdigit():
                        article["year"] = val
                elif key == "article-id_doi":
                    article["doi"] = val
                elif key == "kwd":
                    article["keywords"].extend(val.split())
                elif key.startswith("name_"):
                    try:
                        parts = val.split(";")
                        surname = parts[0].split(":")[1].strip()
                        given = parts[1].split(":")[1].strip()
                        article["authors"].append(f"{given} {surname}")
                    except:
                        continue
                elif key == "fpage":
                    article["pages"] = val + "-" + article["pages"].split("-")[-1]
                elif key == "lpage":
                    article["pages"] = article["pages"].split("-")[0] + "-" + val

        combined = f"{article['title']}. {article['abstract']} {article['introduction']} {article['methods']} {article['results']}".strip()
        if len(combined) > 50:
            article["combined_text"] = combined
            articles.append(article)

    return articles

# ---------------- Main ----------------
def main():
    if not os.path.exists(XML_FOLDER):
        print(f"🚫 XML folder not found: {XML_FOLDER}")
        return

    xml_files = sorted([os.path.join(XML_FOLDER, f) for f in os.listdir(XML_FOLDER) if f.endswith(".xml")])
    print(f"🔍 Found {len(xml_files)} XML files to parse.")

    all_articles = []
    for file in xml_files:
        all_articles.extend(parse_bioc_xml(file))

    if not all_articles:
        print("🚫 No valid articles found. Exiting.")
        return

    print(f"✅ Parsed {len(all_articles)} valid articles. Embedding...")

    texts = [article["combined_text"] for article in all_articles]
    embeddings = embedding_model.encode(texts, convert_to_numpy=True).astype(np.float32)

    print("📦 Building FAISS index...")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, OUTPUT_INDEX)
    print(f"✅ FAISS index saved to: {OUTPUT_INDEX}")

    print("📝 Saving metadata...")
    with open(OUTPUT_META, "w", encoding="utf-8") as f:
        json.dump(all_articles, f, indent=2, ensure_ascii=False)
    print(f"✅ Metadata saved to: {OUTPUT_META}")

if __name__ == "__main__":
    main()
