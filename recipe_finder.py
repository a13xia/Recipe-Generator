import streamlit as st
import requests
import re

st.set_page_config(page_title="Recipe Generator", page_icon="🍴")

st.markdown(
    """
    <style>
    .stApp {
        background-image: url(https://media.istockphoto.com/id/1829241109/ro/fotografie/bucur%C3%A2ndu-ne-de-un-brunch-%C3%AEmpreun%C4%83.jpg?s=2048x2048&w=is&k=20&c=MTUQDUcwR3JmYe9S-dwQw9LT9MM54FyA6p9m_biyPQQ=);
        background-attachment: fixed;
        background-size: cover;
    }
    /* Add spacing above the first block */
    .main-container {
        margin-top: 40px; /* Space above the first block */
    }
    /* Add spacing between each recipe block */
    .recipe-container {
        margin-top: 30px; /* Space above each recipe */
        margin-bottom: 30px; /* Space below each recipe */
    }
    /* Add a rectangle background behind text */
    .text-container {
        background-color: rgba(255, 255, 255, 0.8); /* White with 80% opacity */
        border-radius: 10px; /* Rounded corners */
        padding: 15px; /* Padding inside the rectangle */
        margin-bottom: 10px; /* Space below each text block */
        color: black !important; /* Set text color to black */
    }
    /* Black text for headings, paragraphs, labels, and links */
    h1, h2, h3, h4, h5, h6, p, label, span, a {
        color: black !important; /* Override all text to black */
    }
    div.stButton > button {
        background-color: red;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
    }
    div.stButton > button:hover {
        background-color: darkred;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Recipe Generator")


def get_recipes(ingredients, diet, meal_type):  # Add meal_type here
    api_key = "f10473608231407ab7baca3f6f93d8a2"
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey": api_key,
        "query": ingredients,
        "diet": diet,
        "mealType": meal_type,
        "number": 20,
        "addRecipeInformation": True
    }

    response = requests.get(url, params=params)
    return response.json()


def is_url_valid(url):
    """Check if the URL is accessible."""
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False



def main():
    st.markdown(
        '<div class="main-container"><div class="text-container">Enter comma-separated ingredients (e.g. chicken, rice, broccoli):</div>',
        unsafe_allow_html=True)
    ingredients = st.text_input("Ingredients:", "", label_visibility="collapsed")

    st.markdown('<div class="text-container">Dietary restrictions:</div>', unsafe_allow_html=True)
    diet = st.selectbox("Select a dietary restriction:", ["None", "Vegetarian", "Vegan", "Gluten-Free"],
                        label_visibility="collapsed")

    st.markdown('<div class="text-container">Meal Type:</div>', unsafe_allow_html=True)
    meal_type = st.selectbox("Select a meal type:", ["Any", "Breakfast", "Lunch", "Dinner", "Snack"],
                             label_visibility="collapsed")

    if st.button("Find Recipes"):
        if ingredients:
            response = get_recipes(ingredients, diet, meal_type)
            # print(response)
            results = response.get("results", [])
            if not results:
                st.markdown('<div class="recipe-container text-container">No recipes found.</div>',
                            unsafe_allow_html=True)
            else:
                for recipe in results:
                    # Skip recipes without valid image or source URL
                    if (
                            "image" not in recipe or not recipe["image"] or
                            "sourceUrl" not in recipe or not is_url_valid(recipe["sourceUrl"])
                    ):
                        continue

                    st.markdown('<div class="recipe-container">', unsafe_allow_html=True)

                    st.markdown(f'<div class="text-container"><h3>{recipe["title"]}</h3></div>', unsafe_allow_html=True)

                    st.markdown(
                        f'<div class="text-container">Ready in {recipe["readyInMinutes"]} minutes</div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f'<div class="text-container">Servings: {recipe["servings"]}</div>',
                        unsafe_allow_html=True
                    )

                    st.image(recipe["image"], caption=recipe["title"], width=300)

                    st.markdown(
                        f'<div class="text-container">**Dietary Information:** {", ".join(recipe.get("diets", ["None"]))}</div>',
                        unsafe_allow_html=True
                    )

                    summary = recipe.get("summary", "")
                    if summary:
                        match = re.search(r"(\d+)\s*calories", summary)
                        if match:
                            calories = match.group(1)
                            st.markdown(f'<div class="text-container">**Calories per serving:** {calories} kcal</div>',
                                        unsafe_allow_html=True)

                    st.markdown(
                        f'<div class="text-container"><a href="{recipe["sourceUrl"]}" target="_blank">Link to Recipe</a></div>',
                        unsafe_allow_html=True
                    )
                    st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.markdown('<div class="recipe-container text-container">Enter at least one ingredient</div>',
                        unsafe_allow_html=True)


if __name__ == "__main__":
    main()
