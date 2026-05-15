"""
Dynamic Tool/Skill Loader for Jarvis

This module provides an interface to dynamically import and register tools/skills
from the actions directory or external sources.

Usage:
    - Place your custom action files in the 'actions' directory
    - Each action file should export a function with the same name as the file
    - The tool declaration should be defined in the file as TOOL_DECLARATION
    - Call load_all_tools() to automatically discover and register all tools
"""

import importlib
import importlib.util
import sys
from pathlib import Path
from typing import Dict, List, Any, Callable, Optional


class ToolLoader:
    """Dynamic tool loader for Jarvis actions/skills."""
    
    def __init__(self, actions_dir: Optional[Path] = None):
        """
        Initialize the tool loader.
        
        Args:
            actions_dir: Path to the actions directory. Defaults to ../actions
        """
        if actions_dir is None:
            actions_dir = Path(__file__).parent.parent / "actions"
        self.actions_dir = actions_dir
        self.loaded_tools: Dict[str, dict] = {}
        self.loaded_functions: Dict[str, Callable] = {}
        self.tool_declarations: List[dict] = []
    
    def discover_action_files(self) -> List[Path]:
        """
        Discover all Python action files in the actions directory.
        
        Returns:
            List of paths to action files (excluding __init__.py and tool_loader.py)
        """
        if not self.actions_dir.exists():
            print(f"[ToolLoader] ⚠️ Actions directory not found: {self.actions_dir}")
            return []
        
        action_files = []
        for file_path in self.actions_dir.glob("*.py"):
            # Skip special files
            if file_path.name in ("__init__.py", "tool_loader.py"):
                continue
            # Skip files that start with underscore (private/internal)
            if file_path.name.startswith("_"):
                continue
            action_files.append(file_path)
        
        return sorted(action_files)
    
    def load_action_module(self, file_path: Path) -> Optional[object]:
        """
        Load a single action module from file path.
        
        Args:
            file_path: Path to the action file
            
        Returns:
            Loaded module object or None if loading failed
        """
        module_name = f"actions.{file_path.stem}"
        
        try:
            # Check if module is already loaded
            if module_name in sys.modules:
                module = sys.modules[module_name]
                print(f"[ToolLoader] ♻️  Reloaded existing module: {module_name}")
            else:
                # Load the module dynamically
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                if spec is None or spec.loader is None:
                    print(f"[ToolLoader] ❌ Failed to load spec: {file_path}")
                    return None
                
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                print(f"[ToolLoader] ✅ Loaded module: {module_name}")
            
            return module
            
        except Exception as e:
            print(f"[ToolLoader] ❌ Error loading {file_path.name}: {e}")
            return None
    
    def extract_tool_declaration(self, module: object, module_name: str) -> Optional[dict]:
        """
        Extract tool declaration from a loaded module.
        
        Args:
            module: Loaded module object
            module_name: Name of the module
            
        Returns:
            Tool declaration dict or None if not found
        """
        # Look for TOOL_DECLARATION constant
        if hasattr(module, "TOOL_DECLARATION"):
            declaration = module.TOOL_DECLARATION
            if isinstance(declaration, dict) and "name" in declaration:
                return declaration
        
        # Look for tool_name_DECLARATION pattern
        base_name = module_name.split(".")[-1]
        decl_attr_name = f"{base_name.upper()}_DECLARATION"
        if hasattr(module, decl_attr_name):
            declaration = getattr(module, decl_attr_name)
            if isinstance(declaration, dict) and "name" in declaration:
                return declaration
        
        return None
    
    def extract_action_function(self, module: object, module_name: str) -> Optional[Callable]:
        """
        Extract the main action function from a loaded module.
        
        Args:
            module: Loaded module object
            module_name: Name of the module
            
        Returns:
            Action function or None if not found
        """
        base_name = module_name.split(".")[-1]
        
        # Try common function names
        possible_names = [
            base_name,
            f"{base_name}_action",
            "execute",
            "run",
            "action",
        ]
        
        for func_name in possible_names:
            if hasattr(module, func_name):
                func = getattr(module, func_name)
                if callable(func):
                    return func
        
        return None
    
    def load_single_tool(self, file_path: Path) -> bool:
        """
        Load a single tool from file.
        
        Args:
            file_path: Path to the action file
            
        Returns:
            True if successfully loaded, False otherwise
        """
        module = self.load_action_module(file_path)
        if module is None:
            return False
        
        module_name = f"actions.{file_path.stem}"
        
        # Extract tool declaration
        declaration = self.extract_tool_declaration(module, module_name)
        if declaration is None:
            print(f"[ToolLoader] ⚠️  No TOOL_DECLARATION found in {file_path.name}")
            return False
        
        # Extract action function
        action_func = self.extract_action_function(module, module_name)
        if action_func is None:
            print(f"[ToolLoader] ⚠️  No action function found in {file_path.name}")
            return False
        
        tool_name = declaration["name"]
        
        # Store the tool
        self.loaded_tools[tool_name] = {
            "declaration": declaration,
            "function": action_func,
            "module": module,
            "file": file_path,
        }
        
        self.loaded_functions[tool_name] = action_func
        
        # Add to declarations list if not already present
        if not any(d.get("name") == tool_name for d in self.tool_declarations):
            self.tool_declarations.append(declaration)
        
        print(f"[ToolLoader] ✅ Registered tool: {tool_name}")
        return True
    
    def load_all_tools(self) -> int:
        """
        Load all tools from the actions directory.
        
        Returns:
            Number of successfully loaded tools
        """
        action_files = self.discover_action_files()
        loaded_count = 0
        
        print(f"[ToolLoader] 🔍 Found {len(action_files)} action files")
        
        for file_path in action_files:
            if self.load_single_tool(file_path):
                loaded_count += 1
        
        print(f"[ToolLoader] ✅ Loaded {loaded_count} tools")
        return loaded_count
    
    def reload_tool(self, tool_name: str) -> bool:
        """
        Reload a specific tool.
        
        Args:
            tool_name: Name of the tool to reload
            
        Returns:
            True if successfully reloaded, False otherwise
        """
        if tool_name not in self.loaded_tools:
            print(f"[ToolLoader] ❌ Tool not found: {tool_name}")
            return False
        
        tool_info = self.loaded_tools[tool_name]
        file_path = tool_info["file"]
        
        # Remove from cache
        module_name = f"actions.{file_path.stem}"
        if module_name in sys.modules:
            del sys.modules[module_name]
        
        # Reload
        return self.load_single_tool(file_path)
    
    def reload_all_tools(self) -> int:
        """
        Reload all tools.
        
        Returns:
            Number of successfully reloaded tools
        """
        # Clear current state
        self.loaded_tools.clear()
        self.loaded_functions.clear()
        self.tool_declarations.clear()
        
        return self.load_all_tools()
    
    def get_tool_function(self, tool_name: str) -> Optional[Callable]:
        """
        Get the function for a specific tool.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            Tool function or None if not found
        """
        return self.loaded_functions.get(tool_name)
    
    def get_all_declarations(self) -> List[dict]:
        """
        Get all tool declarations for the API.
        
        Returns:
            List of tool declarations
        """
        return self.tool_declarations.copy()
    
    def import_external_tool(self, file_path: Path) -> bool:
        """
        Import a tool from an external file path.
        
        Args:
            file_path: Path to the external action file
            
        Returns:
            True if successfully imported, False otherwise
        """
        if not file_path.exists():
            print(f"[ToolLoader] ❌ File not found: {file_path}")
            return False
        
        return self.load_single_tool(file_path)


