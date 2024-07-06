<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Telegram Web App</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <script>
        window.onload = function() {
            let tg = window.Telegram.WebApp;
            if (tg.initDataUnsafe.user) {
                let userData = {
                    id: tg.initDataUnsafe.user.id,
                    first_name: tg.initDataUnsafe.user.first_name,
                    last_name: tg.initDataUnsafe.user.last_name,
                    username: tg.initDataUnsafe.user.username,
                    language_code: tg.initDataUnsafe.user.language_code
                };
                console.log(userData);
                document.getElementById("user-info").innerText = JSON.stringify(userData, null, 2);

                // 사용자 정보를 부모 프레임에 전달
                window.parent.postMessage({
                    type: "userData",
                    data: userData
                }, "*");
            } else {
                console.error("사용자 정보를 가져올 수 없습니다.");
            }
        };

        window.addEventListener("message", (event) => {
            if (event.data.type === "userData") {
                const userData = event.data.data;
                console.log("Received user data:", userData);
            }
        });
    </script>
</head>
<body>
    <h1>Welcome to the Telegram Web App</h1>
    <pre id="user-info"></pre>
</body>
</html>
