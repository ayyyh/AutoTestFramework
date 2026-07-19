from playwright.sync_api import sync_playwright


def test_saucedemo_login():
    with sync_playwright() as p:
        # 启动浏览器（headless=False 能看到操作过程）
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 打开 SauceDemo 登录页面（这是一个真实的 UI 登录页面）
        page.goto("https://www.saucedemo.com/")
        print("✅ 页面已打开")

        # 填写用户名和密码（SauceDemo 的标准测试账号）
        page.fill("#user-name", "standard_user")
        page.fill("#password", "secret_sauce")
        print("✅ 已填写账号密码")

        # 点击登录按钮
        page.click("#login-button")
        print("✅ 已点击登录按钮")

        # 等待登录成功后页面跳转，检查是否显示商品列表
        page.wait_for_selector(".inventory_list", timeout=10000)
        print("✅ 登录成功，商品列表已显示")

        # 截图保存证据
        page.screenshot(path="saucedemo_login_success.png")
        print("✅ 截图已保存")

        browser.close()


if __name__ == "__main__":
    test_saucedemo_login()