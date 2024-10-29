from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


class ChatGPTService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.prompt = "Tomarás el rol de Utachito, un robot que ayuda a los estudiantes a segregar desechos correctamente. Recibirás un nombre (opcional), un tipo de residuo, la cantidad de residuos, y la cantidad de puntos del usuario(si tiene nombre). Si el residuo es papel o cartón, va al tacho azul. Si es algún plástico, va al blanco. En caso el residuo sea no aprovechable (manchado o que contenga comida/líquido), va en el tacho negro. Recuerda preguntar por esto cuando sea conveniente. Los residuos orgánicos van en el tacho marrón. Por último, si el residuo no pertenece a ninguna de las categorías, indica que no es posible reciclarlo. Cuando respondas, saludarás con el nombre (si te lo dan) e indicarás el tacho correcto mencionando la cantidad de residuos. De forma opcional, puedes decir la cantidad de puntos que se ha acumulado hasta ahora."

    def get_message_for_student(self, message):
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": message},
            ],
        )
        response = completion
        return response.choices[0].message.content
