## LinkBOX – Modern URL Manager

A sleek and intuitive URL manager designed to help professionals save, organize, and retrieve web links effortlessly. With features like **categorization**, **tagging**, **search**, and **filtering**, it transforms link management into a streamlined, clutter-free experience ([github.com](https://github.com/yashwanth2706/LinkBOX)).

---

### 🎥 Project Walkthrough
[![Project Demo](https://github.com/yashwanth2706/LinkBOX/raw/main/walkthrough/project_thumb.png)](https://raw.githubusercontent.com/yashwanth2706/LinkBOX/main/walkthrough/project.mp4)

### Table of Contents

* [Why Use LinkBOX](#why-use-linkbox)
* [Key Features](#key-features)
* [Who’s It For?](#whos-it-for)
* [Getting Started](#getting-started)
* [Usage Examples](#usage-examples)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [Support & Contact](#support--contact)
* [License](#license)

---

### Why Use LinkBOX

* **Boost productivity** by centralizing and organizing essential web resources across projects or teams.
* **Save time** with fast filtering and search capabilities - say goodbye to digging through browser bookmarks.
* **Stay organized** using tags and categories to structure content for easy retrieval.
* **Enhance collaboration** by sharing curated link collections with colleagues or clients.

---

### Key Features

* **Easy Link Management**: Add, edit, delete, and store links with metadata.
* **Tagging & Categorization**: Organize links by theme, project, importance, or any custom schema.
* **Search & Filters**: Retrieve links instantly via tags, date, category, or search terms.
* **Clean Interface**: Professional-looking, user-friendly design suited for business environments.
* **Error Handling**: Built-in error popups notify users if something goes wrong
* **Trash Bin**: Every URL deleted will be a soft delete and can be retrived with in 30days or Empty trash bin in one click
* **Export - CSV/JSON/PDF/HTML**: Supports selective export or export all to your preffered file format and sharewith your friends,colleagues or clients
* **Import - CSV/JSON**: Import all URLs with CSV or JSON
* **Activity** - Track number of URLs stored/ trashed
* **Performance** - Targted DOM update for trashed urls preventing fullpage reload, pagination with option to select the number of rows to view
* **Selective: Deletion/Reverts/Exports** - User can select urls to delete, revert deleted urls from trash and export 

---

### Who’s It For?
* **Everyone** : )
* **Educators & Students** — build structured repositories of learning resources, references, or academic research.
* **Software Engineers** - manage reference materials, documentation, or snippets.
* **Product Managers / Designers** - centralize design inspirations, competitor analytics, or benchmark sites.
* **Content Teams / Researchers** - consolidate articles, sources, and tools for easy access.
* **Marketing / Sales Professionals** - organize campaigns, competitive content, or sales collateral.

---

### Getting Started

#### Prerequisites

* Ensure you have `git` installed in your system

#### Installation 

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

#### Configuration

Update settings such as database connections, authentication configs, or environment variables as required.
Current settings comes with the default SQLite can be configured with other databases like PostgresSQL

#### Launch

```bash
python manage.py runserver
```

Open in your browser at `http://localhost:8000` (or appropriate URL).

---

### Usage Examples

* **Add a new link**: Click "Add Link," fill in the URL, title, tags, and category.
* **Organize**: Apply tags like “Design,” “Docs,” or “Inspiration.”
* **Search effortlessly**: Type a query or choose filters—LinkBOX instantly retrieves relevant links.
* **Manage your collection**: Edit or remove links as needed through a clean, intuitive interface.

---

### Roadmap

* [ ] React Implementation
* [ ] User Links Analytics (Most visited, Most Links stored under same domain name, recently visited, ...etc)
* [ ] Syncing with browser bookmarks
* [ ] Bulk import/export in JSON
* [ ] Link collections/ groups
* [ ] Browser extension for quick link capture
* [ ] Backup and restore functionality

---

### Contributing

Contributions are welcome! To get involved:

1. Fork the repository
2. Create a descriptive branch (`feature/ui-improvement`, `fix/search-bug`)
3. Submit a pull request—include your reasoned changes
4. Support via issue reports, feature proposals, or code reviews

---

### Support & Contact

Need help or want to contribute?

* Open an issue on GitHub
* Connect via \[GitHub Discussions] or email at **\[[yash1anth.official@gmail.com](mailto:yash1anth.official@gmail.com)]**

---

### License

MIT license





