"""
Inter-Chipset Communication Module
Handles communication between RP2040 (AI chipset) and ESP32 (execution chipset)
Uses UART for serial communication
"""

import json
import time
import sys

# Detect which chipset we're running on
IS_MICROPYTHON = sys.implementation.name == 'micropython'

if IS_MICROPYTHON:
    from machine import UART
    import uasyncio as asyncio
else:
    # For testing/development on regular Python
    import serial
    import asyncio

class ChipsetCommunication:
    """Handles communication between RP2040 and ESP32"""
    
    def __init__(self, chipset_type="rp2040", baudrate=115200):
        """
        Initialize chipset communication
        
        Args:
            chipset_type: "rp2040" or "esp32"
            baudrate: UART baudrate (default: 115200)
        """
        self.chipset_type = chipset_type
        self.baudrate = baudrate
        self.uart = None
        self.message_queue = []
        self._init_uart()
    
    def _init_uart(self):
        """Initialize UART based on chipset type"""
        if IS_MICROPYTHON:
            if self.chipset_type == "rp2040":
                # RP2040: GPIO0 (TX), GPIO1 (RX)
                self.uart = UART(0, baudrate=self.baudrate, tx=0, rx=1)
            elif self.chipset_type == "esp32":
                # ESP32: IO19 (TX), IO22 (RX)
                self.uart = UART(1, baudrate=self.baudrate, tx=19, rx=22)
        else:
            # For development/testing - use serial port
            # This would need to be configured for actual hardware
            pass
    
    def send_message(self, message_type: str, payload: dict, timeout: float = 5.0):
        """
        Send message to other chipset
        
        Args:
            message_type: Type of message (ai_request, execution_request, result, etc.)
            payload: Message payload dictionary
            timeout: Timeout in seconds
        
        Returns:
            Response message or None if timeout
        """
        message = {
            "type": message_type,
            "payload": payload,
            "timestamp": time.time(),
            "chipset": self.chipset_type
        }
        
        message_json = json.dumps(message) + "\n"
        
        if IS_MICROPYTHON:
            if self.uart:
                self.uart.write(message_json.encode())
                return self._wait_for_response(timeout)
        else:
            # Development mode - simulate communication
            print(f"[{self.chipset_type.upper()}] Sending: {message_type}")
            return None
    
    def _wait_for_response(self, timeout: float):
        """Wait for response from other chipset"""
        start_time = time.time()
        buffer = b""
        
        while time.time() - start_time < timeout:
            if self.uart.any():
                data = self.uart.read()
                if data:
                    buffer += data
                    if b"\n" in buffer:
                        # Complete message received
                        try:
                            message_str = buffer.split(b"\n")[0].decode()
                            message = json.loads(message_str)
                            return message
                        except (json.JSONDecodeError, UnicodeDecodeError):
                            buffer = b""
                            continue
            
            time.sleep(0.01)  # Small delay to prevent busy waiting
        
        return None
    
    def receive_message(self, timeout: float = 5.0):
        """
        Receive message from other chipset
        
        Args:
            timeout: Timeout in seconds
        
        Returns:
            Message dictionary or None if timeout
        """
        if IS_MICROPYTHON:
            if self.uart and self.uart.any():
                buffer = b""
                start_time = time.time()
                
                while time.time() - start_time < timeout:
                    if self.uart.any():
                        data = self.uart.read()
                        if data:
                            buffer += data
                            if b"\n" in buffer:
                                try:
                                    message_str = buffer.split(b"\n")[0].decode()
                                    message = json.loads(message_str)
                                    return message
                                except (json.JSONDecodeError, UnicodeDecodeError):
                                    buffer = b""
                                    continue
                    time.sleep(0.01)
        
        return None
    
    def send_ai_request(self, target: str, goal: str):
        """Send AI analysis request (from ESP32 to RP2040)"""
        return self.send_message("ai_request", {
            "target": target,
            "goal": goal
        })
    
    def send_execution_request(self, exploit_data: dict):
        """Send execution request (from RP2040 to ESP32)"""
        return self.send_message("execution_request", {
            "exploit": exploit_data
        })
    
    def send_result(self, result: dict, success: bool = True):
        """Send execution result (from ESP32 to RP2040)"""
        return self.send_message("result", {
            "success": success,
            "data": result
        })
    
    def send_status(self, status: str, details: dict = None):
        """Send status update"""
        return self.send_message("status", {
            "status": status,
            "details": details or {}
        })
    
    def test_communication(self):
        """Test communication between chipsets"""
        print(f"Testing {self.chipset_type.upper()} communication...")
        
        if self.chipset_type == "rp2040":
            # RP2040 sends test message
            response = self.send_message("test", {"message": "Hello from RP2040"})
            if response:
                print(f"✓ Communication test successful: {response}")
                return True
            else:
                print("✗ Communication test failed - no response")
                return False
        else:
            # ESP32 waits for test message
            message = self.receive_message(timeout=10.0)
            if message and message.get("type") == "test":
                print(f"✓ Received test message: {message}")
                # Send response
                self.send_message("test_response", {"message": "Hello from ESP32"})
                return True
            else:
                print("✗ Communication test failed - no message received")
                return False

