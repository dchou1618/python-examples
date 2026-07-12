from collections import defaultdict, deque
from typing import List
def accountsMerge(accounts: List[List[str]]) -> List[List[str]]:
    adj_lst = defaultdict(set)
    email_to_accounts = dict()
    # connected components per account
    for account in accounts:
        emails = account[1:]
        name = account[0]
        for dst in emails:
            email_to_accounts[dst] = name
            adj_lst[emails[0]].add(dst)
            adj_lst[dst].add(emails[0])
    visited = set()
    result = []
    for email in adj_lst:
        if email in visited:
            continue
        email_queue = deque([email])
        visited.add(email)
        component = []
        while email_queue:
            node = email_queue.popleft()
            component.append(node)

            for neighbor in adj_lst[node]:
                if neighbor not in visited:
                    email_queue.append(neighbor)
                    visited.add(neighbor)
        
        component.sort()
        result.append([email_to_accounts[email]]+component)
    return result