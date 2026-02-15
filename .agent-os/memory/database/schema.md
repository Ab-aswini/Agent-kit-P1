# Database Schema

> Last Updated: [DATE]

## Tables

### Template
```
Table: table_name
Columns:
  - id: UUID PRIMARY KEY
  - created_at: TIMESTAMP NOT NULL DEFAULT NOW()
  - updated_at: TIMESTAMP NOT NULL DEFAULT NOW()
  - [column]: [TYPE] [CONSTRAINTS]
Indexes:
  - idx_table_column ON table_name(column)
Relationships:
  - table_name.foreign_id -> other_table.id
```

---

[Tables will be documented here as they are created]
