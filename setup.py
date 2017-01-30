import pip
import sys
try:
    argument = sys.argv[1].lower()
except:
    raise ValueError("setup.py requires either install or develop")
if argument == "develop" or argument == "install":
    def install():
        pip.main(['install', '-r', 'requirements.txt'])

    if __name__ == "__main__":
        install()