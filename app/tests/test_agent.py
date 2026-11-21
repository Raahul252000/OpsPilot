from app.services.agent.incident_investigator_agent import investigate_with_real_agent


if __name__ == '__main__':

    result = investigate_with_real_agent(
        incident_question="""
        Service: user-api
    
        Incident: The application is experiencing database
        connection timeouts and intermittent HTTP 500 errors.
    
        Investigate the incident using the available tools.
        """
    )

    print("\n========== INVESTIGATION REPORT ==========\n")
    print(result)