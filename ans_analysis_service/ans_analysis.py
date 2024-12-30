from sentence_transformers import util
import torch


# Define positivity evaluation
def evaluate_positivity(analyzer, answer):
    """
    Evaluates the positivity of the candidate's answer using VADER.
    
    Parameters:
    - answer (str): The candidate's response.
    
    Returns:
    - positivity_score (float): A score between 0 and 1 representing sentiment positivity.
    """
    sentiment_scores = analyzer.polarity_scores(answer)
    positivity_score = sentiment_scores['pos']  # Extract the positive sentiment score
    return positivity_score

# Define experience evaluation
def evaluate_experience(sentence_model, answer, required_skills):
    answer_embedding = sentence_model.encode(answer, convert_to_tensor=True)
    skill_embeddings = sentence_model.encode(required_skills, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(answer_embedding, skill_embeddings)[0]
    max_similarity = torch.max(similarities).item()
    return min(max_similarity * 100, 100)  # Scale to 0-100 range

# Define culture fit evaluation
def evaluate_culture_fit(sentence_model, answer, culture_reference_texts):
    answer_embedding = sentence_model.encode(answer, convert_to_tensor=True)
    reference_embeddings = sentence_model.encode(culture_reference_texts, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(answer_embedding, reference_embeddings)[0]
    return similarities.mean().item()  # Average similarity score

# Define relevance evaluation
def evaluate_relevance(sentence_model, answer, question):
    answer_embedding = sentence_model.encode(answer, convert_to_tensor=True)
    question_embedding = sentence_model.encode(question, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(answer_embedding, question_embedding).item()
    return similarity * 100  # Scale to 0-100 range

# Main evaluation function
def evaluate_answer(question, answer, model, sentence_model, culture_reference_texts, required_skills):
    positivity = evaluate_positivity(model, answer)
    culture_fit = evaluate_culture_fit(sentence_model, answer, culture_reference_texts)
    relevance = evaluate_relevance(sentence_model, answer, question)
    experience = evaluate_experience(sentence_model, answer, required_skills)

    return {
        "Positivity": round(positivity, 2),
        "Culture Fit": round(culture_fit, 2),
        "Relevance": round(relevance, 2),
        "Experience": round(experience, 2)
    }

