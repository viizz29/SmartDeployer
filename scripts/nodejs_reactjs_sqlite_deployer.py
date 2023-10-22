from tools.modifyenv import modify_env
from os import system, chdir, getcwd
from sys import exit
from pathlib import Path



def deploy(github_account_url, project_name, port_number, token_key, deployment_location):
    print("Node JS + React JS Deployer V 1.0")    
    print("Make sure you have node, npm, npx installed in your system.")
    print()
    print("The script assumes the following project structure: ")
    print("Project")
    print("|")
    print("|----server")
    print("|")
    print("|----client")
    print("|")
    print("|----sqlite.db")
    print()
    print("The project will be fetched from the github repository and deployed.")
    
    app_repository = github_account_url+"/"+project_name+".git"


    mods = [
         {'key':'API_PORT','value':port_number},
         {'key':'TOKEN_KEY','value':token_key},
         ]
    

    address = getcwd()
    chdir(address)
    project_address = "%s/%s"%(address,project_name)
    
    project_path = Path(project_address)
    if project_path.is_dir():
        confirm = 'y'#input('The project ("%s") already exists at "%s" press y/Y to delete it: '%(project_name,address)).lower()
        if confirm!='y':
                print("Aborting ....")
                return
        system("rm -rf %s"%(project_name))

    if project_path.is_dir():
        print("Could not remove the project.")
        print("Aborting...")
        return


    print("Cloning %s ..."%project_name)
    system("git clone "+app_repository)
    git_data_path = Path("%s/.git"%(project_address))
    if not git_data_path.is_dir():
        print("Project clone unsuccessful!")
        print("Aborting ...")
        return
    
    print("modifying the .env file")
    server_component_address = project_address +"/server"
    if not modify_env(server_component_address,mods):
        print("Error in processing the env file.")
        return
    
    print("Installing server component dependencies ..")
    chdir(server_component_address)
    system("npm install --omit=dev")

    print("Building client ...")
    client_component_address = project_address + "/client"
    chdir(client_component_address)
    system("npm install --omit=dev")
    system("npm run build")
    system("rm -rf node_modules")

    
    input("Please make sure that the app is not running ... and then press any key")

    print("Copying the existing database ..")
    chdir(project_address)
    deployed_project_address = deployment_location + "/" + project_name
    sqlite_db_address = deployed_project_address + "/sqlite.db"
    sqlite_db_path = Path(sqlite_db_address)
    if(sqlite_db_path.is_file()):
         system("cp "+sqlite_db_address+ " ./")

    print("Removing the previously deployed application ...")
    system("rm -rf "+deployed_project_address)

    print("Deploying ...")
    system("cd ..")
    system("mv "+project_address + " " + deployment_location + "/")

    print("Running migrations ...")
    chdir(deployed_project_address + "/server")
    system("npx sequelize-cli db:migrate")

    print("All set !")



if __name__ == "__main__":
      deploy()
                    