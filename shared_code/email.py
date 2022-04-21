""" Email functions """
import os
import requests

def send_email(to_name, to_email, replacements, has_complied=False):
    """ send an email """
    from_name = os.getenv('FROM_NAME')
    from_email = os.getenv('FROM_ADDRESS')
    email_api_url = os.getenv('EMAIL_API_URL')
    api_key = os.getenv('EMAIL_API_KEY')
    email_subj = os.getenv('EMAIL_SUBJECT_COMPLIED') if has_complied \
        else os.getenv('EMAIL_SUBJECT_NOT_COMPLIED')
    email_template_url = os.getenv('EMAIL_TEMPLATE_URL_COMPLIED') if has_complied \
        else os.getenv('EMAIL_TEMPLATE_URL_NOT_COMPLIED')

    print(f'sending email to:{to_name} {to_email}')
    print(f'compliance: {has_complied}')
    print(f'template replacments: {replacements}')

    response = requests.post(
        email_api_url,
        headers={
            'x-apikey': api_key
        },
        json={
            'subject': email_subj,
            'to': [{
                'name': to_name,
                'email': to_email
            }],
            'from':{
                'name': from_name,
                'email': from_email
            },
            'template': {
                'url': email_template_url,
                'replacements': {
                    'data': replacements
                }
            }
        }
    )

    response.raise_for_status()
