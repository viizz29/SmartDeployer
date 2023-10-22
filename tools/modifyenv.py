from pathlib import Path

def modify_env(address,mods):
        project_path = Path(address)
        if not project_path.is_dir():
                print("The specified path does not exist.")
                return False
        env_file_path = Path(address+'/.env.example')
        if not env_file_path.is_file():
                print("The specified folder is not a laravel project")
                return False

        records = []
        with env_file_path.open('r') as env_file:
                lines = env_file.readlines()
                for line in lines:
                        line = line.strip()
                        if len(line)>0:
                                data = line.split('=')
                                record = {'key':data[0].strip(),'value':data[1].strip()}
                                records.append(record)

        with env_file_path.open('w',newline='') as env_file:
                for record in records:
                        for mod in mods:
                                if mod['key'] == record['key']:
                                        record['value']=mod['value']
                                        break
                        env_file.write('%s=%s\n'%(record['key'],record['value']))
        env_file_path.rename(address+'/.env')
        print("The configuration has been generated successfully")
        return True

