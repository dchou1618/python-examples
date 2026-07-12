from typing import List, Dict
def deduplicate(findings: List[Dict]) -> List[Dict]:
    pass

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