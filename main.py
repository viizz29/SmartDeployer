from tools.env_reader import EnvReader
def main():
    env_reader = EnvReader(".env")

    print("Deployer 1.0")
    print("* This script deploys your project into a linux based system.")
    print("* For LAN access to the projects, you may need to allow the relevant ports through the firewall.")
    print("* For WAN access you need to enable the port as well as have public IP address")
    print()
    print("1. NodeJS + ReactJS + SqLite Deployer")
    print("2. Laravel Deployer")
    
    choice = int(input())
    if choice == 1:
        
        from scripts.nodejs_reactjs_sqlite_deployer import deploy
        deploy(env_reader.get("NODEJS_REACTJS_SQLITE_GITHUB_ACCOUNT_URL"),
               env_reader.get("NODEJS_REACTJS_SQLITE_PROJECT_NAME"),
               env_reader.get("NODEJS_REACTJS_SQLITE_PORT_NUMBER"),
               env_reader.get("NODEJS_REACTJS_SQLITE_DEPLOYMENT_LOCATION"),
               env_reader.get("NODEJS_REACTJS_SQLITE_TOKEN_KEY")
               )

    elif choice == 2:
        from scripts.laravel_mysql_gmail_deployer import deploy
        deploy(env_reader.get("LARAVEL_MYSQL_GMAIL_GITHUB_ACCOUNT_URL"),
               env_reader.get("LARAVEL_MYSQL_GMAIL_APP_NAME"),
               env_reader.get("LARAVEL_MYSQL_GMAIL_APP_URL"),
               env_reader.get("LARAVEL_MYSQL_GMAIL_DB_NAME"),
               env_reader.get("LARAVEL_MYSQL_GMAIL_DB_USER"),
               env_reader.get("LARAVEL_MYSQL_GMAIL_DB_PASSWORD"),
               env_reader.get("LARAVEL_MYSQL_GMAIL_MAIL_ID"),
               env_reader.get("LARAVEL_MYSQL_GMAIL_MAIL_PASS"),
               env_reader.get("LARAVEL_MYSQL_GMAIL_DATA_DIRECTORY"),
               env_reader.get("LARAVEL_MYSQL_GMAIL_DEPLOYMENT_LOCATION"))
    
if __name__ == "__main__":
    main()