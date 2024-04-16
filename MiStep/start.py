import os,re
from mi_step import MiFit
import gradio as gr
import time

def pid_init():
    pidd = "log/pid"
    if not os.path.isdir(pidd):
        os.makedirs(pidd)
    # if len(os.listdir(pidd)) == 0:
    with open(f"log/pid/{os.getpid()}", "w") as fp:
        fp.write("")

class GradioMiFit():
    def __init__(self) -> None:
        self.stop_task = False
        self.mifit = MiFit()

    def del_res(self,a,b,c):
        return gr.Text.update(value=""),gr.Text.update(value=""),gr.Text.update(value="")

    def mode(self,a):
        if a == "手动":
            return gr.Dropdown.update(visible=False), gr.Dropdown.update(visible=False),gr.Button.update(visible=False)
        elif a == "自动化":
            return gr.Dropdown.update(visible=True), gr.Dropdown.update(visible=True),gr.Button.update(visible=True)

    def unlogin(self):
        return "账号登出成功",\
        gr.Text.update(visible=True),gr.Text.update(visible=True),\
        gr.Button.update(visible=True),gr.Button.update(visible=True),\
        gr.Text.update(visible=False),gr.Button.update(visible=False),\
        gr.Button.update(visible=False),gr.Button.update(visible=False),gr.Radio.update(visible=False),\
        gr.Dropdown.update(visible=False),gr.Dropdown.update(visible=False)

    def login(self,user,passwd):
        res = self.mifit.login_info(user,passwd)
        if "None" in res:# 输出框/用户名/密码/登录按钮/清空按钮/步数/确定按钮/注销按钮/模式/时间1/时间2
            return "账号或者密码未输入",\
                    gr.Text.update(visible=True),gr.Text.update(visible=True),\
                    gr.Button.update(visible=True),gr.Button.update(visible=True),\
                    gr.Text.update(visible=False),gr.Button.update(visible=False),\
                    gr.Button.update(visible=False),gr.Radio.update(visible=False),\
                    gr.Dropdown.update(visible=False),gr.Dropdown.update(visible=False),\
                    gr.Button.update(visible=False)
        elif "Fail" in res:
            return "登录失败，请检查账号密码!",\
                    gr.Text.update(visible=True),gr.Text.update(visible=True),\
                    gr.Button.update(visible=True),gr.Button.update(visible=True),\
                    gr.Text.update(visible=False),gr.Button.update(visible=False),\
                    gr.Button.update(visible=False),gr.Radio.update(visible=False),\
                    gr.Dropdown.update(visible=False),gr.Dropdown.update(visible=False),\
                    gr.Button.update(visible=False)
        elif "Sucess" in res:
            return "登录成功，请输入步数准备起飞~",\
                    gr.Text.update(visible=False),gr.Text.update(visible=False),\
                    gr.Button.update(visible=False),gr.Button.update(visible=False),\
                    gr.Text.update(visible=True),gr.Button.update(visible=True),\
                    gr.Button.update(visible=True),gr.Radio.update(visible=True),\
                    gr.Dropdown.update(visible=False),gr.Dropdown.update(visible=False),\
                    gr.Button.update(visible=False)

    def stop(self):
        self.stop_task = True
    def run_step(self, mode, user,passwd, step=10000, time_min="9:00", time_max="21:00", interval=1):
        if int(step) <= 90000:
            if mode == "手动":
                return self.mifit.getBeijinTime(user, step, step)
            elif mode == "自动化":
                time_min_hour = int(time_min.split(":")[0])
                time_max_hour = int(time_max.split(":")[0])
                if time_min_hour >= time_max_hour:
                    return "时间设置错误"
                else:
                    count = time_max_hour - time_min_hour
                    num_step = int(step) / count
                    init_step = 0
                    current_hour = time_min_hour
                    print("开始执行自动化任务中...")
                    while not self.stop_task and current_hour < time_max_hour:
                        init_step += num_step
                        print(f"当前时间：{current_hour}:00 模拟步数 {int(init_step)} ")
                        self.mifit.login_info(user,passwd)
                        self.mifit.getBeijinTime(user, init_step, init_step)
                        current_hour += interval
                        time.sleep(interval * 10)
                    return "自动化任务执行完毕"
        else:
            return "步数设置不可超出【9W】，请重新输入！！"
    def init_ui(self):
        with gr.Blocks(title="MiFit-Actions") as demo:
            # gr.Markdown("""
            #             <p align="center"><img src='file/imgs/mt_logo.png' alt='image One' style="height: 200px"/><p>""")
            gr.Markdown("""<center><font size=8>微步</center>""")
            gr.Markdown(
                """\
                        <center><font size=3>使用最初的小米运动软件[现在改为Zepp Life]模拟步数，同步至微信运动，仅支持之前手机号码注册的小米运动APP。[自动化任务存在问题，待优化...]</center>""")
            unlogin_btn = gr.Button("注销",variant="primary",visible=False)

            with gr.Row():
                input_user = gr.Text("",label="用户名",placeholder="请输入用户名",show_label=True)
                input_pwd = gr.Text("",label="密码",placeholder="请输入密码",show_label=True)
            with gr.Row():
                login_btn = gr.Button("登录",variant="primary")
                del_button = gr.Button("清空",variant="primary")
            with gr.Row():
                input_step = gr.Text("8000",label="步数",placeholder="请输入步数（建议2-3w即可）",show_label=True,visible=False,scale=4)
                input_mode = gr.Radio(["手动","自动"],value="手动",label="模式选择",visible=False,scale=1)
            with gr.Row():
                time_min = gr.Dropdown(["9:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00","17:00","18:00","19:00","20:00","21:00","22:00"],value="9:00",label="开始时间",visible=False)
                time_max = gr.Dropdown(["9:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00","17:00","18:00","19:00","20:00","21:00","22:00"],value="21:00",label ="结束时间",visible=False)
                ng_button = gr.Button("取消任务",visible=False,scale=1)
            ok_button = gr.Button("确认",scale=1,visible=False,variant="primary")
            output_txt = gr.Text(label="结果",lines=8,max_lines=8,visible=True)
            gr.Markdown("""
            【使用指南】:

            1.手机下载软件 Zepp Life->安卓/苹果都可以。

            2.登录后，点击我的->第三方接入->选择微信。

            3.保存二维码->微信扫码->关注公众号即可。

            4.使用该网址，登录后，输入数据，芜湖起飞！
                        
            【注意事项】:
                        
            1.提交后显示为0，可以重新注册小米运动账号，再绑定【使用指南】，还是不生效，则是步数修改太高，系统限制（7天后自动恢复）。

            2.当天的数据不能降低，即使提交成功也并不会生效。""")

            input_mode.change(self.mode,inputs=[input_mode],outputs=[time_min,time_max,ng_button])
            time_min.change(None,inputs=time_min,outputs=time_min)
            time_min.change(None,inputs=time_max,outputs=time_max)
            login_btn.click(self.login,inputs=[input_user,input_pwd],outputs=[output_txt,input_user,input_pwd,login_btn,del_button,input_step,ok_button,unlogin_btn,input_mode,time_min,time_max,ng_button])
            unlogin_btn.click(self.unlogin,inputs=None,outputs=[output_txt,input_user,input_pwd,login_btn,del_button,input_step,ok_button,unlogin_btn,input_mode,time_max,time_min,ng_button])
            ok_button.click(self.run_step,inputs=[input_mode,input_user,input_pwd,input_step,time_min,time_max],outputs=output_txt)
            del_button.click(self.del_res,inputs=[input_user,input_pwd,output_txt],outputs=[input_user,input_pwd,output_txt])

            return demo

if __name__ == "__main__":
    gwgis = GradioMiFit()
    demo = gwgis.init_ui()
    pid_init()
    demo.queue(150).launch(server_name="127.0.0.1",server_port=8000,share=False,show_api=False)
