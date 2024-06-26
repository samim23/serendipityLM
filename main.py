from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
import asyncio
import logging
from openai import AsyncOpenAI

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

client = AsyncOpenAI(timeout=60.0)

logging.basicConfig(level=logging.INFO)

async def generate_text(prompt, amount):
    model = "gpt-4o"
    temperature = prompt["temperature"]
    response_format = prompt["response_format"]
    message = prompt["message"]

    try:
        response = await client.chat.completions.create(
            model=model,
            response_format={"type": response_format},
            temperature=temperature,
            messages=message,
            n=amount
        )
        results = [choice.message.content for choice in response.choices]
        logging.info(f'GPT: {model}, Temperature: {temperature}, Prompt length: {len(prompt)}, Generated Text: {results}')
        return results
    except Exception as e:
        logging.error(f'Error generating text: {str(e)}')
        raise HTTPException(status_code=500, detail="Error generating text from OpenAI API")

class Eval(BaseModel):
    item: str
    amount: int
    prompt: str

@app.post("/process/")
async def process_json(eval_data: Eval):

    prompt = {
        "temperature": 1,
        "response_format": "json_object",
        "message": [
            {"role": "system", "content": eval_data.prompt + " When you respond, output a JSON where the first key ('thought') corresponds to your thought process when designing the next design. The second key ('name') corresponds to the name of your next design. The last key ('code') corresponds to the exact html code that you would like to try. NEVER add the key ('critique') to the JSON. Here is an example of the desired JSON: {\"thought\": \"<thought>\", \"name\": \"<name>\", \"code\": \"<code>\"} <QUERY> Propose the next design to evaluate. <EVAL> Evaluate all the following examples as starting points and consider their 'fitness' ratings: Fitness 0 = Bad design, Fitness 1 = Great design. Consider carefully the critique that the user might have added to examples. Take a deep breathe and think step by step - then remix, re-combine and improve the provided evaluation examples, taking into account their strengths and weaknesses to create a more innovative and effective design. Ensure your creation is significantly distinct from the examples while addressing any identified flaws and enhancing the positive aspects. Provide a detailed thought process explaining which previous example you used as inspiration and mention its name, how your choices address the criteria and improve upon the examples: \n\n" + eval_data.item},
        ]
    }
    print('----------------------------------------------------------------------------------')
    print("process - EVAL prompt:", prompt)

    try:
        all_results = await generate_text(prompt, eval_data.amount)
        results_json = [json.loads(result) for result in all_results]
    except json.JSONDecodeError as e:
        return JSONResponse(content={"error": f"JSONDecodeError: {str(e)}"}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": f"Unexpected error: {str(e)}"}, status_code=500)

    return JSONResponse(content={"results": results_json})


@app.get("/", response_class=HTMLResponse)
async def get_html():
    try:
        with open("static/index.html") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError as e:
        logging.error(f'FileNotFoundError: {str(e)}')
        return HTMLResponse(content="Index file not found", status_code=404)