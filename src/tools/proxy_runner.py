import paramiko
from src.utils.logger import logger
from src.utils.safety import sanitize_output
from src.tools.shell_runner import CommandResult

def run_ssh_command(host: str, user: str, key_path: str, command: str) -> CommandResult:
    """
    Executes a command on a remote host via SSH.
    """
    logger.info(f"Executing remote command on {host}: {command}")
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(hostname=host, username=user, key_filename=key_path)
        stdin, stdout, stderr = client.exec_command(command)
        
        out_str = stdout.read().decode('utf-8')
        err_str = stderr.read().decode('utf-8')
        exit_status = stdout.channel.recv_exit_status()
        
        client.close()
        
        return CommandResult(
            stdout=sanitize_output(out_str),
            stderr=sanitize_output(err_str),
            returncode=exit_status,
            success=(exit_status == 0)
        )
        
    except Exception as e:
        logger.error(f"SSH execution failed: {e}")
        return CommandResult(stdout="", stderr=str(e), returncode=1, success=False)
