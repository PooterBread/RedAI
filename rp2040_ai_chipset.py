#!/usr/bin/env python3
"""
RP2040 AI Chipset Module
Handles AI logic, database operations, and decision-making
Communicates with ESP32 execution chipset via UART
"""

import sys
import time
import json
from typing import Dict, Optional

# Import core modules
from database import ExploitDatabase
from ai_engine import AIEngine
from chipset_communication import ChipsetCommunication
from config import LOG_LEVEL

# MicroPython compatibility
IS_MICROPYTHON = sys.implementation.name == 'micropython'

if not IS_MICROPYTHON:
    import logging
    logging.basicConfig(level=getattr(logging, LOG_LEVEL))
    logger = logging.getLogger(__name__)
else:
    logger = None
    def log_info(msg): print(f"[AI] {msg}")
    def log_error(msg): print(f"[AI ERROR] {msg}")

class RP2040AIChipset:
    """RP2040 AI Chipset - Handles AI logic and decision-making"""
    
    def __init__(self):
        """Initialize RP2040 AI chipset"""
        if logger:
            logger.info("Initializing RP2040 AI Chipset...")
        else:
            log_info("Initializing RP2040 AI Chipset...")
        
        # Initialize components
        self.db = ExploitDatabase()
        self.ai = AIEngine()
        self.comm = ChipsetCommunication(chipset_type="rp2040")
        
        # State
        self.running = False
        self.current_request = None
        
        if logger:
            logger.info("RP2040 AI Chipset initialized")
        else:
            log_info("RP2040 AI Chipset initialized")
    
    def start(self):
        """Start the AI chipset main loop"""
        self.running = True
        
        if logger:
            logger.info("RP2040 AI Chipset started - waiting for requests...")
        else:
            log_info("RP2040 AI Chipset started - waiting for requests...")
        
        print("\n" + "="*60)
        print("RP2040 AI CHIPSET - RedAI")
        print("="*60)
        print("Status: Ready")
        print("Waiting for requests from ESP32 execution chipset...")
        print("="*60 + "\n")
        
        while self.running:
            try:
                # Check for incoming messages from ESP32
                message = self.comm.receive_message(timeout=1.0)
                
                if message:
                    self._handle_message(message)
                
                # Small delay to prevent busy waiting
                time.sleep(0.1)
                
            except KeyboardInterrupt:
                if logger:
                    logger.info("Shutting down RP2040 AI Chipset...")
                else:
                    log_info("Shutting down RP2040 AI Chipset...")
                self.running = False
                break
            except Exception as e:
                if logger:
                    logger.error(f"Error in main loop: {e}")
                else:
                    log_error(f"Error in main loop: {e}")
                time.sleep(1)
    
    def _handle_message(self, message: Dict):
        """Handle incoming message from ESP32"""
        msg_type = message.get("type")
        payload = message.get("payload", {})
        
        if logger:
            logger.info(f"Received message: {msg_type}")
        else:
            log_info(f"Received message: {msg_type}")
        
        if msg_type == "ai_request":
            self._handle_ai_request(payload)
        elif msg_type == "execution_result":
            self._handle_execution_result(payload)
        elif msg_type == "status":
            self._handle_status(payload)
        elif msg_type == "test":
            # Respond to test message
            self.comm.send_message("test_response", {"message": "RP2040 AI Chipset ready"})
        else:
            if logger:
                logger.warning(f"Unknown message type: {msg_type}")
            else:
                log_info(f"Unknown message type: {msg_type}")
    
    def _handle_ai_request(self, payload: Dict):
        """Handle AI analysis request from ESP32"""
        target = payload.get("target", "")
        goal = payload.get("goal", "")
        
        if logger:
            logger.info(f"Processing AI request: target={target}, goal={goal}")
        else:
            log_info(f"Processing AI request: target={target}, goal={goal}")
        
        try:
            # Get all available exploits from database
            all_exploits = self.db.get_all_exploits()
            
            # Use AI to analyze and select/generate exploit
            analysis = self.ai.analyze_target(goal, all_exploits)
            
            if logger:
                logger.info(f"AI Analysis result: {analysis.get('action')}")
            else:
                log_info(f"AI Analysis result: {analysis.get('action')}")
            
            # Prepare response
            response_payload = {
                "analysis": analysis,
                "target": target,
                "goal": goal
            }
            
            # If using existing exploit, get full details
            if analysis.get("action") == "use_existing":
                exploit_id = analysis.get("exploit_id")
                if exploit_id:
                    exploit = self.db.get_exploit_with_methods(exploit_id)
                    if exploit:
                        response_payload["exploit"] = exploit
                        # Send execution request to ESP32
                        self.comm.send_execution_request(exploit)
                        return
            
            # If generating new exploit
            elif analysis.get("action") == "generate_new":
                generation_prompt = analysis.get("generation_prompt", goal)
                new_exploit = self.ai.generate_new_exploit(target, generation_prompt)
                
                # Save to database
                exploit_id = self.db.add_exploit(
                    name=new_exploit.get("name", "AI Generated Exploit"),
                    description=new_exploit.get("description", ""),
                    target_type=new_exploit.get("target_type", "unknown"),
                    target_component=new_exploit.get("target_component", "unknown"),
                    method_summary=new_exploit.get("method_summary", ""),
                    difficulty=new_exploit.get("difficulty", "medium"),
                    tools_required=new_exploit.get("tools_required", [])
                )
                
                # Add method steps
                steps = new_exploit.get("steps", [])
                if steps:
                    self.db.add_method_steps(exploit_id, steps)
                
                # Get full exploit and send to ESP32
                exploit = self.db.get_exploit_with_methods(exploit_id)
                if exploit:
                    response_payload["exploit"] = exploit
                    self.comm.send_execution_request(exploit)
                    return
            
            # Send analysis result back
            self.comm.send_message("ai_result", response_payload)
            
        except Exception as e:
            error_msg = f"Error processing AI request: {str(e)}"
            if logger:
                logger.error(error_msg)
            else:
                log_error(error_msg)
            
            self.comm.send_message("error", {
                "message": error_msg,
                "target": target,
                "goal": goal
            })
    
    def _handle_execution_result(self, payload: Dict):
        """Handle execution result from ESP32"""
        success = payload.get("success", False)
        result_data = payload.get("data", {})
        
        if logger:
            logger.info(f"Execution result received: success={success}")
        else:
            log_info(f"Execution result received: success={success}")
        
        # Record result in database
        exploit_id = result_data.get("exploit_id")
        target = result_data.get("target", "")
        output = result_data.get("output", "")
        execution_time = result_data.get("execution_time", 0.0)
        
        if exploit_id:
            self.db.record_execution(
                exploit_id=exploit_id,
                target=target,
                success=success,
                output=output,
                execution_time=execution_time
            )
        
        # AI can learn from results (future enhancement)
        # For now, just log the result
        print("\n" + "="*60)
        print("EXECUTION RESULT")
        print("="*60)
        print(f"Status: {'✓ SUCCESS' if success else '✗ FAILED'}")
        print(f"Target: {target}")
        print(f"Execution Time: {execution_time:.2f}s")
        print(f"\nOutput:\n{output}")
        print("="*60 + "\n")
    
    def _handle_status(self, payload: Dict):
        """Handle status update from ESP32"""
        status = payload.get("status", "")
        details = payload.get("details", {})
        
        if logger:
            logger.info(f"Status update: {status}")
        else:
            log_info(f"Status update: {status}")
        
        print(f"[ESP32 Status] {status}")
        if details:
            for key, value in details.items():
                print(f"  {key}: {value}")
    
    def request_execution(self, exploit: Dict, target: str):
        """Request exploit execution on ESP32"""
        exploit_data = {
            **exploit,
            "target": target
        }
        return self.comm.send_execution_request(exploit_data)
    
    def get_database_stats(self):
        """Get database statistics"""
        exploits = self.db.get_all_exploits()
        return {
            "total_exploits": len(exploits),
            "by_type": {}
        }

def main():
    """Main entry point for RP2040 AI chipset"""
    chipset = RP2040AIChipset()
    
    # Test communication
    print("Testing communication with ESP32...")
    if chipset.comm.test_communication():
        print("✓ Communication test passed\n")
    else:
        print("⚠ Communication test failed - continuing anyway\n")
    
    # Start main loop
    chipset.start()

if __name__ == "__main__":
    main()

