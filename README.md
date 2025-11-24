SwadShaala – Intelligent Recipe & Cooking Platform 🍲✨
Welcome to SwadShaala, your next-generation web platform for smart home cooking and recipe mastery! SwadShaala blends culinary tradition with cutting-edge technology: structured recipe management, AI-driven cooking guidance, ingredient scaling, instant grocery planning, and a beautiful, intuitive UI for cooks of any level.

Project Overview 📘
SwadShaala harnesses the power of Django and MySQL to help everyone—students, beginners, food explorers—discover, learn, and prepare great food at home. Core modules simplify every part of the cooking journey, from recipe curation and stepwise guidance to meal planning, smart ingredient tips, and flexible shopping lists.
SwadShaala’s focus is on accessibility, smart automation, and making home cooking both easy and exciting.

Core Features 🛠️
Smart Recipe Management: Structure-rich recipes: media, types, utensils, calories, flame guidance, and stepwise instructions.

AI/NLP-Powered Beginner Guide: Get instant, easy explanations for tough steps, common warning tips, tooltips, and useful videos.

Adaptive Ingredient & Serving Scaler: Auto-calculate ingredient quantities for any serving size—ideal for solo or family meals.

Meal Type & Time Filtering: Tag/browse/search recipes by meal type, filter by prep/cook time and plan ahead with confidence.

Shopping List Generator: Build dynamic grocery lists from your selected recipes and export as PDF/CSV—ingredients grouped by category.

Utensil & Flame Guidance: Every step has utensil and flame info (low/med/high) for true beginner friendliness and cooking accuracy.

Ingredient Substitution & Health Mode: AI recommends healthy swaps for allergies, diets (vegan, gluten-free, etc), or out-of-stock items.

Recipe Discovery via Web Scraper: Trending recipes are scraped, cleaned, and suggested directly from the top food platforms online.

Role-Based Authentication: Secure personal dashboard for each user, with admin oversight for all content and community safety.

Modern, Responsive UI: Powered by Bootstrap, Animate.css, and thoughtful design for use on desktop, tablet, and mobile.

Why SwadShaala? 🌏
Too many cooks struggle with scaling, ingredient doubts, tool confusion, and meal planning chaos. SwadShaala transforms frustration into confidence—making every step visual, interactive, and safe. Whether you’re a student, a new chef, or a home cook wanting to level up, SwadShaala is truly your digital recipe mentor.

Technologies Used 🖥️
Screenshots 🖼️
Check the Screenshots folder for a visual tour:

Screenshots/Home_Page.jpg – Colorful, mobile-friendly landing page

Screenshots/User_Login.jpg – Secure registration and login

Screenshots/Recipe_List.jpg – Browse and filter recipes easily

Screenshots/Add_Recipe.jpg – Media-rich add recipe form

Screenshots/Admin_Dashboard.jpg – Powerful admin controls

Screenshots/Contact_Us.jpg – User help & support screen

(These images showcase SwadShaala's real UI—fast, friendly, and clear!)

Project Folders & Content
recipe_app/: All Django backend code, views, models, templates, and static files

media/: File uploads (recipe images, etc)

Screenshots/: Main UI screens for quick reference

diagrams/: Architecture, flowcharts, and UML diagrams

README.md: You’re reading it!

Stages Timeline 🗂️
Stage	What Was Done
Planning	Brainstormed modules, UI wireframes, feature set
Setup	Django/MySQL config, user auth, recipe model, base UI
Implementation	Stepwise dev: scaler, guides, scraper, export, security
Testing	Manual/automated tests for all major modules
Optimization	UI/UX polish, responsive design, field validation
Release	Uploaded project, screenshots, and docs to GitHub
Quick Start / Installation 🚀
Clone the repository:

bash
git clone https://github.com/vanshmachhi28/swadshaala-cooking-assistant.git
cd swadshaala-cooking-assistant
Install all requirements:

bash
pip install -r requirements.txt
Set up MySQL:

Create an empty database.

Edit settings.py with your credentials.

Migrate:

bash
python manage.py migrate
Load demo data (if provided) or create your own recipes via the web UI.

Run the server:

bash
python manage.py runserver
Visit: http://127.0.0.1:8000/

How to Use
Register or log in for your personal dashboard

Manage recipes, meal plans, and ingredient lists

Get AI-powered help and safety advice

Add to your cart and export shopping lists as PDFs/CSVs in one click

Enjoy a seamless, responsive user experience—with admin controls for reviewers

Contributing 🙌
Fork, branch, and submit pull requests for features or bugfixes

Issues and suggestions very welcome

License
This project is open source and free for educational/personal use.
See the LICENSE file for details.

Contact
Developed & maintained by Vansh Prakash Machhi
Feedback: machhivansh470@gmail.com

Cook smarter. Eat healthier. Try new things.
SwadShaala is your digital sous chef—let’s cook together!
