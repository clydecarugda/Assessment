****Assessment Coding****

**Requirements**
- VSCode
- Python 3.10 or higher
- Git (for cloning the repository)

**Instructions**
1. Open VSCode and install the necessary softwares:
   - Python: Visit the website https://www.python.org and download the latest python
   - Git: Visit https://git-scm.com/ and download Git

2. Clone the repository
   - Open a terminal on your preffered project folder and run "git clone https://github.com/clydecarugda/Assessment"
  
4. Create and activate a virtual environment
   - python3 venv venv **or** python -m venv
   - ./venv/Scripts/activate
  
5. Install dependencies
   - pip install -r requirements.txt
  
6. Make sure that the following files are present in their corresponding folders for the script to run properly:
   - Root directory:
      - ./movies.csv (This file should be in the root folder)
   - datasets folder:
      - genre.json
      - writters.json
**Important:** The script won’t run if these files are missing or incorrectly placed.

8. Run the script using a python debugger(F5 and select python debugger) or use the .exe file I created using PyInstaller for your convinience.

9. Wait for the script to finish processing the file.
   Note: If you're using the .exe file, a cmd window will open. Please note that the script is very basic does not have a GUI. The window will close automatically once processing is done.

10. Once the script is done processing the file, a json file will be generated in the 'Output' folder and is always name 'output.json'.

Troubleshooting:
 - If you face any issues with virtual environment activation, make sure the terminal is opened in the correct folder where the venv folder is located.
 - If for some reason the script won't run or did not generate any file in the Output folder, please double check the required files if named correctly and they are in the correct locations.
