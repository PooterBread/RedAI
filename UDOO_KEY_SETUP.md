# Udoo Key Setup Guide

This guide covers setting up RedAI on the Udoo Key hardware platform.

## Hardware Specifications

- **Microcontrollers**: ESP32-WROVER-E + RP2040
- **Memory**: 8MB PSRAM, 264KB SRAM
- **Storage**: 16MB Internal Flash, 64 M-bit External QSPI Flash
- **Connectivity**: Wi-Fi/BT/BLE
- **I/O**: 26 GPIO pins, UEXT connector (I2C, SPI, UART)
- **Power**: 5VDC via USB-C
- **OS Support**: MicroPython, Arduino

## Setup Options

### Option 1: Full Python (Recommended for Development)

If you're running a full Linux environment on Udoo Key (via RP2040 or ESP32), you can use the standard Python implementation:

1. **Install Python 3.8+** (if not already installed)
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure API keys** (see main README)
4. **Run the tool**:
   ```bash
   python main.py
   ```

### Option 2: MicroPython (Resource-Optimized)

For MicroPython on Udoo Key:

#### Prerequisites

1. **Flash MicroPython** to your Udoo Key
   - Download MicroPython firmware for ESP32 or RP2040
   - Use appropriate flashing tool (esptool for ESP32, rp2040 tools for RP2040)

2. **Install urequests** (for HTTP requests):
   ```python
   import upip
   upip.install('urequests')
   ```

#### File Structure for MicroPython

MicroPython has limited file system support. You'll need to:

1. **Copy essential files** to the device:
   - `main.py` (entry point)
   - `config.py`
   - `database.py`
   - `ai_engine.py`
   - `exploit_executor.py`
   - `micropython_compat.py`
   - `udoo_key_optimized.py`

2. **Database**: SQLite works on MicroPython, but you may need to use a simpler storage method:
   - Consider using JSON files for exploit storage
   - Or use MicroPython's built-in storage capabilities

#### Limitations on MicroPython

- **No subprocess**: Commands must use `urequests` for HTTP requests
- **Limited libraries**: Some Python standard library features unavailable
- **Memory constraints**: 264KB SRAM requires careful memory management
- **File system**: Limited file operations

#### MicroPython-Specific Configuration

Edit `config.py` for MicroPython:

```python
# Use lightweight model
MODEL_NAME = "gpt-4o-mini"  # or "claude-3-haiku-20240307"

# Reduce memory usage
MAX_EXECUTION_TIME = 120  # Shorter timeout
REQUIRE_CONFIRMATION = True
```

## Wi-Fi Setup (Required for AI API)

The Udoo Key needs Wi-Fi connectivity to use AI APIs:

### ESP32 MicroPython Wi-Fi Setup

```python
import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('YOUR_SSID', 'YOUR_PASSWORD')

# Wait for connection
import time
while not wlan.isconnected():
    time.sleep(1)

print('Wi-Fi connected:', wlan.ifconfig())
```

### RP2040 Wi-Fi Setup

If using RP2040 with Wi-Fi module, follow similar pattern or use CircuitPython Wi-Fi libraries.

## Memory Optimization

The Udoo Key has limited memory (264KB SRAM). Use these optimizations:

1. **Enable garbage collection**:
   ```python
   import gc
   gc.collect()  # Call periodically
   ```

2. **Use the optimizer**:
   ```python
   from udoo_key_optimized import UdooKeyOptimizer
   optimizer = UdooKeyOptimizer()
   optimizer.optimize_memory()
   ```

3. **Limit exploit database size**: Keep only essential exploits in memory

4. **Stream responses**: Don't load entire AI responses into memory at once

## Network Considerations

- **API Calls**: All AI operations use cloud APIs (OpenAI/Anthropic)
- **Bandwidth**: Ensure stable Wi-Fi connection
- **Latency**: API calls may take 1-5 seconds depending on connection
- **Data Usage**: Monitor API usage to avoid excessive costs

## Storage Considerations

With 16MB internal flash:

- **Database**: SQLite database will be stored in flash
- **Logs**: Keep log rotation enabled
- **Exploits**: Store exploit definitions efficiently (JSON or SQLite)

## Recommended Configuration

For Udoo Key, use these settings in `config.py`:

```python
# Lightweight model
MODEL_NAME = "gpt-4o-mini"  # Cheaper and faster

# Shorter timeouts
MAX_EXECUTION_TIME = 120

# Enable memory optimization
ENABLE_MEMORY_OPTIMIZATION = True

# Use cloud APIs (not local models)
AI_PROVIDER = "openai"  # or "anthropic"
```

## Testing on Udoo Key

1. **Test Wi-Fi connectivity**:
   ```python
   import network
   wlan = network.WLAN(network.STA_IF)
   print(wlan.isconnected())
   ```

2. **Test API connectivity**:
   ```python
   import urequests
   response = urequests.get("https://api.openai.com/v1/models")
   print(response.status_code)
   ```

3. **Test database**:
   ```python
   from database import ExploitDatabase
   db = ExploitDatabase()
   print("Database initialized")
   ```

## Troubleshooting

### Out of Memory Errors

- Reduce `MAX_EXECUTION_TIME`
- Enable garbage collection more frequently
- Use smaller AI models
- Limit exploit database queries

### Wi-Fi Connection Issues

- Check SSID and password
- Ensure 2.4GHz network (ESP32 doesn't support 5GHz)
- Check signal strength
- Verify router compatibility

### API Connection Failures

- Verify API keys are set correctly
- Check internet connectivity
- Test with simple HTTP request first
- Review API rate limits

### Database Errors

- Ensure flash has sufficient space
- Check file system permissions
- Verify SQLite is available on your MicroPython build

## Performance Tips

1. **Batch operations**: Group multiple operations when possible
2. **Cache results**: Store AI responses for similar queries
3. **Lazy loading**: Load exploits only when needed
4. **Connection pooling**: Reuse HTTP connections when possible

## Alternative: Hybrid Approach

You can run RedAI in a hybrid mode:
- **Udoo Key**: Collects data, executes exploits
- **External Server**: Runs AI analysis, stores large databases

This distributes the workload and reduces Udoo Key resource usage.

## Support

For Udoo Key-specific issues:
1. Check MicroPython documentation
2. Review Udoo Key hardware documentation
3. Test components individually (Wi-Fi, storage, etc.)
4. Monitor memory usage with `gc.mem_free()`




