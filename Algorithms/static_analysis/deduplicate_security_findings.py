from typing import List, Dict
def deduplicate(findings: List[Dict]) -> List[Dict]:
    seen = set()
    output = []
    for finding in findings:
        key = (finding["file"], finding["line"], finding["rule"])
        if key not in seen:
            seen.add(key)
            output.append(finding)
        
    return output

findings = [
 {
  "file":"a.py",
  "line":10,
  "rule":"SQL001"
 },
 {
  "file":"a.py",
  "line":10,
  "rule":"SQL001"
 },
 {
  "file":"b.py",
  "line":20,
  "rule":"XSS001"
 }
]

print(deduplicate(findings))