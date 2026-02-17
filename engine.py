import torch
from diffusers import StableDiffusionXLPipeline
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import hashlib
import os

# 1. Configuração do Modelo (SDXL Turbo para velocidade extrema)
print("🚀 Carregando pesos da IA na GPU...")
pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/sdxl-turbo", 
    torch_dtype=torch.float16, 
    variant="fp16"
).to("cuda")

app = Flask(__name__)
CORS(app)

# Banco de dados de memória (Sementes persistentes)
memory_bank = {}

@app.route('/', methods=['GET'])
def home():
    return "✅ O Servidor da IA está Online e pronto para gerar imagens!"

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        prompt = data.get("prompt", "").lower()
        
        # Lógica de Persistência Automática
        # Usa o hash da primeira palavra do prompt como 'Seed' fixa
        words = prompt.split()
        first_entity = words[0] if words else "default"
        
        if first_entity not in memory_bank:
            # Gera uma semente numérica única baseada no nome
            seed_value = int(hashlib.md5(first_entity.encode()).hexdigest(), 16) % (10**8)
            memory_bank[first_entity] = seed_value
            print(f"🧬 Nova memória criada para: {first_entity} (Seed: {seed_value})")
        
        current_seed = memory_bank[first_entity]
        generator = torch.Generator("cuda").manual_seed(current_seed)

        # Geração da Imagem
        image = pipe(
            prompt=prompt, 
            num_inference_steps=2, 
            guidance_scale=0.0,
            generator=generator
        ).images[0]
        
        # Converte para Base64 para envio ultra rápido
        image.save("output.png")
        with open("output.png", "rb") as img_file:
            img_b64 = base64.b64encode(img_file.read()).decode('utf-8')
            
        return jsonify({
            "status": "success",
            "image": img_b64,
            "entity": first_entity,
            "seed": current_seed
        })

    except Exception as e:
        print(f"❌ Erro na geração: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    print("🛰️ Servidor Flask iniciando na porta 5000...")
    app.run(host='0.0.0.0', port=5000)
