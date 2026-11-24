from openai import OpenAI
import sys

# 1. Configuración del Cliente
# Apuntamos al servidor local de LM Studio
try:
    client = OpenAI(
        base_url="http://localhost:1234/v1", 
        api_key="lm-studio"
    )
except Exception as e:
    print(f"Error al configurar: {e}")
    sys.exit()

# 2. Datos de entrada (Las reseñas del ejercicio)
lista_resenas = [
    "El producto llegó roto, terrible servicio.",
    "Me encantó, es justo lo que buscaba.",
    "El envío fue rápido pero la calidad es regular."
]

# 3. Definición del System Prompt
# Es CRUCIAL ser muy estricto aquí para que no suelte un discurso, solo la etiqueta.
system_prompt = (
    "La clasificación solo puede ser: 'Positivo', 'Negativo' o 'Neutro'."
)

print("--- 🤖 INICIANDO CLASIFICACIÓN DE RESEÑAS ---")
print(f"Procesando {len(lista_resenas)} opiniones...\n")

# 4. Bucle de procesamiento
for reseña in lista_resenas:
    try:
        response = client.chat.completions.create(
            model="local-model", # En LM Studio usa el modelo que tengas cargado
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": reseña}
            ],
            temperature=0.1, # Temperatura baja = Mayor precisión y menos "creatividad"
        )

        # Extraemos la respuesta limpia
        clasificacion = response.choices[0].message.content.strip()

        # 5. Imprimir resultados formateados
        print(f"📝 Reseña: \"{reseña}\"")
        print(f"🏷️  Clasificación: {clasificacion}")
        print("-" * 40)

    except Exception as e:
        print(f"❌ Error procesando la reseña: {e}")
        print("Asegúrate de que el servidor de LM Studio está iniciado (Start Server).")
        break

print("\n✅ Proceso terminado.")