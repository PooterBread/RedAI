#!/usr/bin/env python3
"""
RedAI - AI-Powered Penetration Testing Tool
Compatible with Udoo Key (RP2040/ESP32)

Main entry point for the application
"""

import sys
import argparse
import logging
from typing import Optional, Dict
from database import ExploitDatabase
from ai_engine import AIEngine
from exploit_executor import ExploitExecutor
from config import LOG_LEVEL

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class RedAI:
    """Main RedAI application class"""
    
    def __init__(self):
        self.db = ExploitDatabase()
        self.ai = AIEngine()
        self.executor = ExploitExecutor()
        logger.info("RedAI initialized")
    
    def run_interactive(self):
        """Run interactive mode"""
        print("\n" + "="*60)
        print("RedAI - AI-Powered Penetration Testing Tool")
        print("Compatible with Udoo Key (RP2040/ESP32)")
        print("="*60)
        print("\n⚠️  EDUCATIONAL USE ONLY - Authorized Testing Only\n")
        
        while True:
            try:
                print("\nOptions:")
                print("1. Run penetration test (enter target/goal)")
                print("2. View exploit database")
                print("3. Add manual exploit")
                print("4. View execution history")
                print("5. Exit")
                
                choice = input("\nSelect option (1-5): ").strip()
                
                if choice == '1':
                    self.run_pen_test()
                elif choice == '2':
                    self.view_exploits()
                elif choice == '3':
                    self.add_manual_exploit()
                elif choice == '4':
                    self.view_history()
                elif choice == '5':
                    print("\nExiting RedAI. Stay ethical!")
                    break
                else:
                    print("Invalid option. Please try again.")
            
            except KeyboardInterrupt:
                print("\n\nInterrupted by user. Exiting...")
                break
            except Exception as e:
                logger.error(f"Error in interactive mode: {str(e)}")
                print(f"\nError: {str(e)}")
    
    def run_pen_test(self):
        """Run penetration test based on user prompt"""
        print("\n" + "-"*60)
        print("PENETRATION TEST CONFIGURATION")
        print("-"*60)
        
        target = input("Enter target system/URL: ").strip()
        goal = input("Enter testing goal (e.g., 'capture flag', 'test authentication'): ").strip()
        
        if not target or not goal:
            print("Error: Target and goal are required")
            return
        
        print(f"\nAnalyzing target: {target}")
        print(f"Goal: {goal}")
        print("\nSearching exploit database and consulting AI...")
        
        # Get all available exploits
        all_exploits = self.db.get_all_exploits()
        
        # Use AI to analyze and select/generate exploit
        try:
            analysis = self.ai.analyze_target(goal, all_exploits)
            print(f"\nAI Analysis: {analysis.get('reasoning', 'N/A')}")
            
            if analysis.get('action') == 'use_existing':
                exploit_id = analysis.get('exploit_id')
                if exploit_id:
                    exploit = self.db.get_exploit_with_methods(exploit_id)
                    if exploit:
                        print(f"\n✓ Found matching exploit: {exploit['name']}")
                        self._execute_exploit_flow(exploit, target)
                    else:
                        print(f"\n✗ Exploit ID {exploit_id} not found")
                else:
                    print("\n✗ No exploit ID provided by AI")
            
            elif analysis.get('action') == 'generate_new':
                print("\n⚠ No matching exploit found. Generating new exploit method...")
                generation_prompt = analysis.get('generation_prompt', goal)
                
                new_exploit = self.ai.generate_new_exploit(target, generation_prompt)
                
                print(f"\n✓ Generated new exploit: {new_exploit.get('name', 'Unnamed')}")
                
                # Save to database
                exploit_id = self.db.add_exploit(
                    name=new_exploit.get('name', 'AI Generated Exploit'),
                    description=new_exploit.get('description', ''),
                    target_type=new_exploit.get('target_type', 'unknown'),
                    target_component=new_exploit.get('target_component', 'unknown'),
                    method_summary=new_exploit.get('method_summary', ''),
                    difficulty=new_exploit.get('difficulty', 'medium'),
                    tools_required=new_exploit.get('tools_required', [])
                )
                
                # Add method steps
                steps = new_exploit.get('steps', [])
                if steps:
                    self.db.add_method_steps(exploit_id, steps)
                
                # Get full exploit and execute
                exploit = self.db.get_exploit_with_methods(exploit_id)
                if exploit:
                    self._execute_exploit_flow(exploit, target)
        
        except Exception as e:
            logger.error(f"Error in pen test: {str(e)}")
            print(f"\n✗ Error: {str(e)}")
    
    def _execute_exploit_flow(self, exploit: Dict, target: str):
        """Execute exploit and record results"""
        print("\n" + "-"*60)
        print("EXPLOIT EXECUTION")
        print("-"*60)
        
        # Validate exploit
        is_valid, message = self.executor.validate_exploit(exploit)
        if not is_valid:
            print(f"✗ Exploit validation failed: {message}")
            return
        
        # Execute
        import time
        start_time = time.time()
        success, output = self.executor.execute_exploit(exploit, target)
        execution_time = time.time() - start_time
        
        # Record results
        self.db.record_execution(
            exploit_id=exploit['id'],
            target=target,
            success=success,
            output=output,
            execution_time=execution_time
        )
        
        # Display results
        print("\n" + "="*60)
        print("EXECUTION RESULTS")
        print("="*60)
        print(f"Status: {'✓ SUCCESS' if success else '✗ FAILED'}")
        print(f"Execution Time: {execution_time:.2f}s")
        print(f"\nOutput:\n{output}")
        print("="*60)
    
    def view_exploits(self):
        """View all exploits in database"""
        exploits = self.db.get_all_exploits()
        
        print("\n" + "="*60)
        print(f"EXPLOIT DATABASE ({len(exploits)} exploits)")
        print("="*60)
        
        if not exploits:
            print("No exploits in database.")
            return
        
        for exp in exploits:
            print(f"\nID: {exp['id']}")
            print(f"Name: {exp['name']}")
            print(f"Target: {exp['target_component']} ({exp['target_type']})")
            print(f"Description: {exp['description']}")
            print(f"Difficulty: {exp['difficulty']}")
            print(f"Success Rate: {exp['success_rate']}")
            print("-" * 60)
    
    def add_manual_exploit(self):
        """Manually add an exploit to the database"""
        print("\n" + "-"*60)
        print("ADD MANUAL EXPLOIT")
        print("-"*60)
        
        name = input("Exploit name: ").strip()
        description = input("Description: ").strip()
        target_type = input("Target type (web_app/network/api/iot): ").strip()
        target_component = input("Target component: ").strip()
        method_summary = input("Method summary: ").strip()
        difficulty = input("Difficulty (easy/medium/hard): ").strip() or "medium"
        
        exploit_id = self.db.add_exploit(
            name=name,
            description=description,
            target_type=target_type,
            target_component=target_component,
            method_summary=method_summary,
            difficulty=difficulty
        )
        
        print(f"\n✓ Exploit added with ID: {exploit_id}")
        print("You can add method steps later or use the AI to generate them.")
    
    def view_history(self):
        """View execution history"""
        # This would query execution_results table
        print("\nExecution history feature - to be implemented")
        print("(Check database/exploits.db for execution_results table)")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="RedAI - AI-Powered Penetration Testing Tool"
    )
    parser.add_argument(
        '--target',
        help='Target system/URL (for non-interactive mode)'
    )
    parser.add_argument(
        '--goal',
        help='Testing goal (for non-interactive mode)'
    )
    parser.add_argument(
        '--auto-confirm',
        action='store_true',
        help='Skip confirmation prompts (use with caution)'
    )
    
    args = parser.parse_args()
    
    app = RedAI()
    
    if args.target and args.goal:
        # Non-interactive mode
        app.run_pen_test()
    else:
        # Interactive mode
        app.run_interactive()

if __name__ == "__main__":
    main()

