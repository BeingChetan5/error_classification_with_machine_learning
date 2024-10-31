from jira import JIRA
import re
import pandas as pd


def connect_to_jira():
    jira_token = "ATATT3xFfGF0OHPgKxHofZWOulKNTHoN5FoNmet_MyFV1trGsj2AQoPDLuWEHEa0dFn1jOiYICMrK4c9kC-SEnQE-GR9q3Myh8yeQ28pPbUzpGNzdHA023zWJb-Iwns_EwFBpFe7oJbwm8zeX_g5FtXuiOubTPBB6uOFiZDyoOuJzjD0VeUdFgQ=39805F57"
    options = {'server': 'https://beingcm.atlassian.net'}
    conn = JIRA(options, basic_auth=("chetanmirajkar5@gmailcom", jira_token))
    print("Jira connection established:", conn)
    print(conn.projects())
    return conn


def get_all_jira(conn):
    all_jira = conn.search_issues('Project = "Client Automation" AND Type = Bug')
    print("All Jira:", all_jira)


def create_dataframe(conn, all_jira):
    df = {'error_msg': [],
          'category': []}
    if all_jira:
        for jira in all_jira:
            issue = conn.issue(jira)
            error_type = issue.fields.labels
            msg = issue.fields.description
            df['error_msg'] = msg
            df['category'] = error_type
    return df


def get_df():
    conn = connect_to_jira()
    all_jira = get_all_jira(conn)
    data = create_dataframe(conn, all_jira)
    df = pd.DataFrame(data)
    return df

if __name__ == '__main__':
    get_df()