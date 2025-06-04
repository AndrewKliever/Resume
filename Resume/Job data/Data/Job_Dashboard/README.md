# Job Sales Dashboard

This is a simple interactive dashboard built with Plotly and HTML/JavaScript to visualize job sales data.

## 📊 Features
- Bar charts for total dollar amount by category (2024 & 2025)
- Interactive scatter plot: days to sale vs. total sale amount
- Weekly sales line graph with job totals

## 🚀 How to Run

### Option 1: GitHub Pages
1. Upload the contents of this folder to a GitHub repository.
2. Enable GitHub Pages from the repo settings using the root directory.
3. Your site will be live at:
   ```
   https://yourusername.github.io/repository-name/
   ```

### Option 2: Local Preview
Run a simple server:
```bash
python -m http.server 8000
```
Then visit `http://localhost:8000`

> **Note:** Opening `index.html` directly from your file system may not load charts due to browser security restrictions.

## 🗂 Files
- `index.html`
- `dashboard.js`
- JSON files for the charts
