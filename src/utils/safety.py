import sys
from .logger import logger

def confirm_execution(action: str, target: str) -> bool:
    """
    Prompts the user for confirmation before executing a mutating action.
    """
    print(f"\n🛑 [STRICT SAFETY] You are about to: {action}")
    print(f"📍 Target: {target}")
    response = input("Do you approve this execution? (y/N): ").lower().strip()
    
    if response == 'y':
        logger.info(f"USER APPROVED: {action} on {target}")
        return True
    else:
        logger.warning(f"USER REJECTED: {action} on {target}")
        print("❌ Action aborted by user.")
        return False

def human_readable_summary(action: str, result: str, success: bool) -> str:
    """
    Generates a clear, human-readable summary of a command's result.
    """
    status = "✅ SUCCESS" if success else "❌ FAILED"
    return f"""
--- {action} SUMMARY ---
Status: {status}
Result:
{result}
-------------------------
"""

def sanitize_output(output: str) -> str:
    """
    Place-holder for secret scrubbing logic.
    """
    # Simple placeholder: remove potential GCP project IDs or generic keys
    return output
