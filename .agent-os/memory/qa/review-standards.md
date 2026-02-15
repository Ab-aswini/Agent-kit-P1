# Code Review Standards

## Must Check
1. Correctness - Does the code do what it should?
2. Security - Any vulnerabilities introduced?
3. Performance - Any obvious bottlenecks?
4. Readability - Can another developer understand this?
5. Conventions - Does it follow project conventions?
6. Tests - Is test coverage adequate?
7. Error Handling - Are errors handled gracefully?
8. Edge Cases - Are boundary conditions covered?

## Review Output Format
```json
{
  "status": "approve | request_changes | reject",
  "summary": "Brief overall assessment",
  "findings": [
    {
      "severity": "critical | major | minor | suggestion",
      "file": "path/to/file",
      "line": 0,
      "description": "What was found",
      "suggestion": "How to fix it"
    }
  ]
}
```
