# Dual Chipset Setup Guide

This guide explains how to set up RedAI in distributed mode with RP2040 as the AI chipset and ESP32 as the execution chipset.

## Architecture Overview

**RP2040 (AI Chipset):**
- Handles AI logic and decision-making
- Manages database operations
- Analyzes targets and selects/generates exploits
- Communicates with ESP32 via UART

**ESP32 (Execution Chipset):**
- Executes penetration testing commands
- Handles network operations (Nmap, tcpdump, etc.)
- Manages Wi-Fi/Bluetooth for network attacks
- Performs packet injection and capture
- Communicates with RP2040 via UART

## Hardware Connections

The chipsets communicate via UART:
- **RP2040**: GPIO0 (TX) → ESP32 IO22 (RX)
- **RP2040**: GPIO1 (RX) ← ESP32 IO19 (TX)
- **Baudrate**: 115200 (default, configurable)

## Software Setup

### Step 1: Flash Firmware

**RP2040:**
- Flash MicroPython or full Python environment
- Recommended: Raspberry Pi OS Lite (if supported) or MicroPython

**ESP32:**
- Flash MicroPython firmware
- Ensure UART pins are configured correctly

### Step 2: Transfer Files

**RP2040 (AI Chipset) - Required Files:**
```
rp2040_ai_chipset.py
chipset_communication.py
ai_engine.py
database.py
config.py
micropython_compat.py (if using MicroPython)
udoo_key_optimized.py
```

**ESP32 (Execution Chipset) - Required Files:**
```
esp32_execution_chipset.py
chipset_communication.py
exploit_executor.py
network_exploits.py
config.py
micropython_compat.py
```

### Step 3: Install Dependencies

**RP2040:**
```bash
# If using full Python
pip install openai anthropic python-dotenv

# If using MicroPython
import upip
upip.install('urequests')
```

**ESP32:**
```bash
# If using full Python
pip install -r requirements.txt

# If using MicroPython
import upip
upip.install('urequests')
```

### Step 4: Configure

**RP2040 - Set API Key:**
```python
# In config.py or environment
OPENAI_API_KEY = "your-key-here"
AI_PROVIDER = "openai"
```

**ESP32 - Configure Wi-Fi (optional):**
```python
# In esp32_execution_chipset.py main()
chipset.setup_wifi("YOUR_SSID", "YOUR_PASSWORD")
```

### Step 5: Initialize Database (RP2040 only)

On RP2040, run:
```bash
python init_sample_data.py
python populate_vulnerability_database.py
```

## Running the System

### Option 1: Start Both Chipsets Independently

**Terminal 1 - RP2040 (AI Chipset):**
```bash
python rp2040_ai_chipset.py
```

**Terminal 2 - ESP32 (Execution Chipset):**
```bash
python esp32_execution_chipset.py
```

### Option 2: Unified Mode (Single Chipset)

If running on a single device:
```bash
python main.py
```

## Communication Protocol

The chipsets communicate using JSON messages over UART:

### Message Format
```json
{
    "type": "ai_request" | "execution_request" | "result" | "status",
    "payload": {...},
    "timestamp": 1234567890.123,
    "chipset": "rp2040" | "esp32"
}
```

### Message Types

**AI Request (ESP32 → RP2040):**
```json
{
    "type": "ai_request",
    "payload": {
        "target": "http://example.com",
        "goal": "test authentication"
    }
}
```

**Execution Request (RP2040 → ESP32):**
```json
{
    "type": "execution_request",
    "payload": {
        "exploit": {...},
        "target": "http://example.com"
    }
}
```

**Result (ESP32 → RP2040):**
```json
{
    "type": "result",
    "payload": {
        "success": true,
        "data": {
            "exploit_id": 1,
            "target": "http://example.com",
            "output": "...",
            "execution_time": 2.5
        }
    }
}
```

## Testing Communication

### Test RP2040 → ESP32

On RP2040:
```python
from chipset_communication import ChipsetCommunication
comm = ChipsetCommunication("rp2040")
comm.test_communication()
```

On ESP32:
```python
from chipset_communication import ChipsetCommunication
comm = ChipsetCommunication("esp32")
comm.test_communication()
```

## Workflow Example

1. **User provides target/goal** → ESP32 receives input
2. **ESP32 sends AI request** → RP2040 via UART
3. **RP2040 analyzes** → Uses AI engine and database
4. **RP2040 sends exploit** → ESP32 via UART
5. **ESP32 executes** → Runs penetration testing tools
6. **ESP32 sends results** → RP2040 via UART
7. **RP2040 records results** → Updates database
8. **Results displayed** → To user

## Troubleshooting

### Communication Issues

**Problem: No messages received**
- Check UART connections (GPIO0/GPIO1 on RP2040, IO19/IO22 on ESP32)
- Verify baudrate matches (default: 115200)
- Check if UART is initialized correctly

**Problem: Messages corrupted**
- Reduce baudrate if needed
- Check for interference
- Verify power supply is stable

### RP2040 Issues

**Problem: AI engine not working**
- Verify API key is set
- Check internet connectivity (if using cloud APIs)
- Ensure database is initialized

**Problem: Database errors**
- Check flash storage space
- Verify SQLite support in MicroPython build
- Reinitialize database if needed

### ESP32 Issues

**Problem: Network tools not working**
- Verify Wi-Fi is connected (if needed)
- Check if tools are installed (Nmap, tcpdump)
- Ensure network interface is accessible

**Problem: Execution fails**
- Check exploit structure
- Verify target is accessible
- Review error messages in logs

## Performance Optimization

### RP2040 (AI Chipset)
- Use lightweight AI models (gpt-4o-mini)
- Enable memory optimization
- Limit database query results
- Cache AI responses when possible

### ESP32 (Execution Chipset)
- Optimize network operations
- Use efficient packet capture
- Limit execution timeouts
- Stream large outputs

## Advanced Configuration

### Custom UART Settings

Edit `config.py`:
```python
UART_BAUDRATE = 230400  # Higher speed (if stable)
```

### Message Timeout

Edit `chipset_communication.py`:
```python
def send_message(self, message_type, payload, timeout=10.0):
    # Increase timeout for slow operations
```

### Error Handling

Both chipsets include error handling and will:
- Retry failed communications
- Log errors for debugging
- Continue operation after errors

## Security Considerations

- **API Keys**: Store securely on RP2040 only
- **Network**: Use secure Wi-Fi connections
- **Communication**: Consider encrypting UART messages for sensitive data
- **Execution**: Always require confirmation for dangerous operations

## Future Enhancements

- Encrypted inter-chipset communication
- Load balancing between chipsets
- Redundant execution paths
- Real-time status monitoring
- Web interface for remote control

## Support

For issues:
1. Check communication test results
2. Review logs on both chipsets
3. Verify hardware connections
4. Test components individually
5. Check Udoo Key documentation

