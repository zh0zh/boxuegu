from django.core.mail import send_mail
from django.conf import settings
from celery_tasks.main import celery_app


@celery_app.task(name='send_user_email', bind=True, backoff_retry=3)
def send_user_email(self, to_email, verify_url):
    # send_mail()方法接受五个参数：分别是subject主题, message抄送, from_email公司邮箱, recipient_list收件人地址（注意，这是一个列表），
    # auth_message正文 或 html_message 网页内容。
    subject = "博学谷线修改密码服务"
    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用博学谷线上学习系统。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接进入重置密码页面：</p>' \
                   '<p><a href="%s">%s<a></p>' % (to_email, verify_url, verify_url)
    try:
        send_mail(subject, '', settings.EMAIL_FROM, [to_email], html_message=html_message)
        print(verify_url)
    except Exception as e:
        self.retry(exc=e, max_retries=2)
