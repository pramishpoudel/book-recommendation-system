from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pickle
import numpy as np

# Load your pickle files
popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

app = FastAPI()

# Setup templates folder
templates = Jinja2Templates(directory="templates")

# ---------- Routes ----------

# Index page
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "book_name": list(popular_df['Book-Title'].values),
        "author": list(popular_df['Book-Author'].values),
        "image": list(popular_df['Image-URL-M'].values),
        "votes": list(popular_df['num_ratings'].values),
        "rating": list(popular_df['avg_ratings'].values)
    })

# Recommend page (UI only)
@app.get("/recommend", response_class=HTMLResponse)
async def recommend_ui(request: Request):
    return templates.TemplateResponse("recommend.html", {"request": request})

# Recommend books (form submission)
@app.post("/recommend_books", response_class=HTMLResponse)
async def recommend_books(request: Request, user_input: str = Form(...)):
    # Case-insensitive search
    indices = np.where(pt.index.str.lower() == user_input.lower().strip())[0]

    if len(indices) == 0:
        return templates.TemplateResponse("recommend.html", {
            "request": request,
            "error": f"No book found with name '{user_input}'"
        })

    index = indices[0]

    # Get top 5 similar books
    similar_items = sorted(
        list(enumerate(similarity_scores[index])),
        key=lambda x: x[1],
        reverse=True
    )[0:8]

    data = []
    for i in similar_items:
        temp_df = books[books['Book-Title'].str.strip() == pt.index[i[0]].strip()]
        if not temp_df.empty:
            item = [
                temp_df['Book-Title'].values[0],
                temp_df['Book-Author'].values[0],
                temp_df['Image-URL-M'].values[0]
            ]
            data.append(item)

    return templates.TemplateResponse("recommend.html", {
        "request": request,
        "data": data
    })

# Run locally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("application:app", host="127.0.0.1", port=8080, reload=True)
