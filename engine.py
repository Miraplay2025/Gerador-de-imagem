from flask import Flask, request, jsonify
from flask_cors import CORS
import torch, base64, hashlib, os
from diffusers import AutoPipelineForText2Image

app = Flask(__name__)
CORS(app)

# Carregando o modelo ultra-otimizado para evitar erro 502
print("🚀 Carregando Motor Ultra-Leve...")
pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/sdxl-turbo", 
    torch_dtype=torch.float16, 
    variant="fp16"
).to("cuda")

memory = {}

@app.route('/')
def health(): 
    return "✅ Servidor Online e Estável!"

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        prompt = data.get("prompt", "").lower()
        
        # Persistência Automática por Nome
        words = prompt.split()
        entity = words[0] if words else "default"
        
        if entity not in memory:
            memory[entity] = int(hashlib.md5(entity.encode()).hexdigest(), 16) % 10**8
        
        # Geração rápida (apenas 1 passo para máxima estabilidade)
        image = pipe(
            prompt=prompt, 
            num_inference_steps=1, 
            guidance_scale=0.0, 
            generator=torch.Generator("cuda").manual_seed(memory[entity])
        ).images[0]
        
        image.save("o.png")
        with open("o.png", "rb") as f:
            return jsonify({"image": base64.b64encode(f.read()).decode('utf-8')})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
