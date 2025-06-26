"""
E2E UI Tests for Streamlit App using Selenium and Pytest.
"""

import time
import pytest
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="session", autouse=True)
def streamlit_server():
    proc = subprocess.Popen(["streamlit", "run", "streamlit_app.py"])
    time.sleep(5)  
    yield
    proc.terminate()

@pytest.fixture(scope="module")
def driver():
    """Initialize and teardown the Chrome WebDriver."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

def wait_for_app_ready(driver):
    """Wait for the Streamlit app to load completely."""
    driver.get("http://localhost:8501")
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Clash of Clans Setup Calculator')]"))
    )
    time.sleep(1)  # Give the layout time to stabilize


def test_page_load(driver):
    wait_for_app_ready(driver)
    assert "Streamlit" in driver.title


def test_number_input_fields(driver):
    wait_for_app_ready(driver)
    inputs = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='number']"))
    )
    assert len(inputs) == 30


def test_apply_button(driver):
    wait_for_app_ready(driver)
    
    apply_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class, 'stButton') and .//text()[contains(., 'Apply Level Changes')]]//button")
        )
    )

    apply_btn.click()
    time.sleep(1)
    assert apply_btn.is_displayed()



def select_setup(driver, label_text: str):
    formatted_label = label_text.replace("_", " ").title()

    radio_labels = driver.find_elements(
        By.CSS_SELECTOR,
        'label[data-baseweb="radio"]'
    )

    for label in radio_labels:
        try:
            text_elem = label.find_element(By.CSS_SELECTOR, 'div[data-testid="stMarkdownContainer"] > p')
            if text_elem.text.strip() == formatted_label:
                label.click()
                time.sleep(1)
                label.click()
                return
        except Exception:
            continue

    raise AssertionError(f"Radio button with label '{formatted_label}' not found.")


@pytest.mark.parametrize("setup_option", ["fireball", "spiky_ball", "royal_champion"])
def test_dataframe_columns(driver, setup_option):
    EXPECTED_COLUMNS = []
    if setup_option == "fireball":
        EXPECTED_COLUMNS = ['defense', 'lvl', 'max hp', 'alone', 'giant arrow', 'spiky ball']
    elif setup_option == "spiky_ball":
        EXPECTED_COLUMNS = ['defense', 'lvl', 'max hp', 'alone', 'giant arrow']
    elif setup_option == "royal_champion":
        EXPECTED_COLUMNS = ['defense', 'lvl', 'max hp', 'alone', 'with shield', '1 earthquake', 'shield + 1 earthquake']

    driver.get("http://localhost:8501")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="radiogroup"]'))
    )

    select_setup(driver, setup_option)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'table thead tr'))
    )

    header_cells = driver.find_elements(By.CSS_SELECTOR, 'table thead tr th')
    headers = [cell.text.strip().lower() for cell in header_cells]

    for expected in EXPECTED_COLUMNS:
        assert expected in headers, f"Missing expected column: {expected}"


@pytest.mark.usefixtures("driver")
def test_th_defense_button(driver):
    EXPECTED_DEFENSES = [
        "air_defense", "air_sweeper", "archer_tower", "bomb_tower", "builder_hut",
        "cannon", "clan_castle", "eagle_artillery", "hidden_tesla", "inferno_tower",
        "mortar", "scattershot", "townhall", "wizard_tower", "xbow"]
    EXPECTED_LEVELS = [12, 7, 20, 9, 4, 20, 10, 5, 13, 8, 14, 3, 14, 14, 9]
    wait_for_app_ready(driver)

    # Click "TH 14" button
    buttons = driver.find_elements(By.TAG_NAME, "button")
    th14_button = next(btn for btn in buttons if "TH 14" in btn.text)
    th14_button.click()

    # Wait for session state update
    time.sleep(3)

    table = driver.find_element(By.TAG_NAME, "table")
    rows = table.find_elements(By.TAG_NAME, "tr")

    actual_data = []
    for row in rows[1:]:
        cells = row.find_elements(By.TAG_NAME, "td")
        actual_data.append((cells[0].text.strip(), int(cells[1].text.strip())))

    # Validate result
    expected_data = list(zip(EXPECTED_DEFENSES, EXPECTED_LEVELS))
    assert actual_data == expected_data, f"Expected {expected_data}, got {actual_data}"

