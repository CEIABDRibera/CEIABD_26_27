import os
import sys
from openai import OpenAI

# Función para limpiar la consola de VS Code al iniciar (estética)
def limpiar_pantalla():
    if os.name == 'nt': # Windows
        os.system('cls')
    else: # Mac / Linux
        os.system('clear')

# Limpiamos la pantalla antes de empezar
limpiar_pantalla()

print("Conectando con LM Studio en local...")

# 1. Configuración del cliente
# Asegúrate de que el servidor en LM Studio está en ON (verde)
try:
    client = OpenAI(
        base_url="http://localhost:1234/v1", 
        api_key="lm-studio"
    )
except Exception as e:
    print(f"Error al configurar el cliente: {e}")
    sys.exit()

# 2. Historial inicial
historial = [
    {"role": "system", "content": "Eres un asistente inteligente. Responde de forma clara y breve."}
]

print("------------------------------------------------------------")
print("🟢 CHAT INICIADO CON TU IA LOCAL")
print("   (Escribe 'salir' para cerrar el programa)")
print("------------------------------------------------------------")

while True:
    try:
        # 3. Input del usuario
        # El cursor aparecerá esperando tu texto en la TERMINAL
        pregunta = input("\n👤 Tú: ")
        
        # Condición de salida
        if pregunta.lower().strip() in ["salir", "exit", "quit", "adios"]:
            print("\n👋 ¡Hasta luego!")
            break
        
        # Si el usuario da Enter sin escribir nada, ignoramos
        if not pregunta.strip():
            continue

        # 4. Guardar en memoria
        historial.append({"role": "user", "content": pregunta})

        print("🤖 Pensando...", end="\r") # Efecto visual simple

        # 5. Llamada a la IA
        response = client.chat.completions.create(
            model="local-model",
            messages=historial,
            temperature=0.7,
        )

        # 6. Respuesta
        respuesta_ia = response.choices[0].message.content
        
        # Borramos el "Pensando..." y mostramos respuesta
        print(" " * 20, end="\r") 
        print(f"🤖 IA: {respuesta_ia}")

        # 7. Guardar respuesta en memoria
        historial.append({"role": "assistant", "content": respuesta_ia})

    except KeyboardInterrupt:
        # Permite salir pulsando Ctrl+C en la terminal
        print("\n\n👋 Programa interrumpido. Cerrando.")
        break
    except Exception as e:
        print(f"\n❌ Ocurrió un error: {e}")
        print("💡 Pista: ¿Está LM Studio abierto y el servidor iniciado?")
        break