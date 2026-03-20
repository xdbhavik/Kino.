# 🎬 Kino.

**Kino.** is a content-based movie recommendation web app built with Python and Flask. Enter a movie title and instantly get 6 similar movie suggestions powered by a precomputed cosine similarity matrix.

🔗 **Live Demo:** [kino-eight-sigma.vercel.app](https://kino-eight-sigma.vercel.app)

---

## ✨ Features

- 🔍 Search any movie by title (case-insensitive)
- 🎯 Returns top 6 content-based recommendations
- ⚡ Fast lookups using a precomputed similarity matrix
- 🧩 Splits & reconstructs large pickle files automatically at startup
- 🌐 Deployed and accessible via Vercel

---

## 🛠️ Tech Stack

| Layer       | Technology                        |
|-------------|-----------------------------------|
| Backend     | Python, Flask                     |
| ML / Data   | scikit-learn, pandas, numpy       |
| Serialization | pickle                          |
| Frontend    | HTML, CSS (Jinja2 templates)      |
| Deployment  | Vercel (with gunicorn)            |

---

## 📁 Project Structure

```
Kino./
├── app.py                  # Flask app — routes, recommendation logic, data loading
├── movie_list.pkl           # Serialized list of movie titles
├── similarity.pkl.part1     # Similarity matrix split into 4 parts
├── similarity.pkl.part2
├── similarity.pkl.part3
├── similarity.pkl.part4
├── split_data.py            # Script to split the large similarity.pkl for GitHub
├── requirements.txt         # Python dependencies
├── templates/               # Jinja2 HTML templates
├── static/                  # CSS and static assets
└── training/                # Model training notebooks/scripts
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/xdbhavik/Kino.
   cd Kino.
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**

   ```bash
   python app.py
   ```

4. Open your browser and go to `http://127.0.0.1:5000`

> **Note:** On first run, the app automatically reconstructs `similarity_reconstructed.pkl` from the four split parts. This only happens once.

---

## 🧠 How It Works

1. **Training** — A similarity matrix is computed (cosine similarity) over movie features using scikit-learn. The resulting pickle file is split into 4 parts using `split_data.py` to work around GitHub's 100MB file size limit.

2. **At startup** — `app.py` checks if `similarity_reconstructed.pkl` exists. If not, it merges the four parts back into a single file and loads it into memory.

3. **On search** — The user inputs a movie title. The app finds its index in `movie_list.pkl`, retrieves the top 6 most similar movies from the similarity matrix (excluding the movie itself), and returns them as recommendations.

---

## 📦 Dependencies

```
Flask
pandas
numpy
scikit-learn
gunicorn
```

Install all with:

```bash
pip install -r requirements.txt
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to open a pull request or file an issue.

---

## 📄 License

This project is open source. Feel free to use and modify it.

---

*Built with ❤️ by [xdbhavik](https://github.com/xdbhavik)*
