function onDataFromPython(event) {
    const userDiv = document.getElementById("user-data");
    const data = event.detail;
    
    // Display user data
    if (userDiv) {
        userDiv.innerText = JSON.stringify(data.args);
    }
}

function sendUserDataToStreamlit(userData) {
    Streamlit.setComponentValue(userData);
}

// Assuming this function gets called with actual user data from Telegram Web App
function onTelegramUserDataReceived(userData) {
    sendUserDataToStreamlit(userData);
}

function getUserId() {
    const tg = window.Telegram.WebApp;
    if (tg.initDataUnsafe.user) {
        const userData = {
            id: tg.initDataUnsafe.user.id,
            first_name: tg.initDataUnsafe.user.first_name,
            last_name: tg.initDataUnsafe.user.last_name,
            username: tg.initDataUnsafe.user.username,
            language_code: tg.initDataUnsafe.user.language_code
        };
        document.getElementById("user-info").innerText = JSON.stringify(userData, null, 2);
        onTelegramUserDataReceived(userData); // userData 객체를 전달
        return userData; // userData 객체 반환
    } else {
        console.error("사용자 정보를 가져올 수 없습니다.");
    }
}

Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onDataFromPython);
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, () => {
    const userData = getUserId();
    if (userData) {
        Streamlit.setComponentValue(userData);
    }
});
Streamlit.setComponentReady();
Streamlit.setFrameHeight(500);
