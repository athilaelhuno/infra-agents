import subprocess
from typing import NamedTuple, List, Optional
from src.utils.logger import logger
from src.utils.safety import sanitize_output

class CommandResult(NamedTuple):
    stdout: str
    stderr: str
    returncode: int
    success: bool

def run_command(args: List[str], cwd: Optional[str] = None, shell: bool = False) -> CommandResult:
    """
    Executes a shell command or process and returns a structured result.
    """
    logger.info(f"Executing command: {' '.join(args) if isinstance(args, list) else args}")
    
    try:
        # Use capture_output=True for Python 3.7+
        result = subprocess.run(
            args,
            cwd=cwd,
            shell=shell,
            capture_output=True,
            text=True,
            check=False
        )
        
        stdout = sanitize_output(result.stdout)
        stderr = sanitize_output(result.stderr)
        
        if result.returncode != 0:
            logger.error(f"Command failed with exit code {result.returncode}")
            if stderr:
                logger.error(f"Error output: {stderr.strip()}")
        
        return CommandResult(
            stdout=stdout,
            stderr=stderr,
            returncode=result.returncode,
            success=(result.returncode == 0)
        )
        
    except Exception as e:
        logger.exception(f"Exception occurred while running command: {e}")
        return CommandResult(
            stdout="",
            stderr=str(e),
            returncode=1,
            success=False
        )
