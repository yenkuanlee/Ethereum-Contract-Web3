import os
os.system("ipfs daemon &")
os.system("echo '{ \"Data\": \"Vote\" }' | ipfs object put")
os.system("ipfs pin add QmWvMxzFoKjUh4nF9Knf5XSYguVgzArzVZcsNXUJComLvD")
os.system("sudo /opt/tomcat7/bin/startup.sh")
