import warnings
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize

nltk.download("punkt")
warnings.filterwarnings("ignore")

# Функция для BIO-разметки слов-токенов
def create_bio_tagged_data(id, description, skills_str):
    # Токенизация списка навыков
    skills = [skill.strip() for skill in str(skills_str).split(',')]
    skills_tokens = [word_tokenize(skill.lower()) for skill in skills]
    
    # Токенизация описания вакансии
    description_tokens = word_tokenize(description.lower())
    
    # Создание списка для итоговых данных
    data = []
    
    i = 0
    while i < len(description_tokens):
        token = description_tokens[i]
        tag = 'O'  # По умолчанию каждый токен не является навыком
        
        for skill_tokens in skills_tokens:
            if description_tokens[i:i+len(skill_tokens)] == skill_tokens:
                tag = 'B-SKILL'
                data.append((id, token, tag))
                for j in range(1, len(skill_tokens)):
                    i += 1
                    token = description_tokens[i]
                    tag = 'I-SKILL'
                    data.append((id, token, tag))
                break  # Прерываем цикл, так как совпадение найдено
                
        if tag == 'O':  # Если токен не был отмечен как часть навыка
            data.append((id, token, tag))
        i += 1
    
    return pd.DataFrame(data, columns=['id', 'token', 'tag'])

# Функция для применения BIO-разметки
def apply_to_row(row):
    return create_bio_tagged_data(row['id'], row['description'], row['skills_str'])

# Функция для базовой оценки 
def calculate_accuracy(df):
    # Считаем, сколько раз тег совпал с "O"
    correct_predictions = df['tag'].value_counts().get('O', 0)
    # Общее количество предсказаний
    total_predictions = len(df)
    # Вычисляем точность
    accuracy = correct_predictions / total_predictions
    return accuracy