from tools.modifyenv import modify_env
from os import system, chdir, getcwd
from sys import exit
from pathlib import Path


def deploy(self, github_account_url, 
           project_name,app_url, 
           db_name, db_user, db_pass, 
           gmail_id, mail_pass,
           data_directory,
           deployment_location):
    mods = [
            {'key':'APP_NAME','value':project_name},
            {'key':'APP_URL','value':app_url},
            {'key':'APP_ENV','value':'production'},
            {'key':'APP_DEBUG','value':'false'},
            {'key':'DB_DATABASE','value':db_name},
            {'key':'DB_USERNAME','value':db_user},
            {'key':'DB_PASSWORD','value':db_pass},
            {'key':'MAIL_MAILER','value':'smtp'},
            {'key':'MAIL_HOST','value':'smtp.gmail.com'},
            {'key':'MAIL_PORT','value':'587'},
            {'key':'MAIL_USERNAME','value':gmail_id},
            {'key':'MAIL_ENCRYPTION','value':'tls'},
            {'key':'MAIL_FROM_ADDRESS','value':gmail_id},
            {'key':'MAIL_PASSWORD','value':mail_pass},
            {'key':'DATA_DIRECTORY','value':data_directory},
            
            ]




    address = getcwd()
    
    project_address = "%s/%s"%(address,project_name)


    project_path = Path(project_address)
    if project_path.is_dir():
        system("rm -rf %s"%(project_name))

    if project_path.is_dir():
        print("Could not remove existing temp project.")
        print("Aborting...")
        return

    print("Cloning the repo ...")
    system("git clone "+github_account_url+"/"+project_name)
    git_data_path = Path("%s/.git"%(project_address))
    if not git_data_path.is_dir():
        print("Project clone unsuccessful!")
        print("Aborting ...")
        return


    if not modify_env(project_address,mods):
            print("Error in processing the env file.")
            return

    chdir(project_address)
    system("composer install --optimize-autoloader --no-dev")
    system("php artisan key:generate")

    system("composer install --optimize-autoloader --no-dev")

    system("php artisan migrate")
    system("php artisan auth:clear-resets")

    system("npm install --only=prod")
    system("npm run prod")


    dep_address = deployment_location

    dep_project_path = Path("%s/%s"%(dep_address,project_name))
    if dep_project_path.is_dir():
        #remove previously deployed project
        chdir(dep_address)
        command = "sudo rm -rf %s"%(project_name)
        print("Executing command: ",command)
        system(command)

    dep_project_address = "%s/%s"%(dep_address,project_name)
    
    #deploy current project
    command = "sudo mv %s %s"%(project_address,dep_project_address)
    print("Executing command: ",command)
    system(command)

    chdir(dep_project_address)

    print("creating cache ....")
    system("php artisan down")
    system("php artisan cache:clear")
    system("php artisan route:cache")
    system("php artisan config:cache")
    system("php artisan view:cache")
    system("php artisan up")


    command = 'sudo chown -R root:root %s/%s'%(dep_project_address,"storage")
    print(command)
    system(command)
    command = 'sudo chown -R root:root %s/%s'%(dep_project_address,"bootstrap/cache")
    print(command)
    system(command)
    command = "sudo chmod 777 -R %s/%s"%(dep_project_address,"storage")
    print(command)
    system(command)

    print("All set!!")


if __name__ == "__main__":
    deploy()