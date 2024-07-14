function sendValue(value) {
    Streamlit.setComponentValue(value);
}

function onRender(event) {
    if (!window.rendered) {
        const script = document.createElement('script');
        script.src = "https://telegram.org/js/telegram-webapp.js";
        script.async = true;
        document.body.appendChild(script);

        script.onload = () => {
            if (window.Telegram && window.Telegram.WebApp) {
                const webApp = window.Telegram.WebApp;
                webApp.ready();
                
                if (webApp.initDataUnsafe && webApp.initDataUnsafe.user) {
                    const userId = webApp.initDataUnsafe.user.id;
                    sendValue(userId);
                } else {
                    sendValue(null);
                }
            } else {
                sendValue(null);
            }
        };

        window.rendered = true;
    }
}

Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender);
Streamlit.setComponentReady();
Streamlit.setFrameHeight(100);