import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .langchain_bot import ask_chatbot


@require_POST
def chatbot_api(request):

    print("\n==============================")
    print("CHATBOT API CALLED")
    print("==============================")


    try:

        data = json.loads(request.body)

        print("REQUEST DATA:")
        print(data)


        prompt = data.get("message", "").strip()

        print("PROMPT:")
        print(prompt)


        if not prompt:

            return JsonResponse({
                "success": False,
                "error": "Message is required."
            }, status=400)


        print("\nCalling LangChain...")


        answer = ask_chatbot(
            prompt=prompt,
            thread_id="test-user"
        )


        print("\nLANGCHAIN RESPONSE:")
        print(answer)


        return JsonResponse({
            "success": True,
            "answer": answer
        })


    except Exception as e:

        print("\nCHATBOT ERROR:")
        print(repr(e))


        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500)