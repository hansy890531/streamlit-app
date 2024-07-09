import streamlit as st
import streamlit.components.v1 as components
from streamlit_js_eval import streamlit_js_eval

# Telegram Web App JavaScript를 로드하는 HTML 코드
telegram_script = """

<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script>
      // Helper functions
      function setCookie(cname, cvalue, exdays) {
        const d = new Date();
        d.setTime(d.getTime() + (exdays*24*60*60*1000));
        let expires = "expires="+ d.toUTCString();
        document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
      }

      function getCookie(cname) {
        let name = cname + "=";
        let decodedCookie = decodeURIComponent(document.cookie);
        let ca = decodedCookie.split(';');
        for(let i = 0; i <ca.length; i++) {
          let c = ca[i];
          while (c.charAt(0) == ' ') {
            c = c.substring(1);
          }
          if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
          }
        }
        return "";
      }


      const copyToClipboard = function (textToCopy, onSuccess) {
        console.log('Copying to clipboard...')
        navigator.clipboard.writeText(textToCopy).then(function() {
              /* clipboard successfully set */
              console.log('Copy succeeded!')
              onSuccess()
            }, function() {
              /* clipboard write failed */
              console.log('Copy failed')
        });
      };

      const bsButton = function (title) {
        console.log('Showing a button..')
        setFrameHeight(100);
        //const bdy = document.querySelector("body")
        document.head.insertAdjacentHTML("beforeEnd",`
          <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.1.1/css/bootstrap.min.css">
        `)
        document.body.insertAdjacentHTML("beforeEnd",`
          <button class="btn btn-secondary btn-block" onclick="sendDataToPython({value: true, dataType: 'json'});">${title}</button>
        `)
        return false;
        
      };

      // https://stackoverflow.com/questions/11042212/ff-13-ie-9-json-stringify-geolocation-object
      function getLocation()  {
          return new Promise((resolve, reject) => {
              if (navigator.geolocation) {
                  navigator.geolocation.getCurrentPosition((position) =>
                      resolve({
                          coords: {
                              accuracy: position.coords.accuracy,
                              altitude: position.coords.altitude,
                              altitudeAccuracy: position.coords.altitudeAccuracy,
                              heading: position.coords.heading,
                              latitude: position.coords.latitude,
                              longitude: position.coords.longitude,
                              speed: position.coords.speed,
                          },
                          timestamp: position.timestamp,
                      }),
                  );
              } else {
                  reject(new Error('Browser does not support geolocation!'));
              }
          });
      }
      
      // ----------------------------------------------------
      // Just copy/paste these functions as-is:

      function sendMessageToStreamlitClient(type, data) {
        var outData = Object.assign({
          isStreamlitMessage: true,
          type: type,
        }, data);
        window.parent.postMessage(outData, "*");
      }

      function init() {
        sendMessageToStreamlitClient("streamlit:componentReady", {apiVersion: 1});
      }

      function setFrameHeight(height) {
        sendMessageToStreamlitClient("streamlit:setFrameHeight", {height: height});
      }

      // The `data` argument can be any JSON-serializable value.
      function sendDataToPython(data) {
        sendMessageToStreamlitClient("streamlit:setComponentValue", data);
      }


      // ----------------------------------------------------
      // Now modify this part of the code to fit your needs:

      var data_from_streamlit = ""
      // data is any JSON-serializable value you sent from Python,
      // and it's already deserialized for you.
      function onDataFromPython(event) {
        if (event.data.type !== "streamlit:render") return;
        new_value = event.data.args.js_expressions;  // Access values sent from Python here!
        if (new_value !== data_from_streamlit)
        {
          data_from_streamlit = new_value
          want_output = event.data.args.hasOwnProperty('want_output') ? event.data.args.want_output : true 
          console.log("Evaluating: "+data_from_streamlit)
          result = eval(data_from_streamlit)
          ret_val = want_output ? result : 'No output requested'
          if(want_output) Promise.resolve(ret_val).then(function(value) {
            console.log('Outputting '+value)
            sendDataToPython({value: value, dataType: "json"});
          })
          
        }
      }

      
      // Hack to autoset the iframe height.
      window.addEventListener("load", function() {
        // Hook things up!
        window.addEventListener("message", onDataFromPython);
        init();
        window.setTimeout(function() {
          setFrameHeight(document.documentElement.clientHeight) //
        }, 0);
      });

      // Optionally, if the automatic height computation fails you, give this component a height manually
      // by commenting out below:
      //setFrameHeight(0);
</script>
"""

# HTML 컴포넌트를 사용하여 스크립트 삽입
components.html(telegram_script, height=0)

# 나머지 Streamlit 앱 코드
st.title("Telegram Web App 통합")
st.write("Telegram Web App 스크립트가 로드되었습니다.")


js_code = """
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
        console.log(userData);
        return JSON.stringify(userData);  // JSON 문자열로 변환하여 반환
    }
    return 'No user data available';
}
getUserData();
"""

# streamlit_js_eval을 사용하여 JavaScript 코드 실행 및 결과 받기
result = streamlit_js_eval(js_expressions=js_code, want_output=True, key='js_eval2')

def disp_result():
    if result:
        st.write("Telegram 사용자 정보: ", result)
    else:
        st.write("사용자 정보를 가져올 수 없습니다.")

# 버튼을 클릭할 때 JavaScript 결과를 표시
st.button("Telegram 사용자 정보 표시", on_click=disp_result)
