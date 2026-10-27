# Module 1 Group Assignment

CSCI 5117, Fall 2026, [assignment description](https://canvas.umn.edu/courses/579310/pages/project-1)

## App Info:

* Team Name: Monkey the Five Leaf Clover
* App Name: Quilt
* App Link: [Link here!](https://developing-the-interactive-web-project-1-q9a7.onrender.com/)

### Students

* Aparmita Bajracharya, bajra020@umn.edu
* Diana Nguyen, nguy5285@umn.edu
* Grace Tang, tang0792@umn.edu
* Lindsey Oh, oh000155@umn.edu
* Sarah Peng, peng0471@umn.edu



## Key Features

**Describe the most challenging features you implemented
(one sentence per bullet, maximum 4 bullets):**

* We implemented Full Text search to achieve a more responsive search functionality than keyword search.
* We used HTMX's swapping feature to display search results in our "add connection" modal.
* We implemented infinite scrolling so that the landing page didn't load in all nodes at once.

## Testing Notes

**Is there anything special we need to know in order to effectively test your app? (optional):**

* When testing with Flask, use port 5000 or port 5001


## Screenshots of Site

**[Add a screenshot of each key page (around 4)](https://stackoverflow.com/questions/10189356/how-to-add-screenshot-to-readmes-in-github-repository)
along with a very brief caption:**

![](https://media.giphy.com/media/o0vwzuFwCGAFO/giphy.gif)

### Landing

> Non-account user only sees the "All Patches" and "Categories" tab.
> <img width="959" height="482" alt="image" src="https://github.com/user-attachments/assets/f67274b3-822a-4a9e-9838-317c884fddd2" />

> Account user sees all 4 tabs (here we are on "Categories" tab, scrolled down).
> <img width="959" height="476" alt="image" src="https://github.com/user-attachments/assets/b0b1a339-a329-4317-81ad-604f28056d59" />

> "Recently Viewed" tab, scrolled down. Shows the last couple of patches you visited.
> <img width="959" height="469" alt="image" src="https://github.com/user-attachments/assets/cfef2c78-fdfb-4131-a38c-453edba99685" />


> "New Connections" tab, scrolled to bottom. Shows patches that others have recently connected to your created or saved patches.
> <img width="959" height="471" alt="image" src="https://github.com/user-attachments/assets/c70c50f1-6100-42bf-8888-e146259cc003" />

### Search

> Results when searching "flower".
> <img width="959" height="471" alt="image" src="https://github.com/user-attachments/assets/c2cff8b1-7134-4b93-9f90-4134a96e96d5" />


### View node/patch
> View patch owned by yourself (has edit button).
><img width="959" height="477" alt="image" src="https://github.com/user-attachments/assets/e7e70895-e5df-4319-a693-f28d56a7fb1d" />

> Scroll down to view connections (owner has right to delete).
><img width="959" height="478" alt="image" src="https://github.com/user-attachments/assets/d3017085-2092-44e6-934a-c789eed0bf1a" />

> Saved unowned node.
> <img width="959" height="479" alt="image" src="https://github.com/user-attachments/assets/27347386-eed1-48ab-8711-27db8d8a3b0a" />

> Saved unowned node - view connections (can only delete connections if it connects to your own created node).
> <img width="959" height="476" alt="image" src="https://github.com/user-attachments/assets/ca6d2bf5-07d1-4bc2-bc7a-ef78f693b426" />


### Connect node/patch (pop-up)
> Add connection modal on open
> <img width="959" height="467" alt="image" src="https://github.com/user-attachments/assets/b7bc5862-4a74-4f2a-bac9-47a4020e6fdb" />

> Select some patches for connection
> <img width="959" height="476" alt="image" src="https://github.com/user-attachments/assets/61ddb188-3bed-4c46-a9fb-b112017484cb" />


### Edit node/patch
> Edit patch (has delete, cancel, save).
> <img width="959" height="472" alt="image" src="https://github.com/user-attachments/assets/94597701-7964-4852-b579-91b823bb96c0" />


### Create node/patch
> Fill in title, description, and img of patch form.
> <img width="959" height="473" alt="image" src="https://github.com/user-attachments/assets/63afb59b-4ede-4917-bf61-85218d37b42a" />

### Notifications
> Notifications show up for any new/deleted connections to your created nodes. You can delete the notification or disconnect the connection straight from the notification page.
> <img width="959" height="472" alt="image" src="https://github.com/user-attachments/assets/ae26ce5e-92ab-42be-8ea1-ae8556735cd9" />

### Profile (saved / created nodes/patches)
> Profile page, on saved patches tab.
> <img width="959" height="473" alt="image" src="https://github.com/user-attachments/assets/eb64f684-394e-41ad-af20-9736cbba41e1" />

> Profile page, on your created patches tab.
> <img width="955" height="473" alt="image" src="https://github.com/user-attachments/assets/60fda808-5756-4188-ad13-3cb97a879bde" />


> Edit profile page (cancel or save).
> <img width="959" height="470" alt="image" src="https://github.com/user-attachments/assets/b0b97fab-248d-43a3-b1ef-3256cb76c717" />

### Login
> Screen if user attempts to save node without logging in.
<img width="959" height="480" alt="image" src="https://github.com/user-attachments/assets/d9862082-78bc-49b8-bbef-92b4a6d10ec1" />


## Mock-up 

There are a few tools for mock-ups. Paper prototypes (low-tech, but effective and cheap), Digital picture edition software (gimp / photoshop / etc.), or dedicated tools like moqups.com (I'm calling out moqups here in particular since it seems to strike the best balance between "easy-to-use" and "wants your money" -- the free teir isn't perfect, but it should be sufficient for our needs with a little "creative layout" to get around the page-limit)

In this space please either provide images (around 4) showing your prototypes, OR, a link to an online hosted mock-up tool like moqups.com

**[Add images/photos that show your paper prototype (around 4)](https://stackoverflow.com/questions/10189356/how-to-add-screenshot-to-readmes-in-github-repository) along with a very brief caption:**

![](https://media.giphy.com/media/26ufnwz3wDUli7GU0/giphy.gif)

<img width="4096" height="4096" alt="New_board2_Copy" src="https://github.com/user-attachments/assets/27c5a2ca-d59b-4213-b0c6-89a87c86248a" />

**Pages**
* Login
* Sign Up 1
* Sign Up 2
* Landing (non-account user)
* Landing (account user)
  * Landing 2 (popular categories)
* Search
* View node
* Connect node (pop-up)
* Create node
* Edit node
* Notifications
* Profile (saved / created nodes)
* Settings


## External Dependencies

**Document integrations with 3rd Party code or services here.
Please do not document required libraries. or libraries that are mentioned in the product requirements**

* Library or service name: description of use
* HTMX: Used to display search results within the "add connection" modal without reloading the page. Also for infinite scroll.

**If there's anything else you would like to disclose about how your project
relied on external code, expertise, or anything else, please disclose that
here:**

...
