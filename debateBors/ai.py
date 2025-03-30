import json
import requests

MODEL_NAME = "llama3"  # Can be changed to other models like "tinyllama"

JUDGE_PROMPT = r"""You are a fair and impartial debate judge. Evaluate the following pro and con arguments.

    topic:
    {topic}

    question:
    {question}

    pro argument:
    {pro_arguments}

    con argument:
    {con_arguments}

    Score each argument on a scale of 1-10 for:    
    1. Logical coherence
    2. Evidence quality
    3. Persuasiveness
    4. Relevance to topic
    5. Relevance to question

    Provide a brief explanation for each score, then determine the overall winner.
    Format your response as JSON with the following structure:
    {{
      "pro_scores": {{
        "logic": <score>,
        "evidence": <score>,
        "persuasiveness": <score>,
        "relevance": <score>
      }},
      "con_scores": {{
        "logic": <score>,
        "evidence": <score>,
        "persuasiveness": <score>,
        "relevance": <score>
      }},
      "pro_feedback": "<brief explanation>",
      "con_feedback": "<brief explanation>",
      "winner": "<pro or con>"
    }}
    """

ASSISTANCE_PROMPT = r"""You are given a debate topic "{topic}". Generate {number_of_rounds} subtopics for discussion.

       Instructions:
       1. Generate exactly {number_of_rounds} debate questions
       2. Each question must be under 20 characters
       3. Each question must end with a question mark
       4. Return ONLY a JSON object with this exact structure
       5. make sure it is in debating format that challenges both side:

       {{
         "topics": [
           "Short title 1?",
           "Short title 2?",
           "Short title 3?"
         ]
       }}

       Your response must be valid JSON with no additional text or explanations.
       """


def call_api(prompt):
    """Call the Ollama API with the given prompt"""
    try:
        response = requests.post('http://localhost:11434/api/generate',
                                 json={
                                     'model': MODEL_NAME,
                                     'prompt': prompt,
                                     'stream': False,
                                     'format': 'json'
                                 })
        response.raise_for_status()
        result = response.json()
        return json.loads(result['response'])
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Ollama: {e}")
        return None
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error parsing response: {e}")
        return None


def validate_questions(questions):
    """Validate the structure of questions"""
    if not isinstance(questions, dict) or 'topics' not in questions:
        return False
    if not isinstance(questions['topics'], list):
        return False
    if not all(isinstance(topic, str) for topic in questions['topics']):
        return False
    return True


def create_sub_topic_questions(topic, number_of_rounds):
    """Generate subtopic questions for the debate"""
    for attempts in range(5):  # Try up to 5 times
        try:
            questions = call_api(ASSISTANCE_PROMPT.format(
                topic=topic,
                number_of_rounds=number_of_rounds
            ))

            if validate_questions(questions):
                return questions['topics']

            print(f"Attempt {attempts + 1}: Invalid question format. Retrying...")
        except Exception as e:
            print(f"Attempt {attempts + 1} failed: {e}")

    # Fallback if API fails
    print("Failed to generate questions. Using fallback questions.")
    return [f"Question {i + 1}?" for i in range(number_of_rounds)]


def judge(topic, question, con_args, pro_args):
    """Judge the debate arguments"""
    filled_prompt = JUDGE_PROMPT.format(
        topic=topic,
        question=question,
        pro_arguments=pro_args,
        con_arguments=con_args
    )

    try:
        result = call_api(filled_prompt)

        # Validate result structure
        if not all(key in result for key in ['pro_scores', 'con_scores', 'pro_feedback', 'con_feedback']):
            print("Invalid judging result structure")
            # Return fallback scores if validation fails
            return {
                "pro_scores": {"logic": 5, "evidence": 5, "persuasiveness": 5, "relevance": 5},
                "con_scores": {"logic": 5, "evidence": 5, "persuasiveness": 5, "relevance": 5},
                "pro_feedback": "Scoring failed. Default score assigned.",
                "con_feedback": "Scoring failed. Default score assigned.",
                "winner": "Draw due to scoring failure"
            }

        return result
    except Exception as e:
        print(f"Error in judging: {e}")
        # Return fallback scores
        return {
            "pro_scores": {"logic": 5, "evidence": 5, "persuasiveness": 5, "relevance": 5},
            "con_scores": {"logic": 5, "evidence": 5, "persuasiveness": 5, "relevance": 5},
            "pro_feedback": "Error occurred during judging.",
            "con_feedback": "Error occurred during judging.",
            "winner": "Draw due to error"
        }

#
# # For testing
# if __name__ == '__main__':
#     test_topic = "Education reform"
#     test_questions = create_sub_topic_questions(test_topic, 2)
#     print("Generated questions:", test_questions)
#
#     test_result = judge(
#         test_topic,
#         test_questions[0] if test_questions else "Test question?",
#         "Schools need more funding because education is important.",
#         "We should focus on better allocation of existing resources instead."
#     )
#     print("Judging result:", json.dumps(test_result, indent=2))