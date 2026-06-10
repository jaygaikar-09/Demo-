# Hackathon Git Workflow 🚀

Welcome to the project!

Please follow the steps below carefully.

---

# Step 1: Clone the Repository

```bash
git clone <repo-link>
```

Example:

```bash
git clone https://github.com/username/project.git
```

Move into project folder:

```bash
cd project-name
```

---

# Step 2: Create Your Own Branch

```bash
git checkout -b your-name
```

Example:

```bash
git checkout -b jay
```

---

# Step 3: Add Your Name in `main.py`

Open `main.py`

Add your name there.

Example:

```python
team_members = [
    "Jay",
    "Your Name"
]
```

Save the file.

---

# Step 4: Commit Your Changes

```bash
git add .
git commit -m "Added my name"
```

---

# Step 5: Push Your Branch

```bash
git push origin your-name
```

Example:

```bash
git push origin jay
```

---

# Step 6: Create Pull Request (PR)

* Open GitHub repository
* Click **Compare & Pull Request**
* Click **Create Pull Request**

Done ✅

---

# Important Rules ⚡

* Do NOT push directly to `main`
* Everyone should work on their own branch
* Pull latest changes before starting work

```bash
git pull origin main
```


