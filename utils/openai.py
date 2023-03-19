import openai

from config import settings

openai.api_key = settings.OPENAI_API_KEY

def get_matching_result(tutors: list, description: str):
    tutor_prompt = "\n".join([
        f"{tutor['id']}|{tutor['student']}|{tutor['subject']}|{tutor['time']}" 
        for tutor in tutors
    ])
    prompt = f"""你是一個家教人力網站，擁有許多由家長刊登的家教需求案件，資料包含案件編號、學生年級、科目與時薪、時間(以"|"做區隔)。今天有位願意提供家教勞務的老師，簡述了自己可以提供的教學內容，你要依照家教老師能提供的服務與需求案件做搓合，並將所有配對的結果列出來，只需條列出案件編號

    ===需求案件開始===
    {tutor_prompt}
    ===需求案件結束===

    ===家教老師簡述開始===
    {description}
    ===家教老師簡述結束===

    ===配對結果===
    """
    print(prompt)

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=512,
        top_p=0.4,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["===配對結果==="]
    )
    return response["choices"][0]["text"]
