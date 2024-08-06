import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import StructuredTool


def create_agent(llm, tools, system_prompt):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    return AgentExecutor(
        agent=create_openai_tools_agent(llm, tools, prompt), tools=tools, verbose=True
    )


llm = ChatOpenAI(model="gpt-4", temperature=0)


def create_project_folder(project_name: str) -> str:
    """Create a new folder with the given project name."""
    try:
        os.makedirs(project_name, exist_ok=True)
        return f"Project folder '{project_name}' created successfully."
    except Exception as e:
        return f"Error creating project folder: {str(e)}"


create_folder_tool = StructuredTool.from_function(
    func=create_project_folder,
    name="create_project_folder",
    description="Create a new folder with the given project name in the current directory.",
)


def write_file(content: str, project_name: str, filename: str) -> str:
    """Create and write content to a file in the project folder."""
    file_path = os.path.join(project_name, filename)
    with open(file_path, "w") as f:
        f.write(content)
    return f"File '{filename}' has been created and written successfully in the '{project_name}' folder."


write_file_tool = StructuredTool.from_function(
    func=write_file,
    name="write_file",
    description="Create and write content to a file in the project folder. Input should be the content to write, the project name, and the filename.",
)


def read_file(project_name: str, filename: str) -> str:
    """Read content from a file in the project folder."""
    file_path = os.path.join(project_name, filename)
    try:
        with open(file_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return f"File '{filename}' not found in the '{project_name}' folder."


read_file_tool = StructuredTool.from_function(
    func=read_file,
    name="read_file",
    description="Read content from a file in the project folder. Input should be the project name and the filename.",
)

# D2 Diagram Agent
d2_agent = create_agent(
    llm,
    [write_file_tool, read_file_tool],
    """You are a D2 diagram expert. When given a project overview and solution, create a D2 diagram that represents the main components and their interactions.
    Use the read_file tool to read the README.md file for the project overview and solution.
    Use the write_file tool to save the D2 code to a diagram.d2 file in the project folder.
    Always start your D2 code with the direction (e.g., direction: right).
    Use default shapes and styles. Do not use any custom shapes or styles.
    Focus on creating a high-level architecture diagram that shows the main components and their relationships.
    Ensure the diagram is easy to read and understand.""",
)


def create_d2_diagram(project_name: str) -> str:
    """Create a D2 diagram based on the README overview and solution, and save it to diagram.d2 in the project folder."""
    result = d2_agent.invoke(
        {
            "input": f"Read the README.md file in the {project_name} folder, extract the overview and solution sections, and create a D2 diagram based on this information. Save the D2 code to diagram.d2 in the {project_name} folder.",
            "chat_history": [],
        }
    )
    return result["output"]


d2_diagram_tool = StructuredTool.from_function(
    func=create_d2_diagram,
    name="create_d2_diagram",
    description="Create a D2 diagram based on the README overview and solution, and save it to diagram.d2 in the project folder.",
)

# Tech Spec Writer Agent
tech_spec_agent = create_agent(
    llm,
    [write_file_tool],
    """You are a technical specification writer. When given a product or feature, create a detailed tech spec including 
    sections for Overview, Problem, and Solution. Use the write_file tool to create 
    a README.md file with the tech spec in the project folder.""",
)


def write_tech_spec(product: str, project_name: str) -> str:
    """Write a technical specification for a given product or feature and create a README in the project folder."""
    result = tech_spec_agent.invoke(
        {
            "input": f"Write a technical specification for {product} and create a README.md with the spec in the {project_name} folder",
            "chat_history": [],
        }
    )
    return result["output"]


tech_spec_tool = StructuredTool.from_function(
    func=write_tech_spec,
    name="write_tech_spec",
    description="Write a technical specification for a given product or feature and create a README.md file in the project folder",
)

# Jira Ticket Creator Agent
jira_agent = create_agent(
    llm,
    [read_file_tool, write_file_tool],
    """You are a Jira ticket creator. Based on the D2 diagram and the technical specification, create Jira ticket definitions.
    Use the read_file tool to read the diagram.d2 and README.md files for the project information.
    Create tickets for each main component or feature identified in the diagram and spec.
    For each ticket, include the following fields: name, summary, story points, and relation to other tickets.
    Estimate story points on a scale of 1, 2, 3, 5, 8, 13, with 13 being the most complex.
    List the tickets in the order they should be completed for optimal project progression.
    Use the write_file tool to save the ticket definitions to a JIRA_TICKETS.md file in the project folder.""",
)


def create_jira_tickets(project_name: str) -> str:
    """Create Jira ticket definitions based on the D2 diagram and README, and save them to JIRA_TICKETS.md in the project folder."""
    result = jira_agent.invoke(
        {
            "input": f"Read the diagram.d2 and README.md files in the {project_name} folder, create Jira ticket definitions based on this information, and save them to JIRA_TICKETS.md in the {project_name} folder.",
            "chat_history": [],
        }
    )
    return result["output"]


jira_tickets_tool = StructuredTool.from_function(
    func=create_jira_tickets,
    name="create_jira_tickets",
    description="Create Jira ticket definitions based on the D2 diagram and README, and save them to JIRA_TICKETS.md in the project folder.",
)

# Main Agent
main_agent = create_agent(
    llm,
    [create_folder_tool, tech_spec_tool, d2_diagram_tool, jira_tickets_tool],
    """You are a project manager assistant. Follow these steps for each task:
    1. Use the create_project_folder tool to create a folder with the project name.
    2. Use the write_tech_spec tool to create a technical specification and README.md file in the project folder.
    3. Use the create_d2_diagram tool to create a diagram based on the README overview and solution.
    4. Use the create_jira_tickets tool to generate Jira ticket definitions based on the D2 diagram and README.
    Always perform these steps in order. Ensure all files are created within the project folder.""",
)

# Test the main agent
result = main_agent.invoke(
    {
        "input": """Create a new project called 'GlobalWarming'. Write a tech spec for things people can do to help mitigate global warming. Then, create a D2 diagram based on the README overview and solution. Finally, 
    generate Jira ticket definitions based on the diagram and spec.""",
        "chat_history": [],
    }
)
print(result["output"])
