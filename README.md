# Lumos ShadowDOM 🪄

**Automate Shadow DOM elements in Selenium with zero headache.**

Shadow DOMs are tricky. They hide elements from standard Selenium commands. `lumos-shadowdom` solves this by letting you traverse nested shadow roots automatically using simple paths or even just text.

---

## 🚀 Quick Start

### 1. Install
```bash
pip install lumos-shadowdom
```

### 2. Use it in your code
Lumos adds new superpowers to your Selenium driver automatically!

```python
from selenium import webdriver
import lumos  # <--- Import this to activate magic!

driver = webdriver.Chrome()
driver.get("https://example.com")

# 🟢 Scenario 1: You know the path (or found it using our tool below)
# Syntax: "host-element > nested-host > target-element"
driver.find_shadow("my-app > settings-panel > button#save").click()

# 🟢 Scenario 2: Find ALL matching elements in shadow DOM
buttons = driver.find_all_shadow("nav-menu > button.action")
for btn in buttons:
    print(btn.text)

# 🟢 Scenario 3: You just want to find a button with specific text
# This scans the ENTIRE page (including all shadow roots) for you.
driver.find_shadow_text("Confirm Purchase").click()
```

---

## 🕵️ How to Find the Path? (The Magic Tool)

Don't waste time inspecting elements manually. Use our **Discovery Tool** to generate the exact path instantly.

1.  Open your website in Chrome.
2.  Open **DevTools** (Press `F12` or Right Click -> Inspect).
3.  Go to the **Console** tab.
4.  **Paste** the script below and hit **Enter**.
5.  Hold **`Alt`** and **Click** on any element in the page.
6.  The Console will show you the **Short Path** and **Long Path**. Copy the "Short Path" and use it in `driver.find_shadow()`.

### Copy this Script:
```javascript
// Lumos Discovery Tool v2.0
// Paste this into Chrome Console, then Alt + Click any element.
document.addEventListener('click', function(e) {
    if (!e.altKey) return; 
    e.preventDefault();
    e.stopImmediatePropagation();

    // 1. Get the real target (piercing Shadow DOM)
    let composed = e.composedPath();
    let target = composed[0];
    
    let fullPath = [];
    let shortPath = [];
    let currentScope = [];

    // 2. Traverse up the tree
    for (let i = 0; i < composed.length; i++) {
        let node = composed[i];

        // Stop at document root
        if (node.nodeType !== Node.ELEMENT_NODE && !(node instanceof ShadowRoot)) {
             if (currentScope.length > 0) {
                 fullPath.unshift(currentScope.join(' '));
                 shortPath.unshift(getShortSelector(currentScope));
             }
             break;
        }

        // Handle Shadow Root Boundary
        if (node instanceof ShadowRoot) {
            fullPath.unshift(currentScope.join(' '));
            shortPath.unshift(getShortSelector(currentScope));
            currentScope = [];
            continue;
        }

        // Build Selector for current node
        let selector = node.tagName.toLowerCase();
        if (node.id) {
            selector += '#' + node.id;
        } else if (node.className && typeof node.className === 'string') {
            selector += '.' + node.className.trim().split(/\s+/).join('.');
        }
        currentScope.unshift(selector);
    }
    
    function getShortSelector(scope) {
        let short = [];
        for (let j = scope.length - 1; j >= 0; j--) {
            short.unshift(scope[j]);
            if (scope[j].includes('#')) break; // Stop at ID for brevity
        }
        return short.join(' ');
    }
    
    console.log(`%c 🪄 Lumos Path Discovered!`, 'background: #222; color: #bada55; font-size: 14px; padding: 4px;');
    console.log(`%c Short Path:`, 'font-weight: bold; color: #007bff;', shortPath.join(' > '));
    console.log(`%c Long Path: `, 'color: #666;', fullPath.join(' > '));
}, true);
```

---

## 📚 API Reference

### `driver.find_shadow(path: str, timeout: int = 10) -> WebElement`
Finds a single element inside nested shadow DOMs.
*   **path**: A string describing the path to the element. Use `>` to separate shadow boundaries.
    *   Example: `user-profile > #settings > input.name`
    *   Means: Find `user-profile`, enter its shadow root, find `#settings`, enter its shadow root, find `input.name`.
*   **timeout**: Seconds to wait for element (default: 10).
*   **Returns**: The matching WebElement.

### `driver.find_all_shadow(path: str, timeout: int = 10) -> List[WebElement]`
Finds **ALL** elements matching the path inside nested shadow DOMs.
*   **path**: Same syntax as `find_shadow`. The last selector matches multiple elements.
    *   Example: `app-root > nav-menu > button` returns all buttons in the nav.
*   **Returns**: List of matching WebElements (may be empty).

### `driver.find_shadow_text(text: str, timeout: int = 10) -> WebElement`
Recursively searches **every** shadow root in the DOM for an element containing the specified text.
*   **text**: The text to look for (case-sensitive).
*   **Returns**: The first matching WebElement found.

---

## ❓ FAQ

**Q: Why do I need this?**
A: Standard `driver.find_element()` cannot "see" inside a Shadow DOM. You usually have to write complex code to get the shadow root, then find the element, then repeat for nested roots. Lumos does this in one line.

**Q: Does it work with Selenium 3?**
A: Yes! It is fully compatible with Selenium 3.141.0 and Selenium 4+.

**Q: The Discovery Tool shows a path, but Lumos can't find it.**
A: 
1. Ensure the element is visible on the screen.
2. If the path is very long, try using the "Short Path" provided by the tool.
3. Check if the element is inside an `iframe`. Lumos currently supports Shadow DOM, but `iframe` support is separate (you must switch to the iframe first).

---

## ⚠️ Limitations & Edge Cases

### 1. Shadow DOM inside `<iframe>`
Lumos **cannot** automatically cross `<iframe>` boundaries because they are separate documents.
**Solution**: Switch to the iframe first using Selenium, then use Lumos.

```python
# 1. Switch to the iframe
iframe = driver.find_element(By.ID, "my-frame")
driver.switch_to.frame(iframe)

# 2. Now use Lumos inside the iframe
driver.find_shadow("host-inside-frame > button").click()
```

### 2. Closed Shadow Roots
Lumos cannot access Shadow DOMs created with `mode='closed'`. This is a browser security limitation that no tool can bypass standardly.

---

**Author**: Dhiraj
**License**: MIT

