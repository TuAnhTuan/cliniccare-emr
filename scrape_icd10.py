"""
Scrapes billable (leaf) ICD-10-CM codes from icd10data.com to seed the
ClinicCare Mini EMR database.

Usage:
    pip install requests beautifulsoup4
    python scrape_icd10.py

Output: backend/seed/icd10_codes.csv (code,description)
        backend/seed/icd10_seed.sql  (INSERT statements matching the `diagnoses` table)
"""

import csv
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE = "https://www.icd10data.com"

# A realistic browser User-Agent is required — the site returns 403 for
# generic/bot-looking User-Agent strings.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# Common chapter ranges seen in a general clinic.
RANGES = [
    "/ICD10CM/Codes/E00-E89/E08-E13",   # Diabetes mellitus
    "/ICD10CM/Codes/I00-I99/I10-I1A",   # Hypertensive diseases
    "/ICD10CM/Codes/J00-J99/J00-J06",   # Acute upper respiratory infections
    "/ICD10CM/Codes/J00-J99/J09-J18",   # Influenza and pneumonia
    "/ICD10CM/Codes/K00-K95/K20-K31",   # Diseases of esophagus, stomach, duodenum
    "/ICD10CM/Codes/M00-M99/M50-M54",   # Other dorsopathies (back pain)
    "/ICD10CM/Codes/N00-N99/N30-N39",   # Other diseases of urinary system
    "/ICD10CM/Codes/L00-L99/L20-L30",   # Dermatitis and eczema
    "/ICD10CM/Codes/F01-F99/F40-F48",   # Anxiety disorders
    "/ICD10CM/Codes/R00-R99/R50-R69",   # General symptoms and signs
]

MAX_CODES = 100
REQUEST_DELAY_SECONDS = 1.0

OUTPUT_DIR = Path(__file__).parent / "backend" / "seed"


def get_soup(url):
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


def find_billable_leaf_links(range_path):
    """
    A range page (e.g. /E08-E13) embeds a hidden preview tree for every
    category, built from <li class="codeLine"> entries. Each entry has an
    <i class="glyphicon ... success"> icon for billable (leaf) codes, or
    "danger" for codes that still have children. We only want the
    billable ones, and we grab their href to fetch the full description
    from that code's own page later.

    The page also embeds an unrelated "related codes" widget earlier in
    the DOM (e.g. the I10-I1A hypertension page lists F17.x nicotine
    dependence codes first). We filter results down to the chapter
    letter the range itself belongs to, so that noise is dropped.
    """
    chapter_letter = range_path.rstrip("/").split("/")[-2][0]

    soup = get_soup(BASE + range_path)
    links = []

    for li in soup.find_all("li", class_="codeLine"):
        icon = li.find("i", class_="glyphicon")
        link = li.find("a", class_="identifier")
        if not icon or not link:
            continue
        if "success" not in icon.get("class", []):
            continue  # has children -> not a billable leaf code
        code = link.get_text(strip=True)
        href = link.get("href")
        if code and href and code[0] == chapter_letter:
            links.append((code, href))

    return links


def fetch_description(href):
    """
    A leaf code's own page has a clean, non-truncated description in its
    <title>, formatted as "<year> ICD-10-CM Diagnosis Code <CODE>: <description>".
    """
    soup = get_soup(BASE + href)
    title = soup.title.get_text(strip=True) if soup.title else ""
    match = re.search(r"Diagnosis Code\s+\S+:\s*(.+)", title)
    return match.group(1).strip() if match else ""


def main():
    # Take an even share from each range first so the final set covers a
    # spread of conditions instead of one chapter (e.g. diabetes) crowding
    # out everything else just because it has more sub-codes.
    per_range_cap = MAX_CODES // len(RANGES)
    seen_codes = {}

    for range_path in RANGES:
        print(f"Scanning {range_path} ...")
        try:
            links = find_billable_leaf_links(range_path)
            for code, href in links[:per_range_cap]:
                if code not in seen_codes:
                    seen_codes[code] = href
        except Exception as e:
            print(f"  Error scanning range: {e}")
        time.sleep(REQUEST_DELAY_SECONDS)

    codes_to_fetch = list(seen_codes.items())[:MAX_CODES]
    print(f"Found {len(codes_to_fetch)} billable codes, fetching descriptions...")

    final_codes = []
    for code, href in codes_to_fetch:
        try:
            description = fetch_description(href)
            if description:
                final_codes.append((code, description))
                print(f"  {code}: {description}")
        except Exception as e:
            print(f"  Error fetching {code}: {e}")
        time.sleep(REQUEST_DELAY_SECONDS)

    print(f"\nCollected {len(final_codes)} codes with descriptions.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_DIR / "icd10_codes.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["code", "description"])
        writer.writerows(final_codes)

    with open(OUTPUT_DIR / "icd10_seed.sql", "w", encoding="utf-8") as f:
        f.write("-- Seed data for the diagnoses table (ICD-10-CM billable codes)\n")
        f.write("-- Source: https://www.icd10data.com/ICD10CM/Codes\n\n")
        for code, description in final_codes:
            safe_description = description.replace("'", "''")
            f.write(
                "INSERT INTO diagnoses (icd10_code, description) VALUES "
                f"('{code}', '{safe_description}') "
                "ON CONFLICT (icd10_code) DO NOTHING;\n"
            )

    print(f"Done. See {OUTPUT_DIR / 'icd10_codes.csv'} and {OUTPUT_DIR / 'icd10_seed.sql'}")


if __name__ == "__main__":
    main()
