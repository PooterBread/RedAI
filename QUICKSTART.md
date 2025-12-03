# RedAI Quick Start Guide

Get up and running with RedAI in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- API key for OpenAI or Anthropic
- Internet connection (for AI API calls)

## Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set your API key**:
   ```bash
   export OPENAI_API_KEY="your-key-here"
   # OR
   export ANTHROPIC_API_KEY="your-key-here"
   ```

3. **Initialize sample data** (optional but recommended):
   ```bash
   python init_sample_data.py
   ```

## First Run

1. **Start RedAI**:
   ```bash
   python main.py
   ```

2. **Select option 1** - Run penetration test

3. **Enter target**: `http://example.com`

4. **Enter goal**: `test for SQL injection vulnerabilities`

5. **Review and confirm** the exploit method

6. **View results** after execution

## Example Commands

### Test Authentication
```
Target: http://vulnerable-app.local
Goal: bypass authentication and capture flag
```

### Test File Access
```
Target: http://web-app.com
Goal: access sensitive files using directory traversal
```

### Test API Security
```
Target: https://api.example.com
Goal: discover hidden API endpoints
```

## Configuration

Edit `config.py` or set environment variables:

- `AI_PROVIDER`: `openai` or `anthropic`
- `MODEL_NAME`: Model to use (default: `gpt-4o-mini`)
- `REQUIRE_CONFIRMATION`: Require user confirmation (default: `True`)

## Udoo Key Users

If you're using Udoo Key, see `UDOO_KEY_SETUP.md` for specific instructions.

## Troubleshooting

**"API key not set"**
- Make sure you've exported the API key as an environment variable
- Or create a `.env` file with your key

**"No exploits found"**
- Run `python init_sample_data.py` to populate sample exploits

**Connection errors**
- Check your internet connection
- Verify API key is valid
- Check API service status

## Next Steps

- Add your own exploits via the menu (option 3)
- Review execution history
- Customize exploit methods
- Explore AI-generated exploit variations

---

**Remember**: Only use on systems you own or have explicit permission to test!


