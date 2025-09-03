# 🛒 Amazon Analytics Hub

An interactive Streamlit dashboard to analyze Amazon product data with powerful filters, KPIs, and visualizations.  
Built to explore product performance, discounts, ratings, and customer reviews in a simple yet professional interface.  

🌐 **Live Demo**: [Amazon Dashboard (Streamlit)](https://amazon-dashboard-project-mtsmol5cxwcoxwt2nytupd.streamlit.app/)  
📂 **Repository**: [GitHub Repo](https://github.com/thanuSiva18/amazon-dashboard-Project)

---

## 📌 Features
- 🎯 **Smart Filters**: category, rating, discounts, reviews, search by product name  
- 📈 **Key Performance Indicators**: total products, avg. rating, avg. discount, total reviews, max discount  
- 📊 **Visual Analytics**: pie, bar, scatter, histograms, correlation heatmaps, radar charts  
- 🔬 **Advanced Analytics Tabs**: discount insights, correlations, distributions, top performers  
- 🛍️ **Featured Products**: best rated, most reviewed, top discounted  
- 📥 **Export Data**: download filtered dataset as CSV  
- 📋 **Data Quality Report**: completeness, anomalies, quick insights  

---

## 🏗️ Project Architecture
```text
Amazon Dataset (CSV)
        │
        ▼
   Data Cleaning & Preprocessing (Pandas)
        │
        ▼
 Interactive Dashboard (Streamlit + Plotly)
        │
        ▼
   Deployment (Streamlit Cloud)
````

---

## ⚙️ Tech Stack

* **Python** (pandas, numpy)
* **Visualization**: Plotly Express, Plotly Graph Objects
* **Framework**: Streamlit
* **ML Utility**: scikit-learn (MinMaxScaler for radar chart)
* **Deployment**: Streamlit Cloud

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/thanuSiva18/amazon-dashboard-Project.git
cd amazon-dashboard-Project
```

### 2. Create virtual environment (optional but recommended)

```bash
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate  # On Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the dashboard

```bash
streamlit run dashboard.py
```

### 5. Open in browser

Go to `http://localhost:8501`

---

## 📸 Screenshots

<img width="1474" height="894" alt="Screenshot 2025-09-03 155123" src="https://github.com/user-attachments/assets/8d939052-c587-4624-80ab-824bfaaada1a" />
<img width="1913" height="930" alt="Screenshot 2025-09-03 155113" src="https://github.com/user-attachments/assets/fb9852f9-8c6f-43da-8cc0-e36691434213" />
<img width="1903" height="944" alt="Screenshot 2025-09-03 155058" src="https://github.com/user-attachments/assets/7fefc75a-c7ec-42a9-9426-767d6209c8e7" />

---

## 📌 Insights

* Categories with consistently high ratings
* Correlation between discounts and ratings
* Top-performing products & categories
* Data anomalies (e.g., extreme discounts, missing reviews)

---

## 👤 Author

**Thanu Siva** – AI & Data Science Enthusiast
Built with ❤️ to explore e-commerce data and generate meaningful business insights.


---

Do you want me to also make a **short LinkedIn caption** (with GitHub + hosted link) so you can post today?
```
