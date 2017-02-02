import pip
import sys
import os

try:
    argument = sys.argv[1].lower()
except:
    raise ValueError("setup.py requires either install or develop")
if argument == "develop" or argument == "install":
    def install():
        pip.main(['install', '-r', 'requirements.txt'])

        # make the database
        if not os.path.exists('db.db'):
            from subprocess import call
            try:
                call(["python", "db/db_create.py"])
            except:
                call(["python3", "db/db_create.py"])



    if __name__ == "__main__":
        install()