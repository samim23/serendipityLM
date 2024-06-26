# SerendipityLM

### Interactive evolutionary exploration of generative design spaces with large language models

<p align="center"><img alt="SerendipityLM" src="https://samim.io/studio/assets/work/serendipity/serendipityLM00.png" /></p>

## What is it?

### **Check out [this blog post](https://samim.io/studio/work/serendipityLM/) for an extensive experiment report.**

Generative AI systems have opened up vast design spaces that are challenging to explore. The role of human interaction and intuition in enhancing novelty and variance of AI-generated outputs is crucial yet often overlooked. SerendipityLM is an experiment in "Serendipity Engineering", that moves beyond traditional prompting and instead uses evolutionary interaction methods to generate complex generative artworks with Large Language Models. It turns the exploration of design spaces into a playful and serendipitous experience that investigates the boundaries LLM HCI.

## How does it work?

<p align="center"><img alt="SerendipityLM" src="https://samim.io/studio/assets/work/serendipity/serendipityLM02.png" /></p>

## Requirements

You need to have the OpenAI API key active in your console enviroment

## Installation

You need python version `>=3.7`. From your terminal run:

```bash
git clone https://github.com/samim23/serendipityLM
cd serendipityLM
pip install -r requirements.txt
```

## Run SerendipityLM

```bash
uvicorn main:app --reload --port 1234
```

Then visit the site http://127.0.0.1:1234 in your browser

## Share your results

Feel free to share any intriguing examples you create using SerendipityLM with me [on X](https://x.com/samim).
