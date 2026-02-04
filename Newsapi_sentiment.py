import requests

from transformers import pipeline

#Search tightening
API_KEY = open("API_KEY").read()

#example "Canadian Tire AND (energy OR stocks OR mining OR demand OR reactor)"
query = "Data center AND (ETF OR stock OR energy OR power OR index)"
date = '2026-01-05'
#example "iran OR weapon OR bomb OR sanction OR war OR military"
exclude = "Iran OR weapon OR bomb OR sanction OR military OR warfare OR leak"
domains = ""


pipe = pipeline("text-classification", model="ProsusAI/finbert")

url = (
    'https://newsapi.org/v2/everything?'
    f"q={query} NOT {exclude}&"
    f'from={date}&'
    f'domains={domains}&'
    'sortBy=popularity&'
    f'apiKey={API_KEY}'
)

response = requests.get(url)

print(response.status_code)
print(response.json())

data = response.json()
articles = data.get("articles", [])

total_score = 0
num_articles = 0

for i, article in enumerate(articles):
    print(f'Title: {article["title"]}')
    print(f'Link: {article["url"]}')
    print(f'description: {article["description"]}')
    
    sentiment = pipe(article['content'])[0]
    
    print(f'Sentiment {sentiment["label"]}, Score: {sentiment["score"]}')
    print('_' * 40)
    
    if sentiment['label'] == 'positive':
        total_score += sentiment['score']
        num_articles += 1
    elif sentiment['label'] == 'negative':
        total_score -= sentiment['score']
        num_articles += 1
        
if len(articles) == 0:
    print("No articles returned. Try a different date/query.")
    quit()
        
final_score = total_score / num_articles
print(f'Overall Sentiment: {"Positive" if final_score >= 0.15 else "Negative" if final_score <= -0.15 else "Neutral"} {final_score}')


        
        