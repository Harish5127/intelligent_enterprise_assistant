import json, os
def load_sample_kb():
    # create sample KB files if missing
    os.makedirs('data', exist_ok=True)
    hr_path = os.path.join('data','hr_faq.json')
    it_path = os.path.join('data','it_support.json')
    if not os.path.exists(hr_path):
        hr = [
            {"question":"What are the leave policies?","answer":"Employees are entitled to 18 days of paid leave per year. For more details check the HR portal."},
            {"question":"How do I apply for maternity leave?","answer":"Submit a request to HR with supporting documents. The HR team will process it within 7 working days."}
        ]
        with open(hr_path,'w', encoding='utf-8') as f:
            json.dump(hr,f, indent=2)
    if not os.path.exists(it_path):
        it = [
            {"question":"How to reset my password?","answer":"Use the 'Forgot Password' link on the SSO page or contact IT support."},
            {"question":"My laptop is not connecting to VPN","answer":"Check that VPN client is updated and your credentials are valid. If issue persists, raise a ticket."}
        ]
        with open(it_path,'w', encoding='utf-8') as f:
            json.dump(it,f, indent=2)
load_sample_kb()
