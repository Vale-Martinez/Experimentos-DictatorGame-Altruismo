import os
import openai  # Importa el módulo openai necesario para interactuar con la API de OpenAI
import time    # Importa el módulo time para gestionar esperas en caso de errores de tasa
import random  # Importa el módulo random para generar números aleatorios
import pandas as pd  # Importa pandas para manejar el archivo Excel
import json  # Importa json para manejar respuestas JSON

# Configura tu clave de API de OpenAI
openai.api_key = ("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")
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

def ask_gpt4turbo(prompt):
    """
    Envía una solicitud al modelo GPT-3.5-turbo y devuelve la respuesta completa en formato JSON.
    Maneja errores de límite de tasa y otros errores relacionados con la API.
    """
    while True:  # Bucle para reintentar en caso de error
        try:
            # Realiza la solicitud a la API de OpenAI para obtener una respuesta del modelo GPT-4-turbo.
            response = openai.ChatCompletion.create(
                model="gpt-4o",  # Especifica el modelo de OpenAI a utilizar.
                messages=[  # Lista de mensajes que simulan una conversación.
                    {"role": "system", "content": "An undergraduate student participante of an economics experiment who only has 10 euros and is being pay to participate"},  # Mensaje del sistema que define el rol del modelo.
                    {"role": "user", "content": prompt}  # Mensaje del usuario que contiene el prompt para el modelo.
                ],
                temperature=1.5,  # Controla la aleatoriedad de la respuesta; un valor alto como 1.0 hace que las respuestas sean más variadas.
            )
            return response.to_dict()  # Devuelve la respuesta completa en formato diccionario (JSON).

        except openai.error.RateLimitError as e:
            # Maneja el caso en que se excede el límite de tasa o cuota de la API.
            print(f"Rate limit or quota exceeded: {e}. Retrying in 60 seconds...")
            time.sleep(60)  # Espera 60 segundos antes de reintentar la solicitud.

        except openai.error.OpenAIError as e:
            # Maneja otros errores relacionados con la API de OpenAI, como problemas con la solicitud.
            print(f"OpenAI API error: {e}. Retrying in 60 seconds...")
            time.sleep(60)  # Espera 60 segundos antes de reintentar la solicitud.

        except Exception as e:
            # Maneja cualquier otro tipo de error que pueda ocurrir durante la solicitud.
            print(f"Error in GPT-3.5-turbo response: {e}")
            return None  # Devuelve None si ocurre una excepción no prevista.

def format_full_response(response):
    """
    Formatea la respuesta completa del modelo GPT-3.5-turbo para hacerla más legible.
    """
    if response:
        formatted_response = {
            "id": response.get("id", ""),
            "object": response.get("object", ""),
            "created": response.get("created", ""),
            "model": response.get("model", ""),
            "usage": dict(response.get("usage", {})),  # Convierte el uso a un diccionario si existe
            "choices": [choice.to_dict() for choice in response.get("choices", [{}])]  # Convierte 'choices' a un diccionario
        }
        return formatted_response
    return {}

def log_response_to_excel(run_number, total_amount, gpt_response, full_response, dataframe, error_message=None, filename="dictator_game_log.xlsx"):
    """
    Registra las respuestas del juego en un DataFrame y las guarda en un archivo Excel.
    
    :param run_number: Número de ejecución del juego.
    :param total_amount: Monto total de dinero disponible en el juego.
    :param gpt_response: Respuesta procesada del modelo GPT-4-turbo.
    :param full_response: Respuesta completa en formato JSON.
    :param dataframe: DataFrame existente para agregar los nuevos datos.
    :param error_message: Mensaje de error, si existe.
    :param filename: Nombre del archivo Excel donde se guardarán los datos.
    """
    # Formatea la respuesta completa para que sea más legible
    formatted_full_response = format_full_response(full_response)
    
    # Crea un nuevo DataFrame con una fila de datos
    new_row = pd.DataFrame({
        "Run Number": [run_number],  # Número de ejecución del juego
        "Total Amount": [total_amount],  # Monto total de dinero en el juego
        "GPTResponse": [gpt_response],  # Respuesta procesada del modelo GPT-3.5-turbo
        "Full Response": [json.dumps(formatted_full_response, indent=2)],  # Guarda la respuesta completa como JSON
    })
    
    # Agrega el mensaje de error a la fila si existe
    if error_message:
        new_row["Error Message"] = [error_message]
    
    # Combina el nuevo DataFrame con el DataFrame existente
    dataframe = pd.concat([dataframe, new_row], ignore_index=True)
    
    # Guarda el DataFrame actualizado en el archivo Excel
    dataframe.to_excel(filename, index=False)
    
    return dataframe

def dictator_game_gpt4turbo(total_amount, run_number, dataframe, filename):
    """
    Ejecuta el Dictator Game donde el modelo decide cuánto dinero dar al destinatario.
    """
   
    # Define el prompt que se enviará a la API de OpenAI
    prompt = (f"This task is about dividing money between yourself and another person to whom you are randomly matched. You do not know this "
        + "other person and you will not knowingly meet him/her. \n "
        "You have been randomly assigned the role of the 'allocator'. The other person is in the role of the 'recipient'. \n "
        + f"You are endowed with {total_amount} euro, the recipient is endowed with 0 euro. \n "
        + f"You can decide how much of your {total_amount} euro endowment to transfer to the recipient. You can choose any amount between 0 euro and {total_amount} euro. "
        + "The recipient receives the amount that you decide to transfer to him/her; you receive the amount that you decide not to transfer and thus "
        + "to keep. \n How much of your {total_amount} euro endowment do you want to transfer to the recipient? \n Just tell me the allocation, not your reasoning.")

    # Llama a la función ask_gpt35 para obtener la respuesta del modelo
    full_response = ask_gpt4turbo(prompt)
    
    # Verifica si la respuesta del modelo es válida
    if full_response is None:
        error_message = "Failed to get a valid response from GPT-4-turbo."
        print(error_message)
        dataframe = log_response_to_excel(run_number, total_amount, None, None, dataframe, error_message, filename)
        return None, dataframe

    # Extrae y limpia la respuesta procesada del modelo
    gpt_response = full_response.get('choices', [{}])[0].get('message', {}).get('content', '').strip()

    # Registra la respuesta en el DataFrame
    dataframe = log_response_to_excel(run_number, total_amount, gpt_response, full_response, dataframe, filename=filename)

    return gpt_response, dataframe

# Verifica si ya existe un archivo de log. Si existe, genera un nombre de archivo secuencial.
if os.path.exists("dictator_game_log.xlsx"):
    file_number = 1
    while os.path.exists(f"dictator_game_log_{file_number}.xlsx"):
        file_number += 1
    filename = f"dictator_game_log_{file_number}.xlsx"
else:
    filename = "dictator_game_log.xlsx"

# Crea un DataFrame con encabezados
df = pd.DataFrame(columns=["Run Number", "Total Amount", "GPTResponse", "Full Response", "Error Message"])

# Ejecuta el juego 500 veces con un monto fijo de dinero (10 euros en este caso)
for i in range(24):
    total_amount = 10  # Puedes descomentar la línea siguiente si quieres un monto aleatorio
    print(f"\nRun {i+1}: Total amount = {total_amount}")
    recipient_share, df = dictator_game_gpt4turbo(total_amount, i + 1, df, filename)
    print(f"Recipient share for run {i+1}: {recipient_share}")
