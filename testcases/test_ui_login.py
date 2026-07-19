import pytest
from playwright.sync_api import expect


def test_saucedemo_login(page):
    page.goto("https://www.saucedemo.com/")

    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()

    expect(page.locator(".inventory_list")).to_be_visible()
    expect(page).to_have_title("Swag Labs")