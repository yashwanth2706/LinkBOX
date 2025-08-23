# LinkBOX  

**LinkBOX** is a simple and efficient **URL Manager** designed to help users save, organize, and manage their web links in one place. It provides features like categorization, tagging, search, and filtering, making it easier to keep track of important websites without cluttering your browser bookmarks.  

## ✨ Features  

- 📌 Save and manage unlimited URLs  
- 🏷️ Categorize and sub-categorize links for easy organization  
- 🔍 Powerful search and filter options (by tag, category, subcategory)
- 📊 Track number of saved/trashed links 
- 📑 Export saved URLs to **CSV, PDF**
- ✏️ Edit options to update saved links anytime
- 🖼️ Live site preview for quick access  
- ♻️ Trash/Recycle Bin with **restore** and **delete options**  
- 📱 Responsive UI built with **Bootstrap**  
- ⚡ Backend powered by **Django**  

## 🛠️ Tech Stack  

- **Backend**: Django (Python)  
- **Frontend**: HTML, CSS, JavaScript, Bootstrap  
- **Database**: PostgreSQL (or SQLite for development)  

## Installation instructions:
Assuming You have git installed in your system:

- Create a Folder: \
  `mkdir LinkManager` \
  `cd LinkManager` 

- Clone the repo: \
  `git clone https://github.com/yashwanth2706/LinkBOX.git`
  `cd LinkBOX`

- Linux/MacOS: \
  In Terminal run below command 
  
  To create a virtual envirornment \
  `python3 -m venv .venv` 
  
  To activate the virtual envirornment \
  `source .venv/bin/activate`

- Windows: \
 In CMD run below command to set execution policy to current user \
  `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` 
  
 Create a virtual envirornment with below command \
  `python -m venv .venv` 
  
  To activate the virtual envirornment \
  `. .venv\Scripts\activate` \
  OR \
  `. YOUR_VITUAL_ENVIRORNMENT_NAME\Scripts\activate`

- Install dependencies and run the project \
  `pip install -r requirements.txt` 
  
  Linux/MacOS: \
  `python3 manage.py makemigrations` \
  `python3 manage.py migrate` \
  `python3 manage.py runserver` 
  
  Windows: \
  `python manage.py makemigrations` \
  `python manage.py migrate` \
  `python manage.py runserver`
  
- Open the project in webrowser: \
  `http://127.0.0.1:8000`

## 🤝 Contributing
Contributions, issues, and feature requests are welcome!
Feel free to open an issue or submit a pull request.

## 📜 License
This project is licensed under the MIT License.

