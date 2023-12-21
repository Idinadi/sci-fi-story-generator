from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from typing import Optional
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel, GPT2Config

app = FastAPI(docs_url="/api/v2/apidocs")

# Load the model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('my_story/')
tokenizer.pad_token = tokenizer.eos_token

configuration = GPT2Config.from_pretrained('my_story/', output_hidden_states=False)

model = GPT2LMHeadModel.from_pretrained("my_story/", config=configuration)
model.resize_token_embeddings(len(tokenizer))

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Dummy data storage
users = {}
stories = {}
story_id_counter = 1

# User model
class User(BaseModel):
    username: str
    nickname: Optional[str] = None

# Story model
class Story(BaseModel):
    title: str
    content: str

# User endpoints
@app.post("/users")
def create_user(user: User):
    if user.username in users:
        raise HTTPException(status_code=400, detail="User already exists")
    users[user.username] = user
    return {"message": "User created successfully"}

@app.get("/users/me")
def get_current_user(username: str):
    user = users.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.patch("/api/v2/users/me")
def update_user_nickname(username: str, nickname: str):
    if username not in users:
        raise HTTPException(status_code=404, detail="User not found")
    users[username].nickname = nickname
    return {"message": "User nickname updated successfully"}

# Story endpoints
@app.post("/api/v2/stories")
def create_story(story: Story):
    global story_id_counter
    story_id = story_id_counter
    stories[story_id] = story
    story_id_counter += 1
    return {"id": story_id, "title": story.title}

@app.get("/api/v2/stories")
def list_stories():
    return list(stories.values())

@app.get("/api/v2/stories/{story_id}")
def get_story(story_id: int):
    story = stories.get(story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story

@app.delete("/api/v2/stories/{story_id}")
def delete_story(story_id: int):
    if story_id not in stories:
        raise HTTPException(status_code=404, detail="Story not found")
    del stories[story_id]
    return {"message": "Story deleted successfully"}

# GPT-2 Story Generation endpoint
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

