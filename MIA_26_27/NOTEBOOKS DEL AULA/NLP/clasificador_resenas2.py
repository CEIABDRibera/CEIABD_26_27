from openai import OpenAI
import sys

# Configuración
try:
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
except Exception as e:
    print(f"Error: {e}")
    sys.exit()

lista_resenas = [
    "El producto llegó roto, terrible servicio.",       
    "Me encantó, es justo lo que buscaba.",             
    "El envío fue rápido pero la calidad es regular."   
]

system_prompt = (
    "Eres un clasificador de IA. Tu única tarea es responder con una de estas 3 palabras clave:\n"
    "POSITIVO\n"
    "NEGATIVO\n"
    "NEUTRO\n"
    "No escribas frases. Solo la palabra exacta."
)

print("--- 🤖 CLASIFICADOR FINAL (Ajustado para Neutros) ---\n")

for reseña in lista_resenas:
    try:
        response = client.chat.completions.create(
            model="local-model",
            messages=[
                {"role": "system", "content": system_prompt},
                
                # EJEMPLO 1: Caso negativo claro
                {"role": "user", "content": "Es una basura, no sirve."},
                {"role": "assistant", "content": "NEGATIVO"},
                
                # EJEMPLO 2: Caso positivo claro
                {"role": "user", "content": "Una maravilla, genial."},
                {"role": "assistant", "content": "POSITIVO"},
                
                # EJEMPLO 3 (CAMBIADO): Usamos una frase MIXTA similar a la problemática
                # Le enseñamos explícitamente que "Bueno + Regular" = NEUTRO
                {"role": "user", "content": "Llegó pronto pero la caja estaba sucia."},
                {"role": "assistant", "content": "NEUTRO"},
                
                {"role": "user", "content": reseña}
            ],
            temperature=0.0, # Bajamos a 0.0 para máxima rigidez
            max_tokens=10, 
        )

        respuesta_ia = response.choices[0].message.content.strip().upper()

        if "POSITIVO" in respuesta_ia:
            resultado_visual = "✅ POSITIVO"
        elif "NEGATIVO" in respuesta_ia:
            resultado_visual = "❌ NEGATIVO"
        # Añadimos "REGULAR" por si acaso el modelo se pone rebelde
        elif "NEUTRO" in respuesta_ia or "REGULAR" in respuesta_ia:
            resultado_visual = "⚖️ NEUTRO"
        else:
            resultado_visual = f"❓ Raro: {respuesta_ia}"

        print(f"📝 Reseña: \"{reseña}\"")
        print(f"🏷️  Resultado: {resultado_visual}")
        print("-" * 40)

    except Exception as e:
        print(f"Error: {e}")
        break