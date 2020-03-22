from django.core.mail import send_mail
from dwing.celery import app

@app.task
def send_active_email(email, random_num):
    #发送激活邮件
    try:
        subject = '验证码为'
        html_message = '''
        <p>尊敬的用户 您好</p>
        <p>您的邮箱验证码为%s请在5分钟内输入</p>
        '''%random_num
        send_mail(subject=subject, html_message=html_message,from_email='1161752300@qq.com', recipient_list=[email],
                  message='1161752300@qq.com')
        print('----send mail ok-----')
    except Exception as e:
        print('--send email error--')
        print(e)
        #TODO 上线后添加 error response

