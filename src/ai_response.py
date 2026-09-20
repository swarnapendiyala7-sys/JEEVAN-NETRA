from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


MODEL_NAME = "google/flan-t5-small"


def load_model():
    print("Loading JEEVAN AI response model...")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

    print("JEEVAN AI response model loaded.")

    return tokenizer, model


def generate_response(question, context, tokenizer, model):

    question_lower = question.lower()

    # FLOOD SAFETY
    if any(word in question_lower for word in [
        "flood",
        "flooding",
        "flooded",
        "heavy rain"
    ]):
        return (
            "During a flood:\n\n"
            "1. Move to higher and safer ground when instructed.\n"
            "2. Do not walk or drive through moving flood water.\n"
            "3. Avoid electrical equipment and fallen power lines.\n"
            "4. Keep children away from flooded roads and drainage channels.\n"
            "5. Follow instructions from local authorities."
        )

    # ELECTRICAL SAFETY
    if any(word in question_lower for word in [
        "electrical",
        "electricity",
        "power line",
        "electric hazard",
        "short circuit"
    ]):
        return (
            "For electrical hazards:\n\n"
            "1. Avoid touching electrical equipment in wet or flooded areas.\n"
            "2. Stay away from fallen or exposed power lines.\n"
            "3. Do not enter areas that may contain electrical hazards.\n"
            "4. Report electrical damage to the appropriate maintenance "
            "or emergency authority.\n"
            "5. Follow official safety instructions."
        )

    # ROAD SAFETY
    if any(word in question_lower for word in [
        "road",
        "pothole",
        "bridge",
        "traffic",
        "blocked road"
    ]):
        return (
            "For road and infrastructure safety:\n\n"
            "1. Avoid severely flooded or structurally damaged roads.\n"
            "2. Do not cross barricaded or restricted areas.\n"
            "3. Avoid unnecessary travel through low-lying roads during "
            "heavy rainfall.\n"
            "4. Report potholes, cracks, damaged bridges, fallen trees "
            "and blocked roads.\n"
            "5. Keep access clear for emergency vehicles."
        )

    # FLAN-T5 FALLBACK
    prompt = f"""
You are JEEVAN AI, a community safety assistant.

Use only the information in the safety context.

Question:

{question}

Safety context:

{context}

Give a short practical answer in 2 or 3 sentences.

Do not invent information.
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=100,
        do_sample=False
    )

    answer = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return answer.strip()


if __name__ == "__main__":

    tokenizer, model = load_model()

    question = "What should I do during a flood?"

    context = """
    During a flood:

    Move to higher and safer ground when instructed.

    Do not walk or drive through moving flood water.

    Avoid electrical equipment and fallen power lines.

    Follow instructions from local authorities.

    Keep children away from flooded roads and drainage channels.
    """

    answer = generate_response(
        question,
        context,
        tokenizer,
        model
    )

    print()
    print("=" * 55)
    print("JEEVAN AI RESPONSE")
    print("=" * 55)
    print(answer)
    print("=" * 55)