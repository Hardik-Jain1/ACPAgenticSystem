from mcp.server.fastmcp import FastMCP
import json

mcp = FastMCP("serch_engine")

@mcp.tool()
def doctor_search(state: str) -> str:
    """
    This tool returns doctors that may be near you.
    Args:
        state (str): the two letter state code that you live in.
        Example payload: "CA" for California.   
    Returns:
        str: A list of doctors that may be near you.
        Example Response "{"DOC001":{"name":"Dr John James", "specialty":"Cardiology"...}...}"
    """
    with open("doctors.json", "r") as f:
        doctors = json.load(f) 
    
    return str(doctors)

if __name__ == "__main__":
    mcp.run(transport="stdio")