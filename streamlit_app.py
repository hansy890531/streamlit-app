import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from streamlit.components.v1 import html
import json
import logging
import traceback
import uuid
from datetime import datetime
from typing import Dict, Any

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GoogleSheetsManager:
    def __init__(self):
        self.sh = self._connect_to_google_sheets()

    def _connect_to_google_sheets(self):
        try:
            logger.info("Google Sheets 연결 시도 중...")
            gcp_service_account = st.secrets["gcp_service_account"]
            credentials = Credentials.from_service_account_info(gcp_service_account, scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ])
            client = gspread.authorize(credentials)
            sh = client.open_by_key(st.secrets["sheets"]["sheet_key"])
            logger.info("Google Sheets 연결 성공")
            return sh
        except Exception as e:
            logger.error(f"Google Sheets 연결 실패: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def get_worksheet(self, name: str):
        return self.sh.worksheet(name)

    def get_current_reservations(self, worksheet, date: str, time: str) -> int:
        all_data = worksheet.get_all_values()
        headers = all_data.pop(0)
        df = pd.DataFrame(all_data, columns=headers)
        df['예약 인원'] = df['예약 인원'].astype(int)
        return df[(df['예약 날짜'] == str(date)) & (df['예약 시간'] == time)]['예약 인원'].sum()

class UserManager:
    def __init__(self, sheets_manager: GoogleSheetsManager):
        self.sheets_manager = sheets_manager

    def verify_user(self, user_id: str) -> bool:
        users_worksheet = self.sheets_manager.get_worksheet("Users")
        users_data = users_worksheet.get_all_values()
        users_df = pd.DataFrame(users_data[1:], columns=users_data[0])
        return user_id in users_df['TelegramID'].values

    def add_user_if_not_exists(self, user_data: Dict[str, Any]):
        users_worksheet = self.sheets_manager.get_worksheet("Users")
        users_data = users_worksheet.get_all_values()
        users_df = pd.DataFrame(users_data[1:], columns=users_data[0])
        
        if user_data['id'] not in users_df['TelegramID'].values:
            new_row = [user_data['id'], user_data['username'], user_data['first_name'], user_data['last_name']]
            users_worksheet.append_row(new_row)
            logger.info(f"새 사용자 추가됨: {user_data['username']}")

class ReservationManager:
    def __init__(self, sheets_manager: GoogleSheetsManager):
        self.sheets_manager = sheets_manager

    @staticmethod
    def generate_reservation_id() -> str:
        return str(uuid.uuid4())[:8]  # 8자리 고유 ID 생성

    def create_reservation(self, user_id: str, date: str, time: str, people: int, notes: str) -> str:
        worksheet = self.sheets_manager.get_worksheet("한남2_투어")
        current_reservations = self.sheets_manager.get_current_reservations(worksheet, date, time)
        max_capacity = 10
        
        if current_reservations + people > max_capacity:
            raise ValueError(f"예약 가능 인원 초과 (현재 예약: {current_reservations}명, 최대: {max_capacity}명)")
        
        reservation_id = self.generate_reservation_id()
        new_row = [reservation_id, user_id, str(date), time, str(people), notes, str(datetime.now())]
        worksheet.append_row(new_row)
        logger.info(f"새 예약 추가됨: {reservation_id}")
        return reservation_id

    def modify_reservation(self, reservation_id: str, user_id: str, new_date: str, new_time: str, new_people: int, new_notes: str):
        worksheet = self.sheets_manager.get_worksheet("한남2_투어")
        cell = worksheet.find(reservation_id)
        if not cell:
            raise ValueError("예약을 찾을 수 없습니다.")
        
        row = worksheet.row_values(cell.row)
        if row[1] != str(user_id):
            raise PermissionError("해당 예약에 대한 수정 권한이 없습니다.")
        
        current_reservations = self.sheets_manager.get_current_reservations(worksheet, new_date, new_time) - int(row[4])
        if current_reservations + new_people > 10:
            raise ValueError("예약 가능 인원을 초과했습니다.")
        
        worksheet.update_cell(cell.row, 3, str(new_date))
        worksheet.update_cell(cell.row, 4, new_time)
        worksheet.update_cell(cell.row, 5, str(new_people))
        worksheet.update_cell(cell.row, 6, new_notes)
        logger.info(f"예약 수정됨: {reservation_id}")

    def cancel_reservation(self, reservation_id: str, user_id: str):
        worksheet = self.sheets_manager.get_worksheet("한남2_투어")
        cell = worksheet.find(reservation_id)
        if not cell:
            raise ValueError("예약을 찾을 수 없습니다.")
        
        row = worksheet.row_values(cell.row)
        if row[1] != str(user_id):
            raise PermissionError("해당 예약에 대한 취소 권한이 없습니다.")
        
        worksheet.delete_row(cell.row)
        logger.info(f"예약 취소됨: {reservation_id}")

    def get_user_reservations(self, user_id: str) -> pd.DataFrame:
        worksheet = self.sheets_manager.get_worksheet("한남2_투어")
        data = worksheet.get_all_values()
        headers = data.pop(0)
        df = pd.DataFrame(data, columns=headers)
        return df[df['사용자 ID'] == str(user_id)]

def main():
    st.set_page_config(page_title="설명회 예약 시스템", layout="wide")
    
    # Telegram WebApp API 스크립트 추가
    html("""
        <script src="https://telegram.org/js/telegram-web-app.js"></script>
        <script>
            let tg = window.Telegram.WebApp;
            
            if (tg.initDataUnsafe.query_id) {
                tg.expand();
                
                // 사용자 정보 가져오기
                let user = tg.initDataUnsafe.user;
                let userData = {
                    id: user.id,
                    first_name: user.first_name,
                    last_name: user.last_name,
                    username: user.username,
                    language_code: user.language_code
                };
                
                // Streamlit에 사용자 정보 전달
                window.parent.postMessage({
                    type: "streamlit:setComponentValue",
                    value: JSON.stringify(userData)
                }, "*");
                
            } else {
                console.error("이 앱은 Telegram 내에서만 사용할 수 있습니다.");
            }
        </script>
    """, height=0)

    sheets_manager = GoogleSheetsManager()
    user_manager = UserManager(sheets_manager)
    reservation_manager = ReservationManager(sheets_manager)

    # 사용자 정보 받기 및 자동 로그인
    if 'user_data' not in st.session_state:
        user_data_raw = st.query_params.get("streamlit:componentValue")
        if user_data_raw:
            user_data = json.loads(user_data_raw)
            st.session_state.user_data = user_data
            user_manager.add_user_if_not_exists(user_data)
            if user_manager.verify_user(user_data['id']):
                st.session_state.logged_in = True
                logger.info(f"사용자 자동 로그인 성공: {user_data['username']}")
            else:
                st.session_state.logged_in = False
                logger.warning(f"未승인 사용자 접근: {user_data['username']}")
        else:
            st.session_state.logged_in = False
            logger.warning("사용자 정보를 가져올 수 없습니다.")

    st.session_state.logged_in = True

    
    # 메인 애플리케이션 (로그인 성공 시에만 표시)
    if st.session_state.get('logged_in', False):
        st.title("설명회 예약 시스템")
        st.write(f"환영합니다, {st.session_state.user_data['first_name']} {st.session_state.user_data['last_name']}님!")

        tab1, tab2, tab3 = st.tabs(["예약하기", "예약 수정", "예약 취소"])

        with tab1:
            st.header("예약하기")
            with st.form("reservation_form", clear_on_submit=True):
                date = st.date_input("예약 날짜")
                time = st.selectbox("예약 시간", ["10:30", "13:30", "16:00"])
                people = st.number_input("예약 인원", min_value=1, max_value=10, value=1)
                notes = st.text_area("기타 특이사항")
                submit_button = st.form_submit_button("예약하기")

            if submit_button:
                try:
                    reservation_id = reservation_manager.create_reservation(
                        st.session_state.user_data['id'], str(date), time, people, notes
                    )
                    st.success(f"예약이 완료되었습니다. 예약 번호: {reservation_id}")
                    
                    reservation_data = json.dumps({
                        "reservationId": reservation_id,
                        "userId": st.session_state.user_data['id'],
                        "date": str(date),
                        "time": time,
                        "people": people,
                        "notes": notes
                    })
                    
                    html(f"""
                        <script>
                            let reservation = {reservation_data};
                            console.log("Telegram에 전송할 데이터:", reservation);
                            try {{
                                tg.sendData(JSON.stringify(reservation));
                                console.log("Telegram 데이터 전송 성공");
                            }} catch (error) {{
                                console.error("Telegram 데이터 전송 실패:", error);
                            }}
                            tg.close();
                        </script>
                    """, height=0)
                except Exception as e:
                    st.error(str(e))

        with tab2:
            st.header("예약 수정")
            reservation_id_to_modify = st.text_input("수정할 예약 번호를 입력하세요")
            if st.button("예약 조회"):
                try:
                    worksheet = sheets_manager.get_worksheet("한남2_투어")
                    cell = worksheet.find(reservation_id_to_modify)
                    if cell:
                        row = worksheet.row_values(cell.row)
                        if row[1] == str(st.session_state.user_data['id']):
                            st.write("현재 예약 정보:")
                            st.write(f"예약 번호: {row[0]}")
                            st.write(f"날짜: {row[2]}")
                            st.write(f"시간: {row[3]}")
                            st.write(f"인원: {row[4]}")
                            st.write(f"특이사항: {row[5]}")
                            
                            with st.form("modify_form"):
                                new_date = st.date_input("새 예약 날짜", value=datetime.strptime(row[2], "%Y-%m-%d").date())
                                new_time = st.selectbox("새 예약 시간", ["10:30", "13:30", "16:00"], index=["10:30", "13:30", "16:00"].index(row[3]))
                                new_people = st.number_input("새 예약 인원", min_value=1, max_value=10, value=int(row[4]))
                                new_notes = st.text_area("새 특이사항", value=row[5])
                                modify_button = st.form_submit_button("예약 수정")
                            
                            if modify_button:
                                try:
                                    reservation_manager.modify_reservation(
                                        reservation_id_to_modify,
                                        st.session_state.user_data['id'],
                                        str(new_date),
                                        new_time,
                                        new_people,
                                        new_notes
                                    )
                                    st.success("예약이 성공적으로 수정되었습니다.")
                                except Exception as e:
                                    st.error(str(e))
                        else:
                            st.error("해당 예약에 대한 수정 권한이 없습니다.")
                    else:
                        st.error("해당 예약 번호를 찾을 수 없습니다.")
                except Exception as e:
                    logger.error(f"예약 수정 중 오류 발생: {str(e)}")
                    logger.error(traceback.format_exc())
                    st.error(f"예약 수정 중 오류가 발생했습니다: {str(e)}")

        with tab3:
            st.header("예약 취소")
            reservation_id_to_cancel = st.text_input("취소할 예약 번호를 입력하세요")
            # 기존 예약 조회
            if st.button("내 예약 조회"):
                logger.info("기존 예약 조회 버튼 클릭됨")
                try:
                    user_reservations = reservation_manager.get_user_reservations(st.session_state.user_data['id'])
                    if user_reservations.empty:
                        logger.warning("예약 정보 없음")
                        st.warning('예약 정보가 없습니다.')
                    else:
                        st.dataframe(user_reservations)
                except Exception as e:
                    logger.error(f"예약 조회 중 오류 발생: {str(e)}")
                    logger.error(traceback.format_exc())
                    st.error(f"예약 조회 중 오류가 발생했습니다: {str(e)}")

            else:
                st.error("로그인에 실패했습니다. 텔레그램 미니앱을 통해 접속해주세요.")

if __name__ == "__main__":
    main()
    logger.info("앱 실행 완료")
