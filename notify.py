import requests

def send_line_notify(msg, token):
    url = 'https://notify-api.line.me/api/notify'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'message': msg}
    response = requests.post(url, headers=headers, data=data)
    return response.status_code
