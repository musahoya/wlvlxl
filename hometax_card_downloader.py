import asyncio
import sys
from playwright.async_api import async_playwright

# 홈택스 자동 로그인 및 신용카드 내역 다운로드 프로그램
# 주의: 홈택스 보안 정책에 따라 자동화가 차단될 수 있으며, 
# 실제 사용 시에는 사용자의 PC 환경(보안 프로그램 설치 등)이 필요할 수 있습니다.

async def run(user_id, user_pw):
    async with async_playwright() as p:
        # 브라우저 실행 (headless=False로 설정하여 동작 과정을 확인하는 것을 권장합니다)
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        print("1. 홈택스 로그인 페이지 접속 중...")
        await page.goto("https://hometax.go.kr/websquare/websquare.html?w2xPath=/ui/pp/index_pp.xml&initPage=agitxLogin")
        
        # 페이지 로딩 대기
        await page.wait_for_selector("#mf_txppWframe_iptUserId")

        print("2. 아이디/비밀번호 입력 중...")
        await page.fill("#mf_txppWframe_iptUserId", user_id)
        await page.fill("#mf_txppWframe_iptUserPw", user_pw)
        
        print("3. 로그인 버튼 클릭...")
        await page.click("#mf_txppWframe_anchor25")

        # 로그인 후 메인 페이지 이동 대기
        try:
            await page.wait_for_selector("#mf_wfHeader_hdGroup001", timeout=10000)
            print("로그인 성공!")
        except:
            print("로그인 실패 또는 추가 인증(간편인증 등)이 필요합니다.")
            # 여기서 멈추고 사용자가 수동으로 인증을 완료할 때까지 기다릴 수도 있습니다.
            # await page.wait_for_selector("#mf_wfHeader_hdGroup001", timeout=60000)

        print("4. 사업용 신용카드 매입내역 조회 페이지로 이동...")
        # 직접 메뉴 경로를 클릭하거나 URL로 이동
        # 사업용신용카드 매입내역 조회 메뉴 코드: FN0206 (변동 가능)
        await page.goto("https://hometax.go.kr/websquare/websquare.html?w2xPath=/ui/pp/index_pp.xml&menuCd=FN0206")
        
        await page.wait_for_load_state("networkidle")

        print("5. 조회 조건 설정 및 조회...")
        # 예: 분기별 조회 또는 월별 조회 설정 (홈택스 UI에 따라 다름)
        # 이 부분은 홈택스 개편에 따라 선택자(Selector)가 자주 변경됩니다.
        # 현재 분기 조회 버튼 클릭 예시
        # await page.click("#btn_query") 

        print("6. 엑셀 다운로드 시도...")
        # 엑셀 다운로드 버튼 클릭 및 파일 저장
        # async with page.expect_download() as download_info:
        #     await page.click("#trigger_excel_down") # 실제 ID 확인 필요
        # download = await download_info.value
        # await download.save_as("hometax_credit_card_history.xlsx")
        
        print("작업이 완료되었습니다. (상세 조회 및 다운로드 로직은 UI 구조에 맞춰 조정이 필요합니다.)")
        
        # 브라우저를 바로 닫지 않고 확인 시간을 가짐
        await asyncio.sleep(5)
        await browser.close()

if __name__ == "__main__":
    # 실행 방법: python hometax_card_downloader.py 아이디 비밀번호
    if len(sys.argv) < 3:
        print("사용법: python hometax_card_downloader.py [ID] [PASSWORD]")
    else:
        asyncio.run(run(sys.argv[1], sys.argv[2]))