# Global instance for convenience
_default_loader: Optional[ToolLoader] = None


def get_tool_loader(actions_dir: Optional[Path] = None) -> ToolLoader:
    """
    Get or create the default tool loader instance.
    
    Args:
        actions_dir: Optional path to actions directory
        
    Returns:
        ToolLoader instance
    """
    global _default_loader
    if _default_loader is None:
        _default_loader = ToolLoader(actions_dir)
    return _default_loader


def load_all_tools(actions_dir: Optional[Path] = None) -> tuple[List[dict], Dict[str, Callable]]:
    """
    Convenience function to load all tools and return declarations and functions.
    
    Args:
        actions_dir: Optional path to actions directory
        
    Returns:
        Tuple of (tool_declarations, tool_functions)
    """
    loader = get_tool_loader(actions_dir)
    loader.load_all_tools()
    return loader.get_all_declarations(), loader.loaded_functions


if __name__ == "__main__":
    # Test the loader
    print("=" * 60)
    print("Testing ToolLoader")
    print("=" * 60)
    
    loader = ToolLoader()
    count = loader.load_all_tools()
    
    print(f"\nLoaded {count} tools:")
    for name, info in loader.loaded_tools.items():
        print(f"  - {name}: {info['file'].name}")
    
    print(f"\nTool declarations: {len(loader.tool_declarations)}")
