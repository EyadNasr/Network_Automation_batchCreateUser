import  time, paramiko, json, concurrent.futures, re
from jinja2 import Environment, FileSystemLoader

def invalid_password(password):
    # Check length
    if len(password) < 8 or len(password) > 128:
        return 1
    if re.search(r"[?\s]", password):
        return 2
    if not re.search(r"[0-9]+", password) or not re.search(r"[~!@#$%&*()\-_=+}{'\";:/.>,<\\|\[\]\^]+",password) or not\
            re.search(r'[A-Z]+',password) or not re.search(r'[a-z]+', password):
        return 3
    return 0

def invalid_username(username):
    # Check length
    if len(username) < 6 or len(username) > 253:
        return True
    if re.search(r"(^@)|(@$)|[/\\:*\"<>|'%?\s]", username):
        return True
    return False

delay = 5
def mainCode(remote):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if remote["host"] == "" or remote["username"] == "" or remote["password"] == "": return
    ssh.connect(hostname=remote["host"], port=22, username=remote["username"], password=remote["password"])
    shell = ssh.invoke_shell()
    shell.send('n\n')       #   escape the initial password security risk warning
    shell.send('screen-length 0 temporary\n')
    time.sleep(1)

    env = Environment(loader=FileSystemLoader('.'))
    temp = env.get_template("Create_user_VRP8.j2")
    with open("CreateUsers_inputs.json") as f:
        data = f.read()
        inputs = json.loads(data)
    commands = temp.render(config=inputs) + '\n'
    for user in inputs["users"]:
        if invalid_username(user["username"]):
            print(f"Error: the username \"{user['username']}\" is invalid. It must be 6-253 characters long and in form"
                  f" of 'user@domain'.\n It can not include invalid characters / \\ : * ? \" < > | @ ' %")
            raise SystemExit
        if invalid_password(user["password"]):
            if invalid_password(user["password"]) == 2:
                print(f"Error: The password \"{user['password']}\" for the username \"{user['username']}\" is invalid"
                      f".\n It must not contain '?' or spaces!")
            elif invalid_password(user["password"]) == 1:
                print(f"Error: The password \"{user['password']}\" for the username \"{user['username']}\" is invalid"
                      f".\n It must be 8-128 characters long")
            elif invalid_password(user["password"]) == 3:
                print(f"Error: The password \"{user['password']}\" for the username \"{user['username']}\" is too simple"
                      ".\n It must contain upper-case letters, lower-case letters, digits, and special characters.")
            raise SystemExit
    shell.send('sys\n')
    shell.send(commands)
    time.sleep(delay)
    output = shell.recv(999999).decode()
    print(output)

with open("Credentials.json") as f:
    data = f.read()
    credentials = json.loads(data)

num_threads = len(credentials)# multiprocessing.cpu_count()

# Create a thread pool executor with the desired number of threads
with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    # Submit the slow function to the thread pool executor for each piece of data
    futures = [executor.submit(mainCode, remote) for remote in credentials]
    # Wait for all the threads to complete
    results = [f.result() for f in futures]