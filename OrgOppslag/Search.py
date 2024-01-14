from .SupportFunctions import get_org_nr, get_brreg_info, format_company_name, generate_suggested_emails, check_emails, get_external_info, find_similar_companies, generate_context
import pandas as pd

def search_company(company, validate_emails=False, similar_results=5, google_search_count=1):
    # Get Org. Nr.
    org_nr = get_org_nr(company)
    if isinstance(org_nr, pd.DataFrame):
        # if the result is a dataframe with companies, find similar companies and return list
        return find_similar_companies(company, org_nr, similar_results)
    if not org_nr:
        return None
    
    # Get info from brreg
    brreg_info = get_brreg_info(org_nr)
    if not brreg_info:
        return None
    
    # Get different formats of the company name
    formatted_names = format_company_name(brreg_info)

    # Generate List of suggested emails
    suggested_emails = generate_suggested_emails(formatted_names)
    
    # Validate emails using an email checker
    valid_emails = [] # Defaults to no emails
    if validate_emails == True:
        valid_emails = check_emails(suggested_emails)

    # Get external info
    external_info = get_external_info(formatted_names["clean_name"], google_search_count=google_search_count)

    context = generate_context(external_info=external_info, brreg_info=brreg_info)

    return {"brreg_info" : brreg_info,
            "external_info" : external_info,
            "context" : context,
            "valid_emails" : valid_emails,
            "suggested_emails" : suggested_emails,
            "formatted_names" : formatted_names}
