# Testing Skill

> Loaded by: QA Division agents | Version: 1.0

## Test Pyramid
```
        /  E2E  \        <- Few, slow, expensive
       / Integr. \      <- Some, moderate
      /   Unit    \     <- Many, fast, cheap
```

## Unit Test Pattern (Arrange, Act, Assert)
```python
def test_user_creation():
    # Arrange
    user_data = {"name": "Alice", "email": "alice@test.com"}
    # Act
    user = UserService.create(user_data)
    # Assert
    assert user.name == "Alice"
    assert user.id is not None
```

## Coverage: 80% minimum, 100% on critical paths

## Naming: `test_[unit]_[scenario]_[expected_result]`

## Mocking
- Mock external services, not the thing under test
- Prefer dependency injection over monkey patching

## Anti-Patterns
- Tests dependent on execution order or external services
- Tests without assertions; flaky timing-dependent tests
- Testing implementation instead of behavior

## Checklist
- [ ] All public APIs have tests
- [ ] Edge cases covered
- [ ] Tests are independent and deterministic
- [ ] Coverage above 80%
- [ ] Test names describe behavior
