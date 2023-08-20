# Scope Test Dev Project

For Mac users new to Python, download the latest version here: https://www.python.org/ftp/python/3.11.4/python-3.11.4-macos11.pkg

Find the package in your downloads folder, double click it, and follow the instructions.

Once this is completed, open your Terminal application (located in your Applications folder), and you should be able to type
`python` and see this:

`Python 3.11.4 (main, Jul  3 2023, 16:14:57) [Clang 14.0.3 (clang-1403.0.22.14.1)] on darwin
Type "help", "copyright", "credits" or "license" for more information.`

If that does not work, there are lots of things that may have gone wrong. Please feel free to reach out to me at `amartin@thedevteam.dev` so I can help you.

Assuming that does work, type `ctrl + d` to exit Python and continue.

Download the code from your web browser here: https://github.com/agmartin/scope_test/archive/refs/heads/main.zip

If your Mac doesn't automatically unzip this package, you can unaip it yourself by simply double clicking it.

Move the unzipped folder to a place on your Mac where you like to work on things.

Navigate to the folder you just downloaded in your Terminal app. The easiest way to do this is by locating the folder in your Finder window, right-clicking on it and holding down the `option` key. You will see an option to copy ... as pathname. Select that.

Then go to your Terminal app and type `cd ` and paste the pathname and pressing enter. You are now in the working directory of the project.

We are going to create a virtual environment, which is a way of isolating code and dependencies for Python applications we are going to use, such as this one.

Type the following in your Terminal app: `python -m venv scopetest` and press enter.

You can then "activate" your virtual environment by typing `source ./scopetest/bin/activate` again, press enter.

You will probably need to get the latest version of pip installed. You can do this by typing `pip install --upgrade pip` and pressing enter.

This is a little like Thanos in the Avengers. We're using pip to upgrade pip. :)

We're almost there!

Now we're going to install the project dependencies so we can create reports.

type `pip install -r requirements.txt` and press enter. Once this is complete, we can run the program using this command:

`python main.py` and pressing enter. This will create a report called `test.pdf` in the report_pdfs folder that you can open using the Preview app or any other
pdf reader you choose.