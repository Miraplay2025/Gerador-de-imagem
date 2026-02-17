import torch
from diffusers import StableDiffusionXLPipeline
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import base64

# Configuração do Modelo Ultra Rápido
print("🚀 Carregando IA... Aguarde.")
pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/sdxl-turbo", 
    torch_dtype=torch.float16, 
    variant="fp16"
).to("cuda")

app = Flask(__name__)
CORS(app)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get("prompt")
    # Gerando a imagem em 2 passos (super rápido)
    image = pipe(prompt=prompt, num_inference_steps=2, guidance_scale=0.0).images[0]
    image.save("result.png")
    
    with open("result.png", "rb") as img_file:
        return jsonify({"image": base64.b64encode(img_file.read()).decode('utf-8')})

def run_app():
    app.run(port=5000)

# Inicia o servidor Flask
threading.Thread(target=run_app).start()
print("✅ Servidor Interno Rodando na porta 5000")
