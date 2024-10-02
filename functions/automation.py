#!/usr/bin/python3

from subprocess import run,PIPE,call
def execute_shell_program(container , creation = "manual"):

    if container == "ubuntu":
        result = run(["sh","scripts/launch_ubuntu"] , stdout=PIPE, text=True)
        msg = "Ubuntu Container Up and Running"
    elif container == "nginx":
        result = run(["sh","scripts/launch_web_server"] , stdout=PIPE, text=True)
        msg = "Nginx Container Up and Running"
    elif creation == "auto":
        #command = f'scripts/launch_container.sh {container}'
        #result = run(command, shell=True, capture_output=True, text=True)
        result = run(["sh" , "scripts/launch_container.sh" , container] , stdout=PIPE , text=True) 

    else:
        print(f"{program} is not a valid shell program.")
    
    return result
