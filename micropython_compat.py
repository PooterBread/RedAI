"""
MicroPython Compatibility Layer for Udoo Key
Provides compatibility shims for MicroPython vs CPython differences
"""

import sys

# Detect if running on MicroPython
IS_MICROPYTHON = sys.implementation.name == 'micropython'

if IS_MICROPYTHON:
    # MicroPython-specific imports and implementations
    try:
        import urequests as requests
    except ImportError:
        requests = None
    
    # MicroPython doesn't have subprocess, so we'll use alternative methods
    def execute_command_micropython(command: str):
        """
        Execute command on MicroPython using available methods
        For Udoo Key, this might use network requests or hardware-specific APIs
        """
        # On MicroPython, we can use urequests for HTTP requests
        # For other commands, we might need to use hardware-specific APIs
        if command.startswith('curl') or 'http' in command.lower():
            # Parse curl-like commands and convert to urequests
            return _execute_http_request_micropython(command)
        else:
            # For other commands, return a message that manual execution is needed
            return {
                'success': False,
                'output': '',
                'error': f'Command execution not directly supported on MicroPython: {command}. Use network requests or hardware APIs.'
            }
    
    def _execute_http_request_micropython(command: str):
        """Convert curl commands to urequests calls"""
        if not requests:
            return {
                'success': False,
                'output': '',
                'error': 'urequests not available. Install with: upip install urequests'
            }
        
        # Simple curl parser (basic implementation)
        # This is a simplified version - full implementation would parse curl args
        try:
            if 'POST' in command:
                # Extract URL and data
                url_start = command.find('http')
                if url_start == -1:
                    return {'success': False, 'output': '', 'error': 'No URL found'}
                
                url_end = command.find(' ', url_start)
                if url_end == -1:
                    url_end = command.find("'", url_start)
                if url_end == -1:
                    url_end = command.find('"', url_start)
                
                url = command[url_start:url_end] if url_end != -1 else command[url_start:]
                
                # Extract data
                data_start = command.find('-d')
                if data_start != -1:
                    data_str = command[data_start+3:].strip().strip("'").strip('"')
                    # Simple parsing - in production, use proper parser
                    response = requests.post(url, data=data_str)
                else:
                    response = requests.post(url)
            else:
                # GET request
                url_start = command.find('http')
                if url_start == -1:
                    return {'success': False, 'output': '', 'error': 'No URL found'}
                
                url_end = command.find(' ', url_start)
                if url_end == -1:
                    url_end = command.find("'", url_start)
                if url_end == -1:
                    url_end = command.find('"', url_start)
                
                url = command[url_start:url_end] if url_end != -1 else command[url_start:]
                response = requests.get(url)
            
            return {
                'success': response.status_code < 400,
                'output': response.text if hasattr(response, 'text') else str(response.content),
                'error': None if response.status_code < 400 else f'HTTP {response.status_code}'
            }
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': str(e)
            }
    
    # Export the function
    execute_command = execute_command_micropython
    
else:
    # CPython - use standard subprocess (handled in exploit_executor)
    execute_command = None  # Will use subprocess in exploit_executor




