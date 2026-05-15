# actions/example_skill.py
"""
Example Skill/Tool Template for Jarvis

This file demonstrates how to create a new custom tool/skill for Jarvis.
Copy this file and modify it to create your own tools.

Required components:
1. TOOL_DECLARATION - Defines the tool for the AI
2. Main function with the same name as the tool (or use the _action suffix)
"""


# =============================================================================
# TOOL DECLARATION
# This tells the AI what the tool does and what parameters it needs
# =============================================================================

TOOL_DECLARATION = {
    "name": "example_skill",  # Must match the function name below
    "description": (
        "This is an example skill. Replace this description with what your tool does. "
        "Be clear about when to use this tool."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "param1": {
                "type": "STRING",
                "description": "Description of first parameter"
            },
            "param2": {
                "type": "INTEGER",
                "description": "Description of second parameter"
            },
            "optional_param": {
                "type": "STRING",
                "description": "Description of optional parameter"
            }
        },
        "required": ["param1"]  # List only required parameters
    }
}


# =============================================================================
# MAIN ACTION FUNCTION
# This function will be called when the AI decides to use this tool
# =============================================================================

def example_skill(parameters: dict, player=None, session_memory=None):
    """
    Example skill function.
    
    Args:
        parameters: Dictionary containing the parameters from the AI
        player: UI object for logging and speaking (optional)
        session_memory: Memory object for storing context (optional)
    
    Returns:
        str: Result message to return to the AI
    """
    
    # Extract parameters
    param1 = parameters.get("param1")
    param2 = parameters.get("param2", 0)  # Default value for optional params
    optional_param = parameters.get("optional_param")
    
    # Validate required parameters
    if not param1:
        msg = "Sir, param1 is required for this skill."
        _speak_and_log(msg, player)
        return msg
    
    # ======================================================================
    # YOUR CODE HERE
    # Implement your skill's logic here
    # ======================================================================
    
    result = f"Executed example_skill with param1={param1}, param2={param2}"
    
    if optional_param:
        result += f", optional={optional_param}"
    
    # Log and speak the result
    msg = f"Sir, {result}."
    _speak_and_log(msg, player)
    
    # Optionally store in session memory
    if session_memory:
        try:
            session_memory.set_last_search(
                query=f"example_skill {param1}",
                response=msg
            )
        except Exception:
            pass
    
    return msg


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def _speak_and_log(message: str, player=None):
    """Helper function to log and speak messages."""
    if player:
        try:
            player.write_log(f"JARVIS: {message}")
            # If you want to speak the message:
            # player.speak(message)
        except Exception:
            pass


# =============================================================================
# ALIAS FUNCTION (Optional)
# If your main function has a different name (e.g., example_action),
# create an alias that matches the tool name
# =============================================================================

# def example_action(parameters: dict, player=None, session_memory=None):
#     # Your implementation
#     return "Done"
# 
# # Alias to match tool name
# def example_skill(parameters: dict, player=None, session_memory=None):
#     return example_action(parameters, player, session_memory)
