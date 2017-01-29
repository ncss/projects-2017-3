# Find It!
NCSS 2017, Group 3 - _**the best group**_

*Find It!* : "A website that uses crowdsourcing to find out where to purchase products" (line taken from [this article on NCSS 2017](http://sydney.edu.au/engineering/news/2017/coding-for-kids-summer-school.shtml) cos it's a pretty neat summary :P)

See more about us and our site in this [video](https://www.youtube.com/watch?v=nrfOD1kIIOM) :)

---

## Running from source

Clone the repo:
```bash
$ git clone https://github.com/ncss/projects-2017-3/
```
Create the database:
```bash
python db/db_create.py
```

- Only clone the repository and create the database when running for first time.

Install requirements:
```bash
pip install -r requirements.txt
```

Start the server:
```bash
python server.py
```
The server runs by default at localhost:8888. (Type localhost:8888 into a browser to view)

---

## How to run *Find It!* with screenshots

Here is a version of how to run the project with screenshots — just to make it a tiny bit more approachable :). This how-to is made quickly for GitHub Desktop. (But of course you can go with whatever you like, this is just if you don't really have preferences, yet :))

- If you'd like to use [GitHub Desktop](https://desktop.github.com), click on the linked name to go download it. And then set it up.

- Then visit the link for our project: [GitHub projects 2017 group 3 link](https://github.com/ncss/projects-2017-3) and click on 'Clone or download'. Then click 'Open in Desktop' to open it in GitHub Desktop.
<br />
<img height="400" alt="Screenshot of 'Clone or download' NCSS group 3 project on GitHub" src="https://cloud.githubusercontent.com/assets/22441348/22179660/b2671018-e0ae-11e6-8df9-b70c499bd306.png">
<br />
You'll be prompted to choose a location to save the repository on your computer, and then the project will start cloning.

- Once the project has finished cloning, it will appear in the left panel under the heading 'GitHub' on GitHub Desktop. Then, Open in Terminal/Git Shell by right-clicking on the project name:
<br />
<img height="400" alt="Right click on project name with mouse hovering over 'Open in Terminal'" src="https://cloud.githubusercontent.com/assets/22441348/22178733/aafd91dc-e093-11e6-9b03-4091818ce586.png">
<br />
(The name of the option 'Open in Terminal/Git Shell' is just dependent on whichever Operating System you are using. These screenshots here are for Mac OS.)


In shell, if you want to run a Python file named `file.py` for example, you can type in `python db_create.py`once you're in the directory of the file.


- *Only if first time running*, we need to create the database (this also contains the dummy data). `python db/db_create.py` is the command to run the file that creates the database (on at least Windows I think).
Here is a screenshot (this is for Mac where `python3` is for running python3)
![Running python db/db_create.py in terminal](https://cloud.githubusercontent.com/assets/22441348/22178698/92192268-e092-11e6-85c2-2808e01170d2.png)

- Now, each time you want to run the project, you need the server. Run `python server.py`
![Running python server.py in terminal](https://cloud.githubusercontent.com/assets/22441348/22178746/052e2162-e094-11e6-897d-9f4f8d73b80d.png)
If it worked and the server's working, you'll see the `Reloading... waiting for requests on http://localhost:8888` message appear.

- After you have the server, open a browser and type in `localhost:8888` to see our awesome site :P
![Screenshot of website with localhost:8888 in the URL bar](https://cloud.githubusercontent.com/assets/22441348/22178763/9648a230-e094-11e6-8211-c199425f8397.png)
<br/>
Messages will keep appearing in the shell as you do things on the site, this is expected.

## How to open the project (in Atom), with screenshots
[Atom](https://atom.io) is a customisable text editor. You can use it to view and edit the files in our project. And of course you can use whatever else you like too if you have any preferences :)

- You can view code in Atom by going to Repository>Open in Atom on Mac, I think there's a button on Windows with the Atom icon.
Screenshot for Mac:
<br/>
<img alt="Screenshot of GitHub Desktop zoomed in on Repository, Open in Atom" src="https://cloud.githubusercontent.com/assets/22441348/22178790/1bd5092a-e095-11e6-87d7-0149e8e3d895.png">
<br/>
or you can also right-click on the project name and then Open in Atom:
<br/>
<img height="400" alt="Screenshot of GitHub Desktop zoomed in on right-click project name and mouse hover over 'Open in Atom'" src="https://cloud.githubusercontent.com/assets/22441348/22178779/eca7ffcc-e094-11e6-9062-ba5bab09b1a5.png">
<br/>

---
If you have any ideas or comments on this tutorial, please feel very free to add.

And if you're having trouble with anything, please tell us! :DD
