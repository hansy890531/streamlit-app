import streamlit as st
import streamlit.components.v1 as components
from streamlit_js_eval import streamlit_js_eval

# JavaScript 코드 작성
js_code = """
function getUserId() {
    Telegram.WebApp.ready();
    let tg = window.Telegram.WebApp;
    if (tg && tg.initDataUnsafe && tg.initDataUnsafe.user) {
        let userId = tg.initDataUnsafe.user.id;
        postEvent('getUserId', function() {
            console.log('User ID sent to parent:', userId);
        }, userId);
        return userId;
    } else {
        return 'No user data available';
    }
}

function postEvent(eventType, callback, eventData) {
    if (!callback) {
        callback = function () {};
    }
    if (eventData === undefined) {
        eventData = '';
    }
    console.log('[Telegram.WebView] > postEvent', eventType, eventData);

    if (window.TelegramWebviewProxy !== undefined) {
        TelegramWebviewProxy.postEvent(eventType, JSON.stringify(eventData));
        callback();
    }
    else if (window.external && 'notify' in window.external) {
        window.external.notify(JSON.stringify({eventType: eventType, eventData: eventData}));
        callback();
    }
    else if (isIframe) {
        try {
            var trustedTarget = 'https://hannam22.streamlit.app/;
            // For now we don't restrict target, for testing purposes
            trustedTarget = '*';
            if (window.parent !== window.top) {
                window.parent.parent.postMessage(JSON.stringify({eventType: eventType, eventData: eventData}), trustedTarget);
            } else {
                window.parent.postMessage(JSON.stringify({eventType: eventType, eventData: eventData}), trustedTarget);
            }
            callback();
        } catch (e) {
            callback(e);
        }
    }
    else {
        callback({notAvailable: true});
    }
}

getUserId();
"""

# streamlit_js_eval을 사용하여 JavaScript 코드 실행 및 결과 받기
result = streamlit_js_eval(js_expressions=js_code, want_output=True, key='js_eval')

def disp_result():
    to_display = f"JavaScript 결과는: {result}"
    st.write(to_display)

# 버튼을 클릭할 때 JavaScript 결과를 표시
st.button("JavaScript 결과 표시", on_click=disp_result)
