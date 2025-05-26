import requests

def send_sms(phone: str, message: str) -> dict:
    """
    Отправляет SMS через API NotiSend.

    :param phone: Номер телефона получателя (например, 89655444278)
    :param message: Текст сообщения
    :return: Ответ API в формате dict
    """
    url = "https://sms.notisend.ru/api/message/send"
    api_key = "0f1d946fe6d8231f2a08fa6c93551b08"
    data = {
        "project": "Loom_TG",
        "recipients": phone,
        "message": message,
        "apikey": api_key
    }
    response = requests.post(url, data=data, headers={"Accept": "application/json"})
    return response.json()

# Пример использования:
if __name__ == "__main__":
    result = send_sms("79655444278", "34567")
    print(result)