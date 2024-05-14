# Определяем метрики precision, recall, F1
def calculate_metrics(predictions, true_tags, skill_tag_indices):
    """
    Расчет precision, recall и F1-score только для тегов B-SKILL и I-SKILL.
    
    predictions: Предсказания модели (после применения torch.max).
    true_tags: Истинные теги.
    skill_tag_indices: Индексы тегов B-SKILL и I-SKILL.
    """
    # Инициализация счетчиков для TP, FP, FN
    tp = 0
    fp = 0
    fn = 0

    # Преобразование векторов для удобства сравнения
    pred_flat = predictions.view(-1)
    true_flat = true_tags.view(-1)
    
    for skill_tag in skill_tag_indices:
        # True Positives: Предсказанный тег совпадает с истинным
        tp += ((pred_flat == skill_tag) & (true_flat == skill_tag)).sum().item()
        # False Positives: Предсказан тег, но истинный тег другой
        fp += ((pred_flat == skill_tag) & (true_flat != skill_tag)).sum().item()
        # False Negatives: Тег не был предсказан, хотя он есть
        fn += ((pred_flat != skill_tag) & (true_flat == skill_tag)).sum().item()

    # Расчет метрик
    precision = tp / (tp + fp) if tp + fp > 0 else 0
    recall = tp / (tp + fn) if tp + fn > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0

    return precision, recall, f1