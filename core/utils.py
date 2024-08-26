from django.core.mail import EmailMessage
from django.template.loader import get_template

def send_email(email, subject, template_path, context):
    """
    Helper function to send HTML email notification to users.

    Parameters:
    - subject (str): The subject of the email.
    - plain_message (str): The plain text message of the email.
    - template_path (str): The file path to the HTML template.
    - context (dict): The context dictionary to render the HTML template.

    Example usage:
    send_email(
        "Weekly Report",
        "Here is the weekly report in plain text.",
        "mails/mail.html",
        {"user": "username"}
    )
    """



    # Render the HTML content from the template
    html_message = get_template(template_path).render(context)

    # Create the email
    msg = EmailMessage(
        subject,
        html_message,
        'Innomatch',  # Replace with the actual sender's email
        [email]
    )
    msg.content_subtype = "html"  # Main content is now text/html

    msg.send()

# Example usage:
# send_email(
#     "Weekly Report",
#     "Here is the weekly report in plain text.",
#     "mails/mail.html",
#     {"user": "username"}
# )
