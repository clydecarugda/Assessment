****Assessment Coding****

**Requirements**
- VSCode
- Python 3.10 or higher

**Instructions**
1. Open VSCode and install the following:
   - Python: Visit the website https://www.python.org and download the latest python
   - Git: Visit https://git-scm.com/ and download Git

2. Clone the repository
   - Open a terminal on your preffered folder and run "git clone https://github.com/clydecarugda/Assessment"
  
4. Create and activate a virtual environment
   - python3 venv venv **or** python -m venv
   - ./venv/Scripts/activate
  
5. Install dependencies
   - pip install -r requirements.txt
  
6. The files required for the code to run are
   - Root directory:
      - ./movies.csv (This file should be in the root folder)
   - datasets folder:
      - genre.json
      - writters.json
Note: These files should be present in their respective folder with the correct filename and type for the python script to run.

8. Run the script using a python debugger(F5 and select python debugger) or use the .exe file I created using PyInstaller for your convinience.

9. Wait for the script to finish processing the file.
   Note: If you're using the .exe file, a cmd window will open. Please note that the script is very basic does not have a GUI.

10. Once the script is done processing the file, a json file will be generated in the 'Output' folder and is always name 'output.json'.
