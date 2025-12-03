# Fix IntelliCode Error - Step by Step

## Method 1: Check Output Windows (Do This First)

1. In VS Code, press `Cmd+Shift+U` to open Output panel
2. In the dropdown at the top right of the Output panel, select:
   - "Python" - look for errors
   - "VS IntelliCode" - look for errors
3. Copy any error messages you see

## Method 2: Reset Python Language Server

1. Press `Cmd+Shift+P`
2. Type: `Python: Restart Language Server`
3. Wait a few seconds
4. Check if error is gone

## Method 3: Disable IntelliCode Temporarily

1. Press `Cmd+Shift+X` (Extensions)
2. Search for "IntelliCode"
3. Click the gear icon next to it
4. Select "Disable"
5. Reload VS Code (`Cmd+Shift+P` → "Developer: Reload Window")
6. Re-enable it after reload

## Method 4: Reinstall Python Extension

1. Press `Cmd+Shift+X`
2. Search for "Python" (by Microsoft)
3. Click the gear icon → "Uninstall"
4. Reload VS Code
5. Reinstall Python extension
6. Reload again

## Method 5: Clear All VS Code Python Caches

Run these commands in terminal:

```bash
# Clear Python extension cache
rm -rf ~/Library/Application\ Support/Code/User/workspaceStorage/*/state.vscdb

# Clear IntelliCode cache
rm -rf ~/Library/Application\ Support/Code/CachedExtensions/visualstudioexptteam.vscodeintellicode-*

# Clear Pylance cache (if using Pylance)
rm -rf ~/Library/Application\ Support/Code/CachedExtensions/ms-python.vscode-pylance-*
```

Then reload VS Code.

## Method 6: Check Python Interpreter

1. Press `Cmd+Shift+P`
2. Type: `Python: Select Interpreter`
3. Make sure a valid Python 3.8+ is selected
4. If not, select one or add a new one

## Method 7: Disable IntelliCode Completely (If Not Needed)

If you don't need IntelliCode features:

1. Press `Cmd+Shift+P`
2. Type: `Preferences: Open Settings (JSON)`
3. Add this line:
   ```json
   "python.analysis.intellicodeEnabled": false
   ```
4. Save and reload

