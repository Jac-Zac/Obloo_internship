# Building a chatbot with Chainlit

This code let's you run an LLM through ... With ...

You can see the code of the steps up to the final solution:

- [app.py](app.py) - Answers questions, remembers questions, and supports uploaded text files

### Notes:

- [langsmith](https://www.youtube.com/results?search_query=langsmith): used for tracking chats in the future
- [Create your ollama model from huggingface]()https://www.youtube.com/watch?v=bANziaFj_sA&list=PLz-qytj7eIWWNnbCRxflmRbYI02jZeG0k&index=12
- chainlit

### Installation

- Install [Ollama](https://ollama.com/)

- Install the model we are using:

```bash
ollama pull mistral
ollama pull nomic-embed-text
```

##### Set up a Python virtual environment

```bash
python -m venv .env
source .env/bin/active
```

#### Install dependencies

```bash
pip install -r requirements.txt
```

#### Create the database

```bash
python3 create_database.py
```

#### Run the chatbot:

```bash
chainlit run app.py -w
```

> Navigate to http://localhost:8000

You can then try to ask a question such as:

> What could we extract from the moon ? Is there any interesting development ?

## Notes about other potential usages:

I feel like things like AI might be misrepresented by the data

[Good paper using GNN for predictions](https://arxiv.org/pdf/2105.11537.pdf)

- Edge-augmented Graph Transformer

- Look into this dataset: [they used logistic regression](https://news.crunchbase.com/venture/vc-success-prediction-crunchbase-data-mason-lender/)

- Newer paper on startup [prediction using XGBoost](https://arxiv.org/pdf/2309.15552.pdf)

- ML startup [selection prediction](https://pdf.sciencedirectassets.com/313360/1-s2.0-S2405918821X00025/1-s2.0-S2405918821000040/main.pdf?X-Amz-Security-Token=IQoJb3JpZ2luX2VjEDYaCXVzLWVhc3QtMSJIMEYCIQDgdC80JpXzjbg%2FjFOqKvGl%2BroB9AzNkOXMkOAASjsAFgIhAI958yHPHO%2B6mPei99b7pwDXdtZMuNC%2FumWlVd%2Fqn%2FiMKrIFCD8QBRoMMDU5MDAzNTQ2ODY1Igz66c21ifxDvFujAEUqjwXA1RXP%2B1c9tpVCiu2Qlc%2ByUREyOnkcmpygmarmWUE0iEoXK3zHLoXbwkW3jaSFaqsHplZqPcgYgqN%2BhU%2BqeSk53bz%2FQPdKbq4Bxm2m6QLpJqtGOpqP1d2osuEO6IJibhT3ETI92gzTUjv53bJtpcZvEllt9g64EhPQCr9nPn8PK0n9skrBd1Rj6uum9QhHgDHc%2BBO90Bzj3OVfPkbgTZkC4te2SlIWf8bCn36AmC11EJSyElswoSgU1SolvGZRTmRFROiLOb%2FNqa5SHeQB5AMmhUgbZ6wt18V%2F4FnaVHO5yO6S8fJqHaITgfKowEl3TkZB6rxoEyiWFaIqaRE0UFzn%2BhANHJuD0SzpQx1khgcpeA4nPsFo%2FSN6fKhWVr4zzlfRMwLyYtIkkJKdSBcWgIMgBBQfspg6lscbyLUcs36SlYPIP2be%2Fe%2Bireo5KPo8HNeXQy9G0ISYCyEyheExFFSP4JCsnsUN8zvHiNQsGL5ibfLbQob95s3R6ODNGkTTVPaL07Qr7QuXYhF%2F9h9I65ucLPQXDiX7xdlYDSU4lqiWdT9Inb%2F9XDMc%2FhUd2aEteXbi9fvHAODkcVsk9EKdtDj80UicnOZ0W1saJdRODYec71SmhBEwwAZo1b9zuuzkrL6RnAEx4Np4MZo8K0c%2ByxF1plZRr18Xvm2lUS%2B9TGK8T%2FFtWzzusynp7IqFqtQlURljpcZv0vRIIIWy4fB009Vxq6ioybi0LkZwTfTcYcYuJ2OsgXIUeHCQwzScpHNuPjrE764zxPteKORrLQHQcaoLUl27e0Luw1QA5L3ssnPzpTYGlTWhYaFN%2FGhzH%2Fp6DFFopl4yRsK7bBbeb%2BK7KmgRCObV8OZG0SrnXpjXFFZNMOXev68GOrABXkK2JwZYphiaKfJ%2FB8Ce05AxCd3ERPYOA2ptTEaS%2BsKlIo%2FdsPB9r7kTuYTf7j%2FM4MOi%2BfvbmipPABvohVVavvA8ZrRiObo0oOU53YVUfsFLNCEwC5awcvv%2FR8dm40zJljy2XvjiTUDifNMMubDQvJQRWYGKoHJHJTYGqfun1AlZO6qtlejtOsFUk237EaINl38Oe2MdcAULZ0rfrOaPvrUnY%2Bn6TPSLj%2BVmzT2jt0o%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20240312T072859Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAQ3PHCVTYWT63FFFK%2F20240312%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=0d7cb6f4aa0030af56f00c005bafb10743c8b9bb6d857d19d03a2f746fef10ef&hash=d7602caaa3ae251da2d753686821588fc2a81588e1d92a3a0564416b8fcf7305&host=68042c943591013ac2b2430a89b270f6af2c76d8dfd086a07176afe7c76c2c61&pii=S2405918821000040&tid=spdf-375ea719-0f1d-488c-9c9f-bcc500513aa2&sid=489ce44175ed8446787ac06998852c402a04gxrqb&type=client&tsoh=d3d3LnNjaWVuY2VkaXJlY3QuY29t&ua=021a59595c5d535556&rr=86321213ab2cc291&cc=at)

- [PitchBooks is using it](https://techcrunch.com/2023/03/20/pitchbooks-new-tool-uses-ai-to-predict-which-startups-will-successfully-exit/)

- Other paper suggested: [bad investments](https://deliverypdf.ssrn.com/delivery.php?ID=160086092066064069071086082096113119006019033078069020110118067122084089093001072073037033029008062055124090098098001019014122053027061051031007108076070089017099022010042038102124064023104003117071025114127086118125072093117067029027090024020001108067&EXT=pdf&INDEX=TRUE) + [criticisms](https://news.ycombinator.com/item?id=32042187)

- [Kaggle dataset](https://www.kaggle.com/code/fpolcari/startup-success-prediction#conclusions-and-main-findings)
