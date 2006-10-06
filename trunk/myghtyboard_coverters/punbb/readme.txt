		Forum data dump generator for punBB 1.2

- This script will generate a python file with users/categories/forums/topics/posts data.
- The dump file will be in a django ORM "format"

HOW TO USE:
- put "django.php" in main punBB folder and open it in the browser. The file folder needs write access (or create install_1.py and add write access to this file)
- The script will generate the dump file
- move it to the main django project folder with working myghtyboard
- run it (python install_1.py)
NOTE: It will delete all users except first superuser (id 1)
