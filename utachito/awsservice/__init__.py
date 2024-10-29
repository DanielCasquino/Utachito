import requests
import io
from PIL import Image
import base64

url = "https://ki482ms00l.execute-api.us-east-1.amazonaws.com/dev/face/"


def numpy_to_base64(image_matrix):
    image = Image.fromarray(image_matrix.astype("uint8"))
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")

    # Step 3: Encode the buffer contents to base64
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str


# {'statusCode': 500, 'body': 'Error when recognizing face', 'error': 'An error occurred (InvalidParameterException) when calling the SearchFacesByImage operation: There are no faces in the image. Should be at least 1.'}


def recognize(image_matrix, waste="botella", amount=1):
    image_binary = numpy_to_base64(image_matrix)
    # Dentro de lambda se decodea porque tiene que ir en binario para Rekognition
    # Se tiene que cambiar para convertir de matriz a base64. Luego solo se hace el decode
    # Qunatity es la cantidad de desecho.
    # waste es el tipo de desecho.
    body = {"image": image_binary, "quantity": amount, "waste": waste}
    response = requests.post(url + "recognition", json=body)
    # print(response)
    # regresa un diccionario de la forma {"statusCode": 200, "body": {"message": message, "student": student}}
    body = response.json()
    # print(body)
    if body["statusCode"] == 500:
        message = f"Soy un estudiante que falta registrarse. Tengo una cantidad {amount} de {waste}"
    else:
        message = body["body"]["message"]

    # El message es de la forma: Soy NOMBRE, tengo DESECHO.
    # Si no está registrado, en lugar de nombre dice que es un estudiante que falta registrarse
    # Igualmente, si está registrado, se regresa los datos del estudiante en student
    return message
