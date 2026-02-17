import torch
from diffusers import StableDiffusionXLPipeline
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import base64
import hashlib

# Configuração do Modelo
pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/sdxl-turbo", 
    torch_dtype=torch.float16, 
    variant="fp16"
).to("cuda")

app = Flask(__name__)
CORS(app)

# Dicionário para guardar a "Semente" de cada personagem/lugar
memory_bank = {}

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get("prompt", "").lower()
    
    # Lógica de Persistência Automática
    # Extrai a primeira palavra ou nome para criar uma semente fixa
    words = prompt.split()
    entity_name = words[0] if words else "default"
    
    if entity_name not in memory_bank:
        # Cria uma semente única baseada no nome para persistência eterna
        memory_bank[entity_name] = int(hashlib.md5(entity_name.encode()).hexdigest(), 16) % (10**8)
    
    seed = memory_bank[entity_name]
    generator = torch.Generator("cuda").manual_seed(seed)

    # Geração com a semente travada para o nome usado
    image = pipe(
        prompt=prompt, 
        num_inference_steps=2, 
        guidance_scale=0.0,
        generator=generator
    ).images[0]
    
    image.save("result.png")
    
    with open("result.png", "rb") as img_file:
        return jsonify({
            "image": base64.b64encode(img_file.read()).decode('utf-8'),
            "entity": entity_name,
            "seed": seed
        })

def run_app():
    app.run(port=5000)

threading.Thread(target=run_app).start()
print("✅ Motor de Persistência Automática Online na porta 5000")
