import streamlit as st

def main():
    st.title("Telegram Web App Integration")

    # Embedding the Telegram Web App HTML
    st.components.v1.html("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Telegram Web App</title>
            <script src="https://telegram.org/js/telegram-web-app.js"></script>
        </head>
        <body>
            <h1>Telegram Web App</h1>
            <div id="user-info">사용자 정보 로딩 중...</div>
        
            <script>
                function getUserData() {
                    let tg = window.Telegram.WebApp;
                    if (tg && tg.initDataUnsafe && tg.initDataUnsafe.user) {
                        let userData = {
                            id: tg.initDataUnsafe.user.id,
                            first_name: tg.initDataUnsafe.user.first_name,
                            last_name: tg.initDataUnsafe.user.last_name,
                            username: tg.initDataUnsafe.user.username,
                            language_code: tg.initDataUnsafe.user.language_code
                        };
                        document.getElementById("user-info").innerText = JSON.stringify(userData, null, 2);
                        
                        // Send message to Streamlit app
                        window.parent.postMessage(JSON.stringify(userData), '*');
                    } else {
                        console.error("사용자 정보를 가져올 수 없습니다.");
                        document.getElementById("user-info").innerText = "사용자 정보를 가져올 수 없습니다.";
                    }
                }
        
                window.onload = function() {
                    getUserData();
                };
        
                window.Telegram.WebApp.onEvent('viewportChanged', function() {
                    getUserData();
                });
            </script>
        </body>
        </html>
    """)

if __name__ == "__main__":
    main()
