from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from diffusers import StableDiffusionPipeline
from torch import autocast
import torch


class Text2Image(BaseModel):
    prompt: str
    negative_prompt: str | None = "out of frame, lowres, text, error, cropped, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, out of frame, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck, username, watermark, signature"


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello world!"}


counter = 0


@app.post("/txt2img", response_class=FileResponse)
async def txt2img(body: Text2Image):
    global counter

    model = "andite/pastel-mix"
    pipe = StableDiffusionPipeline.from_pretrained(
        model, torch_dtype=torch.float16)

    # If you're using a CPU, remove or comment the line below
    pipe = pipe.to("cuda")

    def dummy_checker(images, **kwargs):
        return images, False

    pipe.safety_checker = dummy_checker

    prompt = body.prompt
    negative_prompt = body.negative_prompt

    image = pipe(prompt=prompt, negative_prompt=negative_prompt).images[0]

    # Increment the counter and generate the image filename
    counter += 1
    filename = f"images/image-{counter}.png"

    # Save the image to the generated filename
    image.save(filename)

    return filename
