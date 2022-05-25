# shoe-db
Toy backend for shoe recommendation


## Code Diagram  
```mermaid
flowchart LR
db1[(Users)] --> py1([create_links])
py1 --> py2([load_links])
py2 --> db2[(Shoe Links)]
db2 --> py3([create_shoe_recs])
py3 --> json1[[Shoe Recommendations]]


db1 -. User adds/deletes shoes .-> db2
db1 -. User adds shoes .-> db3[(Interactions)]
json1 -. User interactions stored .-> db3
db3 --> py3
```

## Data Diagram
``` mermaid
flowchart TB
    subgraph USERS
    db1[(Equipment)]
    end

db1 --> db2[(Shoe Links)]
    subgraph SHOE RECOMMENDATION
    db2 --> db3[(Interactions)]
    db3 --> db2
    end
```