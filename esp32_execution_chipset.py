#!/usr/bin/env python3
"""
ESP32 Execution Chipset Module
Handles network operations, command execution, and penetration testing tools
Communicates with RP2040 AI chipset via UART
"""

import sys
import time
import json
from typing import Dict, Optional

# Import modules
from exploit_executor import ExploitExecutor
from network_exploits import NetworkExploitEngine
from chipset_communication import ChipsetCommunication

# MicroPython compatibility
IS_MICROPYTHON = sys.implementation.name == 'micropython'

if IS_MICROPYTHON:
    import network
    import machine
    import uasyncio as asyncio
else:
    import asyncio

if not IS_MICROPYTHON:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
else:
    logger = None
    def log_info(msg): print(f"[EXEC] {msg}")
    def log_error(msg): print(f"[EXEC ERROR] {msg}")

class ESP32ExecutionChipset:
    """ESP32 Execution Chipset - Handles network operations and command execution"""
    
    def __init__(self):
        """Initialize ESP32 execution chipset"""
        if logger:
            logger.info("Initializing ESP32 Execution Chipset...")
        else:
            log_info("Initializing ESP32 Execution Chipset...")
        
        # Initialize components
        self.executor = ExploitExecutor()
        self.network_engine = NetworkExploitEngine()
        self.comm = ChipsetCommunication(chipset_type="esp32")
        
        # Network setup
        self.wlan = None
        if IS_MICROPYTHON:
            self.wlan = network.WLAN(network.STA_IF)
        
        # State
        self.running = False
        self.current_execution = None
        
        if logger:
            logger.info("ESP32 Execution Chipset initialized")
        else:
            log_info("ESP32 Execution Chipset initialized")
    
    def setup_wifi(self, ssid: str, password: str):
        """Setup Wi-Fi connection"""
        if not IS_MICROPYTHON or not self.wlan:
            if logger:
                logger.warning("Wi-Fi setup not available (not MicroPython)")
            return False
        
        try:
            self.wlan.active(True)
            self.wlan.connect(ssid, password)
            
            # Wait for connection
            timeout = 10
            while not self.wlan.isconnected() and timeout > 0:
                time.sleep(1)
                timeout -= 1
            
            if self.wlan.isconnected():
                if logger:
                    logger.info(f"Wi-Fi connected: {self.wlan.ifconfig()}")
                else:
                    log_info(f"Wi-Fi connected: {self.wlan.ifconfig()}")
                return True
            else:
                if logger:
                    logger.error("Wi-Fi connection failed")
                else:
                    log_error("Wi-Fi connection failed")
                return False
        except Exception as e:
            if logger:
                logger.error(f"Wi-Fi setup error: {e}")
            else:
                log_error(f"Wi-Fi setup error: {e}")
            return False
    
    def start(self):
        """Start the execution chipset main loop"""
        self.running = True
        
        if logger:
            logger.info("ESP32 Execution Chipset started - waiting for commands...")
        else:
            log_info("ESP32 Execution Chipset started - waiting for commands...")
        
        print("\n" + "="*60)
        print("ESP32 EXECUTION CHIPSET - RedAI")
        print("="*60)
        print("Status: Ready")
        print("Waiting for commands from RP2040 AI chipset...")
        print("="*60 + "\n")
        
        while self.running:
            try:
                # Check for incoming messages from RP2040
                message = self.comm.receive_message(timeout=1.0)
                
                if message:
                    self._handle_message(message)
                
                # Small delay to prevent busy waiting
                time.sleep(0.1)
                
            except KeyboardInterrupt:
                if logger:
                    logger.info("Shutting down ESP32 Execution Chipset...")
                else:
                    log_info("Shutting down ESP32 Execution Chipset...")
                self.running = False
                break
            except Exception as e:
                if logger:
                    logger.error(f"Error in main loop: {e}")
                else:
                    log_error(f"Error in main loop: {e}")
                time.sleep(1)
    
    def _handle_message(self, message: Dict):
        """Handle incoming message from RP2040"""
        msg_type = message.get("type")
        payload = message.get("payload", {})
        
        if logger:
            logger.info(f"Received message: {msg_type}")
        else:
            log_info(f"Received message: {msg_type}")
        
        if msg_type == "execution_request":
            self._handle_execution_request(payload)
        elif msg_type == "network_request":
            self._handle_network_request(payload)
        elif msg_type == "test":
            # Respond to test message
            self.comm.send_message("test_response", {"message": "ESP32 Execution Chipset ready"})
        else:
            if logger:
                logger.warning(f"Unknown message type: {msg_type}")
            else:
                log_info(f"Unknown message type: {msg_type}")
    
    def _handle_execution_request(self, payload: Dict):
        """Handle exploit execution request from RP2040"""
        exploit = payload.get("exploit", {})
        target = payload.get("target", exploit.get("target", ""))
        
        if logger:
            logger.info(f"Executing exploit: {exploit.get('name', 'Unknown')}")
        else:
            log_info(f"Executing exploit: {exploit.get('name', 'Unknown')}")
        
        # Send status update
        self.comm.send_status("executing", {
            "exploit": exploit.get("name", "Unknown"),
            "target": target
        })
        
        try:
            # Execute exploit
            start_time = time.time()
            success, output = self.executor.execute_exploit(exploit, target, auto_confirm=True)
            execution_time = time.time() - start_time
            
            # Prepare result
            result = {
                "exploit_id": exploit.get("id"),
                "target": target,
                "success": success,
                "output": output,
                "execution_time": execution_time
            }
            
            # Send result back to RP2040
            self.comm.send_result(result, success=success)
            
        except Exception as e:
            error_msg = f"Execution error: {str(e)}"
            if logger:
                logger.error(error_msg)
            else:
                log_error(error_msg)
            
            self.comm.send_result({
                "exploit_id": exploit.get("id"),
                "target": target,
                "success": False,
                "output": error_msg,
                "execution_time": 0.0
            }, success=False)
    
    def _handle_network_request(self, payload: Dict):
        """Handle network operation request from RP2040"""
        operation = payload.get("operation", "")
        
        if logger:
            logger.info(f"Network operation: {operation}")
        else:
            log_info(f"Network operation: {operation}")
        
        try:
            if operation == "nac_test":
                interface = payload.get("interface", "eth0")
                result = self.network_engine.test_network_access_control(interface)
                self.comm.send_result(result, success=True)
            
            elif operation == "host_discovery":
                target_range = payload.get("target_range")
                interface = payload.get("interface", "eth0")
                result = self.network_engine.nmap_host_discovery(target_range, interface)
                self.comm.send_result(result, success=result.get("success", False))
            
            elif operation == "port_scan":
                target = payload.get("target", "")
                scan_type = payload.get("scan_type", "syn")
                result = self.network_engine.nmap_port_scan(target, scan_type)
                self.comm.send_result(result, success=result.get("success", False))
            
            elif operation == "packet_capture":
                interface = payload.get("interface", "eth0")
                duration = payload.get("duration", 60)
                filter_str = payload.get("filter")
                result = self.network_engine.capture_packets(interface, duration, filter_str)
                self.comm.send_result(result, success=result.get("success", False))
            
            else:
                self.comm.send_result({
                    "error": f"Unknown network operation: {operation}"
                }, success=False)
        
        except Exception as e:
            error_msg = f"Network operation error: {str(e)}"
            if logger:
                logger.error(error_msg)
            else:
                log_error(error_msg)
            
            self.comm.send_result({
                "error": error_msg
            }, success=False)
    
    def request_ai_analysis(self, target: str, goal: str):
        """Request AI analysis from RP2040"""
        return self.comm.send_ai_request(target, goal)

def main():
    """Main entry point for ESP32 execution chipset"""
    chipset = ESP32ExecutionChipset()
    
    # Setup Wi-Fi if needed (can be configured)
    # chipset.setup_wifi("YOUR_SSID", "YOUR_PASSWORD")
    
    # Test communication
    print("Testing communication with RP2040...")
    if chipset.comm.test_communication():
        print("✓ Communication test passed\n")
    else:
        print("⚠ Communication test failed - continuing anyway\n")
    
    # Start main loop
    chipset.start()

if __name__ == "__main__":
    main()

