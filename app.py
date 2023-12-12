from fastapi import FastAPI, HTTPException
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel, GPT2Config

app = FastAPI()

# Load the model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('my_story/')
tokenizer.pad_token = tokenizer.eos_token

configuration = GPT2Config.from_pretrained('my_story/', output_hidden_states=False)

model = GPT2LMHeadModel.from_pretrained("my_story/", config=configuration)
model.resize_token_embeddings(len(tokenizer))

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

@app.post("/stories/")
async def generate_text(prompt: str):
    try:
        generated = torch.tensor(tokenizer.encode(prompt)).unsqueeze(0)
        generated = generated.to(device)

        sample_outputs = model.generate(
            generated,
            do_sample=True,
            top_k=50,
            max_length=500,
            top_p=0.95,
            num_return_sequences=1
        )

        outputs = [tokenizer.decode(sample_output, skip_special_tokens=True) for sample_output in sample_outputs]
        return {"generated_text": outputs}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
