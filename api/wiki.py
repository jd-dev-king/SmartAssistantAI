import wikipediaapi


def search_wiki(topic):

    try:

        wiki = wikipediaapi.Wikipedia(
            user_agent="SmartAssistantAI/1.0",
            language="en"
        )

        page = wiki.page(topic)


        if not page.exists():

            return (
                "I couldn't find that topic. "
                "Try another search."
            )


        summary = page.summary


        if len(summary) > 600:
            summary = summary[:600] + "..."


        return summary


    except Exception as e:

        return f"Wikipedia error: {e}"