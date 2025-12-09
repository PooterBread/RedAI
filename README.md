# RedAI - AI-Powered Penetration Testing Tool

An intelligent penetration testing tool that uses AI to automate security testing tasks. Compatible with **Udoo Key** (Raspberry Pi RP2040 + ESP32) for portable, on-device penetration testing.

## ⚠️ Disclaimer

**This tool is for EDUCATIONAL PURPOSES and AUTHORIZED PENETRATION TESTING ONLY.**

- Only use on systems you own or have explicit written permission to test
- Unauthorized access to computer systems is illegal
- Users are solely responsible for their actions
- The developers assume no liability for misuse

## Features

- 🤖 **AI-Powered Exploit Generation**: Uses advanced AI models to generate new exploit methods when known exploits don't exist
- 📚 **Exploit Database**: Maintains a database of known exploits and methods for quick access
- 🔍 **Intelligent Matching**: AI analyzes your testing goals and matches them with relevant exploits
- ⚡ **Automated Execution**: Executes penetration testing methods step-by-step
- 🔒 **Safety Features**: Built-in safety checks and confirmation prompts
- 📊 **Execution Tracking**: Records all execution results for analysis
- 🎯 **Udoo Key Compatible**: Optimized for resource-constrained devices

## Architecture

### Unified Mode (Single Device)
```
RedAI/
├── main.py              # Main application entry point
├── ai_engine.py         # AI model integration (OpenAI/Anthropic)
├── database.py          # SQLite database management
├── exploit_executor.py  # Safe exploit execution engine
├── config.py            # Configuration management
└── init_sample_data.py  # Sample exploit data initialization
```

### Dual Chipset Mode (Distributed)
```
RP2040 (AI Chipset)          ESP32 (Execution Chipset)
├── rp2040_ai_chipset.py    ├── esp32_execution_chipset.py
├── ai_engine.py            ├── exploit_executor.py
├── database.py             ├── network_exploits.py
└── chipset_communication.py └── chipset_communication.py
         ↕ UART Communication ↕
```

**Dual Chipset Benefits:**
- **RP2040**: Handles AI logic, database, decision-making (better processing power)
- **ESP32**: Handles network operations, command execution (built-in Wi-Fi/Bluetooth)
- **Resource Optimization**: Each chipset focuses on its strengths
- **Parallel Processing**: AI can analyze while execution runs

See `DUAL_CHIPSET_SETUP.md` for detailed setup instructions.

## Installation

### Prerequisites

- Python 3.8 or higher
- Udoo Key (or any system running Python)
- API key for AI provider (OpenAI or Anthropic)

### Setup

1. **Clone or download this repository**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   
   Create a `.env` file (or set environment variables):
   ```bash
   # For OpenAI
   export AI_PROVIDER=openai
   export OPENAI_API_KEY=your_api_key_here
   export MODEL_NAME=gpt-4o-mini
   
   # OR for Anthropic
   export AI_PROVIDER=anthropic
   export ANTHROPIC_API_KEY=your_api_key_here
   ```

   Alternatively, use a `.env` file:
   ```bash
   AI_PROVIDER=openai
   OPENAI_API_KEY=your_key_here
   MODEL_NAME=gpt-4o-mini
   ```

4. **Initialize sample data** (optional):
   ```bash
   python init_sample_data.py
   ```

5. **Populate comprehensive vulnerability database** (recommended):
   ```bash
   python populate_vulnerability_database.py
   ```
   This adds 30+ known vulnerabilities and exploitation methods from OWASP Top 10, CVE database, and common penetration testing techniques.

## Usage

### Interactive Mode

Run the tool interactively:

```bash
python main.py
```

The interactive menu provides:
1. Run penetration test (enter target/goal)
2. View exploit database
3. Add manual exploit
4. View execution history
5. Exit

### Command Line Mode

Run a specific test:

```bash
python main.py --target http://example.com --goal "test authentication"
```

### Example Workflow

1. **Start the tool**:
   ```bash
   python main.py
   ```

2. **Select option 1** to run a penetration test

3. **Enter target**: `http://vulnerable-app.local`

4. **Enter goal**: `capture flag from authentication system`

5. **AI Analysis**: The tool will:
   - Search the exploit database for matching methods
   - If found, use the existing exploit
   - If not found, generate a new exploit method using AI

6. **Review and confirm**: Review the exploit method and confirm execution

7. **Execution**: The tool executes the exploit step-by-step

8. **Results**: View execution results and captured data

## How It Works

### 1. User Prompt Analysis

When you provide a target and goal, the AI:
- Analyzes your request
- Searches the exploit database for relevant methods
- Determines if an existing exploit can be used or if a new one needs to be generated

### 2. Exploit Selection/Generation

**If matching exploit found**:
- Retrieves the exploit from database
- Prepares execution plan
- Executes step-by-step

