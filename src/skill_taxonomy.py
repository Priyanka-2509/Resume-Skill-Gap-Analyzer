SKILL_TAXONOMY = {
    "Technology": ["python", "java", "javascript", "sql", "aws", "docker", "react", "node.js", "html", "css"],
    
    "Business & Management": ["project management", "stakeholder management", "business analysis", "strategic planning", "p&l management", "operations", "crm", "salesforce", "agile", "scrum"],
    
    "Travel & Tourism": ["gds", "amadeus", "sabre", "itinerary planning", "travel consulting", "visa processing", "hotel booking", "tour management", "customer service", "destination knowledge"],
    
    "Marketing & Sales": ["seo", "digital marketing", "social media", "content strategy", "lead generation", "market research", "email marketing", "public relations", "sales forecasting"],
    
    "Finance & Accounting": ["financial modeling", "accounting", "auditing", "taxation", "budgeting", "quickbooks", "excel", "financial reporting", "risk management"],
    
    "Soft Skills": ["communication", "leadership", "problem solving", "time management", "teamwork", "adaptability", "negotiation", "conflict resolution", "public speaking", "critical thinking"]
}

SKILL_WEIGHTS = {
    # Tech
    "python": 2.0, "aws": 2.0,
    # Business
    "strategic planning": 2.0, "project management": 1.5,
    # Travel
    "amadeus": 2.0, "gds": 2.0, "itinerary planning": 1.5,
    # Finance
    "financial modeling": 2.0, "auditing": 1.8,
    # Soft Skills 
    "leadership": 1.5, "negotiation": 1.5, "communication": 1.2
}
