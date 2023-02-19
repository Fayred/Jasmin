commands = (
    # change directory
    "cd", "pushd", "popd",
    # list files
    "ls", "dir", "echo *", 
    # editor
    "vim", "vi", "nano", "ed", "sed", "sudoedit", "tee",
    # reader
    "cat", "more", "less", "tail", "head", "hd", "hexdump", "xxd", "source", "base32", "base64", "md5sum", "sha1sum", "sha256sum", "sha512sum",
    # other about files
    "split", "wc", "find", "locate", "ln", "cp", "mv", "zip", "xz", "tar", "file",
    # about shell
    "set", "chsh", "sh", "bash", "ash", "csh", "zsh", "ksh", "fish",
    # client / network
    "curl", "wget", "ftp", "ssh", "scp", "nc", "netcat", "netstat", "ip", "ifconfig",
    # about permission
    "sudo", "chown", "chmod", "usermod", "adduser", "addgroup", "gpasswd", "passwd", "groups", "whoami", "id", 
    # about procs / jobs
    "ps", "top", "htop", "jobs", "fg", 
    # about ENV
    "export", "env", "pwd",
    # about binary
    "which", "whereis",
    # langages
    "python", "python3", "ruby", "perl", "php", "lua", "awk", 
    # about machine
    "uname", "hostname", "neofetch",
    # other
    "man", "nmap", "gdb", "git", "gcc", "g++",
)

from paramiko import SSHClient, AutoAddPolicy
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
import getpass
import argparse
from pathlib import Path


def get_active_commands(user, host, privatekey, port, verbose):
    if privatekey:
        privatekey_path = input("RSA private key path [~/.ssh/id_rsa]: ") or str(Path.home()) + "/.ssh/id_rsa"
    password = getpass.getpass("Password : ")

    console = Console()
    console.print(Panel.fit(
        f"[yellow]Hostname : {host}\nUsername : {user}\nPort : {port}[/yellow]\n\nEscape from restricted shells : [blue bold][link=https://0xffsec.com/handbook/shells/restricted-shells/]restricted-shells", 
        title="Jasmin"
    ))
    with SSHClient() as client:
        client.set_missing_host_key_policy(AutoAddPolicy())
        try:
            if privatekey:
                client.connect(host, username=user, password=password, port=port, key_filename=privatekey_path, timeout=3)
            else:
                client.connect(host, username=user, password=password, port=port, timeout=3)
        except Exception:
            console.print_exception()
            exit(-1)

        with Progress(console=console) as progress:
            task = progress.add_task("Fuzzing" , total=len(commands))
            for command in commands:
                stdin, stdout, stderr = client.exec_command(f"{command} --help")
                if not stderr.read():
                    console.print(f"[green][+] '{command}'")
                elif stderr.read() != "" and verbose:
                    console.print(f"[red][-] '{command}'")
                progress.update(task, advance=1, refresh=True)

def main():
    parser = argparse.ArgumentParser()
    required_args = parser.add_argument_group("required arguments")
    required_args.add_argument("--user", metavar="username", help="username", required=True)
    required_args.add_argument("--host", metavar="hostname", help="ip address or domain name", required=True)
    optional_args = parser.add_argument_group("optional arguments")
    optional_args.add_argument("--privatekey", action="store_true", help="connection established with your private key")
    optional_args.add_argument("-p", "--port", default=22, help="ssh to use port (default=22)")
    optional_args.add_argument("-v", "--verb", action="store_true", help="give each command tested (default=False)")
    args = parser.parse_args()

    get_active_commands(args.user, args.host, args.privatekey, args.port, args.verb)

if __name__ == "__main__":
    main()