**If no matching exploit**:
- AI generates a new exploit method based on:
  - Target description
  - Testing goal
  - Known vulnerability patterns
- Saves the new exploit to database for future use
- Executes the generated method

### 3. Safe Execution

The execution engine:
- Validates exploit structure
- Requires user confirmation (configurable)
- Executes commands with timeouts
- Blocks dangerous commands
- Records all results

## Database Schema

The tool uses SQLite with three main tables:

- **exploits**: Stores exploit metadata (name, description, target type, etc.)
- **methods**: Stores step-by-step execution methods for each exploit
- **execution_results**: Tracks execution history and results

## Configuration

Edit `config.py` or set environment variables:

- `AI_PROVIDER`: AI provider (`openai`, `anthropic`, `local`)
- `MODEL_NAME`: Model to use (default: `gpt-4o-mini` for cost efficiency)
- `MAX_EXECUTION_TIME`: Maximum time per exploit (default: 300s)
- `REQUIRE_CONFIRMATION`: Require user confirmation (default: True)
- `LOG_LEVEL`: Logging level (default: INFO)

## Udoo Key Compatibility

RedAI is designed to work with Udoo Key's hardware constraints:

### Hardware Specifications Supported
- **ESP32-WROVER-E + RP2040** microcontrollers
- **8MB PSRAM, 264KB SRAM** memory constraints
- **16MB Flash** storage
- **Wi-Fi/BT/BLE** connectivity for API access

### Setup Options

1. **Full Python** (if running Linux on Udoo Key):
   - Standard installation works as-is
   - All features available

2. **MicroPython** (resource-constrained):
   - Use `micropython_compat.py` for compatibility
   - Requires `urequests` for HTTP operations
   - See `UDOO_KEY_SETUP.md` for detailed instructions

### Optimizations

1. **Lightweight models**: `gpt-4o-mini` or `claude-3-haiku` recommended
2. **API-based AI**: Cloud APIs (no local model inference needed)
3. **Memory management**: Built-in garbage collection and optimization
4. **Efficient storage**: SQLite database optimized for flash storage
5. **Network-aware**: Handles Wi-Fi connectivity and reconnection

See `UDOO_KEY_SETUP.md` for complete Udoo Key setup instructions.

## Vulnerability Database

The tool includes a comprehensive vulnerability database with 30+ known exploits:

### OWASP Top 10 2024
- Broken Access Control (IDOR)
- Cryptographic Failures
- Injection (SQL, NoSQL, LDAP, Command)
- Insecure Design
- Security Misconfiguration
- Vulnerable Components
- Authentication Failures
- Software/Data Integrity Failures
- Security Logging Failures
- Server-Side Request Forgery (SSRF)

### Additional Vulnerabilities
- XML External Entity (XXE) Injection
- File Upload Vulnerabilities
- Cross-Site Request Forgery (CSRF)
- XSS Variants (Stored, Reflected, DOM-based)
- Path Traversal (with encoding bypasses)
- API Vulnerabilities (Mass Assignment, Rate Limiting)
- Network Attacks (ARP/DNS Spoofing)
- Buffer Overflows
- Server-Side Template Injection (SSTI)
- Race Conditions
- Open Redirect
- HTTP Header Injection
- Subdomain Takeover
- Information Disclosure
- And more...

**To populate the full database:**
```bash
python populate_vulnerability_database.py
```

## Extending the Tool

### Adding Custom Exploits

1. Use the interactive menu (option 3) to add manually
2. Or modify `init_sample_data.py` to add more samples
3. Or let the AI generate new exploits automatically

### Custom AI Models

To use local models (future feature):
- Set `AI_PROVIDER=local`
- Configure `LOCAL_MODEL_PATH` and `LOCAL_MODEL_TYPE`
- Implement local model interface in `ai_engine.py`

## Safety Features

- ✅ Command validation and sanitization
- ✅ Dangerous command blocking
- ✅ Execution timeouts
- ✅ User confirmation prompts
- ✅ Comprehensive logging
- ✅ Execution history tracking

## Troubleshooting

### "API key not set" error
- Ensure your API key is set in environment variables or `.env` file
- Check that `AI_PROVIDER` matches your API key type

### "No exploits found"
- Run `python init_sample_data.py` to populate sample data
- Or add exploits manually through the menu

### Execution failures
- Check that target is accessible
- Verify network connectivity
- Review logs in `logs/execution.log`

## Contributing

This is an educational project. Contributions should:
- Maintain ethical use focus
- Add safety features
- Improve AI integration
- Enhance Udoo Key compatibility

## License

This project is for educational purposes. Use responsibly and ethically.

## Support

For issues or questions:
1. Check the logs in `logs/execution.log`
2. Review configuration in `config.py`
3. Ensure all dependencies are installed

---

**Remember**: With great power comes great responsibility. Use this tool ethically and only on systems you're authorized to test.
