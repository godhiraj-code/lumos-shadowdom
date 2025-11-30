from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import lumos
import time

def test_live():
    print("Starting Live Test...")
    options = Options()
    # options.add_argument("--headless") # Uncomment if you want headless
    
    try:
        driver = webdriver.Chrome(options=options)
        driver.get("http://watir.com/examples/shadow_dom.html")
        
        print("Page loaded. Attempting to find shadow element...")
        
        # The page has a shadow host #shadow_host which contains a span with text
        # Let's try to find the text inside the shadow root
        
        # 1. Test find_shadow (Monkey Patch)
        # Structure: #shadow_host -> #shadow_content -> span
        # Note: The example site structure might vary, this is a guess based on common examples
        # Let's use the Smart Search first as it's more robust to unknown structures
        
        print("Testing Smart Search (find_shadow_text)...")
        try:
            # There is usually some text like "some text" or "nested text"
            # Let's try to find the text "nested text" which is common in this example
            el = driver.find_shadow_text("nested text")
            print(f"SUCCESS: Found element with text: {el.text}")
            # Highlight the element to make it visible
            driver.execute_script("arguments[0].style.border='3px solid red'", el)
            time.sleep(2) # Wait to see the result
        except Exception as e:
            print(f"Smart Search Failed: {e}")

        # 2. Test Path Search
        print("Testing Path Search (find_shadow)...")
        try:
            # Assuming structure: #shadow_host > span
            # You might need to adjust this path based on the actual site structure
            el = driver.find_shadow("#shadow_host > span")
            print(f"SUCCESS: Found element by path: {el.text}")
            # Highlight the element
            driver.execute_script("arguments[0].style.border='3px solid blue'", el)
            time.sleep(2) # Wait to see the result
        except Exception as e:
            print(f"Path Search Failed: {e}")

    except Exception as e:
        print(f"Global Error: {e}")
    finally:
        if 'driver' in locals():
            time.sleep(2) # Final wait before closing
            driver.quit()
            print("Driver closed.")

def test_selectorshub():
    print("\nStarting SelectorsHub Test...")
    options = Options()
    
    try:
        driver = webdriver.Chrome(options=options)
        driver.get("https://selectorshub.com/xpath-practice-page/")
        driver.maximize_window()
        
        print("Page loaded. Scrolling down to Shadow DOM section...")
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(1)
        
        # SelectorsHub has a shadow dom with input fields
        # Let's try to find the "Enter email" field inside shadow dom
        
        print("Testing Smart Search (find_shadow_text)...")
        try:
            # Searching for the label or placeholder text might be tricky if it's an input
            # Let's try to find an element that contains text "Enter email"
            # Or we can try to find the input directly if we knew the path.
            # Let's try to find the "Love Pizza" text which is often in a shadow dom example there
            # Or "Enter email" placeholder? find_by_text works on innerText.
            # Let's try to find the "Pizza" text which is usually in the shadow dom example.
            el = driver.find_shadow_text("Pizza") 
            print(f"SUCCESS: Found element with text: {el.text}")
            driver.execute_script("arguments[0].style.border='3px solid red'", el)
            time.sleep(2)
        except Exception as e:
            print(f"Smart Search Failed: {e}")

        print("Testing Path Search (find_shadow)...")
        try:
            # User provided path
            long_path = "html > body.wp-singular.page-template-default.page.page-id-1097.wp-custom-logo.wp-embed-responsive.wp-theme-hello-elementor.wp-child-theme-hello-theme-child-master.hello-elementor-default.elementor-default.elementor-kit-5.elementor-page.elementor-page-1097.e--ua-blink.e--ua-chrome.e--ua-webkit > main#content > div.page-content > div.elementor.elementor-1097 > div.elementor-element.elementor-element-8f72400.e-flex.e-con-boxed.e-con.e-parent.e-lazyloaded > div.e-con-inner > div.elementor-element.elementor-element-3e79790.e-con-full.e-flex.e-con.e-child > div.elementor-element.elementor-element-617b7ae.e-con-full.e-flex.e-con.e-child > div.elementor-element.elementor-element-6fef204.result.elementor-widget.elementor-widget-html > div.elementor-widget-container > div#userName"
            
            # The user's path ends at #userName, which is the HOST.
            # We need to target the input inside it. The previous test used #userName > #kils
            # So we append > #kils to the user's path
            full_path = long_path + " > #kils"
            
            print(f"Testing with User's Long Path...")
            el = driver.find_shadow(full_path)
            print(f"SUCCESS: Found element by path: {el.get_attribute('id')}")
            el.clear()
            el.send_keys("Long Path Works!")
            driver.execute_script("arguments[0].style.border='3px solid blue'", el)
            time.sleep(1)
        except Exception as e:
            print(f"Long Path Search Failed: {e}")

        print("Testing Correct Fields...")
        try:
            # 1. Username Field
            # Host: #userName, Input ID: #kils
            print("Entering 'User' into Username field...")
            user_input = driver.find_shadow("div#userName > #kils")
            user_input.clear()
            user_input.send_keys("User")
            driver.execute_script("arguments[0].style.border='3px solid green'", user_input)
            
            # 2. Pizza Field
            # User provided path: div#userName > div#app2 > input#pizza
            print("Entering 'Margherita' into Pizza Name field using User Path...")
            pizza_path = "div#userName > div#app2 > input#pizza"
            pizza_input = driver.find_shadow(pizza_path)
            pizza_input.clear()
            pizza_input.send_keys("Margherita")
            driver.execute_script("arguments[0].style.border='3px solid orange'", pizza_input)

            # Capture screenshot
            driver.save_screenshot("c:/shadowroot/evidence_user_path.png")
            print("SUCCESS: Entered values into both fields. Screenshot saved to c:/shadowroot/evidence_user_path.png")
            time.sleep(2)
        except Exception as e:
            print(f"Field Test Failed: {e}")

    except Exception as e:
        print(f"Global Error: {e}")
    finally:
        if 'driver' in locals():
            time.sleep(2)
            driver.quit()
            print("Driver closed.")

if __name__ == "__main__":
    test_live()
    test_selectorshub()
