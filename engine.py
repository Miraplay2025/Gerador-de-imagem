import torch
from diffusers import StableDiffusionXLPipeline
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import base64
import hashlib

# Configuração do Modelo Ultra Rápido
print("🚀 Carregando IA... Aguarde.")
pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/sdxl-turbo", 
    torch_dtype=torch.float16, 
    variant="fp16"
).to("cuda")

app = Flask(__name__)
CORS(app)

# Rota de teste para evitar o erro "Not Found"
@app.route('/', methods=['GET'])
def index():
    return "✅ O Servidor da IA está Online e pronto para gerar!"

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        prompt = data.get("prompt", "").lower()
        
        # Extrai a primeira palavra para a semente de persistência
        words = prompt.split()
        entity_name = words[0] if words else "default"
        
        if entity_name not in memory_bank:
            memory_bank[entity_name] = int(hashlib.md5(entity_name.encode()).hexdigest(), 16) % (10**8)
        
        seed = memory_bank[entity_name]
        generator = torch.Generator("cuda").manual_seed(seed)

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
                "status": "success"
            })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

memory_bank = {}

def run_app():
    app.run(port=5000)

if __name__ == "__main__":
    run_app()
