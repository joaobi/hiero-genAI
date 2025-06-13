# hiero-genAI
Code to generate new versions of an ASCII Ancient Egyptian hieroglyph for the purpose of generating datasets for sign classification (OCR).
Uses AzureOpenAI with a GPT-Image-1 model and the  API version 2025-04-01-preview.

Takes a picture (in the sample, the sign A1 created using the Aaron fonts) and produces another based on the prompt.

Ilustration of the output from the sample code:
![Ilustration of the sample](https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fee62082e-7c48-43b9-b1f6-fa24713de6c9_681x300.png)

More details on [my Substack](https://open.substack.com/pub/thetwolands/p/using-ai-to-generate-new-hieroglyphs?r=27isp3&utm_campaign=post&utm_medium=web&showWelcomeOnShare=true)

## Requirements
Update the variables.env with your own AzureOpenAI model configuration. Currently (June 2025), GPT-Image-1is still under preview on AOAI and you will need to request access to it.

### Python dependencies
python-dotenv

requests

dotenv

## Execution
```shell
python hiero-gen.py
```

