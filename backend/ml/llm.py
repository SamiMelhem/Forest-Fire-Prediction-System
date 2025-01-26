from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun

load_dotenv()

def make_recommendation(time: float):
    class Queries(BaseModel):
        severity: str
        search_queries: list[str]

    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    structured_llm = model.with_structured_output(Queries)

    stage_1_prompt = """You are a public safety agent that specializes in wildfire safety precautions and recommendations. Given information about an impending wildfire, your job is to provide relevant, timely recommendations to the user.

    ## Severity Categories

    LOW SEVERITY:
    - No immediate danger to the user's location, but monitoring is advised.

    MODERATE SEVERITY:
    - Potential risk to the user's location within the next 3-7 days.
    - Preparatory actions are recommended.

    HIGH SEVERITY:
    - Immediate risk to the user's location within the next 1-3 days.
    - Urgent evacuation or critical safety measures are required.

    ## Inputs
    - Time for wildfire to arrive (days): {time}

    ## Task:
    - Predict the severity of the fire relative to the user's current situation
    - Based on your knowledge of the situation, brainstorm search queries that could provide the user with much-needed information (e.g., "where is the closest emergency shelter?", "what are some evacuation routes from X?", etc.). **Output the top 3 most relevant.**
    - Output ONLY valid JSON with this schema (Starting and Ending with this exact JSON format):
    {{
        "severity": "LOW | MODERATE | HIGH",
        "search_queries": ["list", "of", "relevant", "internet", "queries"]
    }}

    Output:
    """

    stage_1_output: Queries = structured_llm.invoke(stage_1_prompt.format(time=time))

    # Perform internet searches based on the outputs from stage 1
    search = DuckDuckGoSearchRun()
    search_results = []
    for query in stage_1_output.search_queries:
        search_results.append(search.invoke(query))


    class Recommendations(BaseModel):
        recommendations: list[str]

    stage_2_prompt = """You are an expert in wildfire safety. Given a list of credible, updated information from the internet and a "severity" category of an imminent wildfire, plesae consolidate that information into a list of concise, actionable points that the user can implement.

    ## Output Format:
    {{
        "recommendations": ["list", "of", "relevant", "recommendations"]
    }}

    ## Severity Categories

    LOW SEVERITY:
    - No immediate danger to the user's location, but monitoring is advised.

    MODERATE SEVERITY:
    - Potential risk to the user's location within the next 3-7 days.
    - Preparatory actions are recommended.

    HIGH SEVERITY:
    - Immediate risk to the user's location within the next 1-3 days.
    - Urgent evacuation or critical safety measures are required.

    # Inputs

    ## Internet search results
    {search_results}

    ## Wildfire severity
    {severity}

    # Output
    """

    structured_llm = model.with_structured_output(Recommendations)

    stage_2_output: Recommendations = structured_llm.invoke(stage_2_prompt.format(search_results=search_results, severity=stage_1_output.severity))
    
    return stage_2_output