
# 📰 Variety News Article Scraper

A Python-based web scraping application built using Streamlit that extracts news articles from [Variety](https://variety.com/) based on a selected publication date.

## 📌 Project Overview

The Variety News Article Scraper allows users to select a specific publication date and automatically collect articles published on that date.

The application extracts article details, displays the results in an interactive dashboard, and allows users to download the extracted information in CSV format.

## ✨ Features

- Select a specific article publication date.
- Automatically retrieve article URLs from the Variety sitemap.
- Extract article publication dates.
- Extract article titles.
- Extract article URLs.
- Extract main article body text.
- Display the total number of articles found.
- Show extracted information in an interactive dashboard.
- Download extracted article data as a CSV file.
- Track scraping progress through a progress bar.

## 📊 Data Extracted

The application extracts the following five fields for each article:

| Field | Description |
|---|---|
| Article Date | Date the article was published |
| Title | Article headline |
| URL | Original Variety article link |
| Main Body Text | Main content of the article |
| Website Name | Variety |

## 🛠️ Technologies Used

- **Python** – Main programming language
- **Streamlit** – Interactive web dashboard
- **Requests** – Fetch webpage and sitemap data
- **BeautifulSoup4** – HTML parsing and content extraction
- **Pandas** – Data handling and CSV export
- **XML ElementTree** – Sitemap parsing

## 📁 Project Structure

```text
News_Article_Scraper/
│
├── app.py
├── scraper.py
├── requirements.txt
├── README.md
└── articles.csv
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/variety-news-article-scraper.git
```

### 2. Open the project folder

```bash
cd variety-news-article-scraper
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

### 5. Open the dashboard

Open the following URL in your browser:

```text
http://localhost:8501
```

## 🚀 How to Use

1. Open the Variety News Article Scraper dashboard.
2. Select the required publication date.
3. Click the **Search Articles** button.
4. Wait for the scraping process to complete.
5. View the total number of articles found.
6. Review the extracted article details.
7. Click **Download Complete CSV** to export the results.

## 📥 Output

The extracted article information is saved in CSV format.

**Output file:** `articles.csv`

The CSV file contains:

- Article Date
- Title
- URL
- Main Body Text
- Website Name

## 🌐 Data Source

Website: https://variety.com/

Articles are retrieved using the website's monthly sitemap and individual article pages.

## ⚠️ Notes

- Results depend on the availability and structure of Variety's sitemap.
- Some articles may not expose publication dates or article content in accessible page metadata.
- Website changes may require updates to the scraping logic.
- Please respect the website's terms of service and scraping policies.

## 👨‍💻 Developer

**Siddhesh Bane**

GitHub: https://github.com/YOUR_USERNAME

---

⭐ If you find this project useful, feel free to star the repository!
