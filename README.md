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

- Contribution guidelines: \
  create a seprate branch on the feature you're working on and create a pullrequest
