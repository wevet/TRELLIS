import gradio as gr
import time
import threading


class AppHelper:

    K_AUDIO_URL = "https://www.myinstants.com/media/sounds/ding-sound-effect_2.mp3"

    def __init__(self):
        self.alert_box = gr.HTML("")
        self.sound = gr.Audio(visible=False, autoplay=True)
        pass


    def clear_alert_async(self):
        """ 10秒後にUIを削除する（非同期処理）"""

        threading.Thread(target=self.delayed_clear_alert, daemon=True).start()


    def delayed_clear_alert(self):
        time.sleep(10)
        if self.alert_box:
            self.alert_box.render = False
            print("alert box clear => {}".format(self.alert_box))

        if self.sound:
            self.sound.clear()
            print("sound clear {}".format(self.sound))


    def show_alert_image_notify(self, message, status, output_buf, video_output):
        if output_buf is None or video_output is None:
            print("not valid buf or video")
            return "", None
        return self.show_alert_notify(message, status)


    def show_alert_notify(self, message, status="info"):
        """
        Gradio のネイティブ通知を使って、アラートを表示する。
        :param message: 表示するメッセージ
        :param status: "info", "warning", "error" のいずれか
        """
        if status == "info":
            return gr.Info(message), self.K_AUDIO_URL
        elif status == "warning":
            return gr.Warning(message), self.K_AUDIO_URL
        elif status == "error":
            return gr.Error(message), self.K_AUDIO_URL
        else:
            return gr.Info(message), self.K_AUDIO_URL  # デフォルトは info


    def show_alert(self, message):
        html_content = f"""
        <div id="custom-alert" style="
            position: fixed;
            top: 50px;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: #ffcc00;
            padding: 15px 30px;
            border-radius: 8px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
            font-size: 18px;
            font-weight: bold;
            z-index: 10000;
            display: flex;
            align-items: center;
            gap: 10px;
        ">
            ✅ {message}
        </div>
        <script>
            (function() {{
                console.log("MutationObserver setup started.");
    
                let observer = new MutationObserver((mutations, obs) => {{
                    let alertBox = document.getElementById("custom-alert");
                    if (alertBox) {{
                        console.log("Alert box detected! Setting timeout for removal.");
    
                        setTimeout(() => {{
                            alertBox.remove();
                            console.log("Alert box removed.");
                        }}, 10000);
    
                        obs.disconnect();
                    }}
                }});
    
                observer.observe(document.body, {{
                    childList: true,
                    subtree: true
                }});
            }})();
        </script>
        """

        return html_content, self.K_AUDIO_URL


