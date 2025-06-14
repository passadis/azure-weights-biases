# import weave

# # Replace with your actual W&B username and project name
# runs = weave.ref("your-wandb-username/rag-demo").runs()

# weave.panel.Group({
#     "🧠 RAG Inference Logs": runs.table().select([
#         "query",
#         "retrieved_doc_ids",
#         "retrieved_text",
#         "generated_answer",
#         "latency_ms"
#     ]),
#     "📢 Feedback Logs": runs.table().select([
#         "feedback_query",
#         "user_feedback"
#     ])
# })

import weave
from weave import panel

@weave.type()
def rag_dashboard():
    runs = weave.ref("passadis/rag-demo").runs()

    return panel.Group({
        "📊 RAG Queries": runs.table().select([
            "query", "retrieved_doc_ids", "generated_answer", "latency_ms"
        ]),
        "📈 Feedback Sentiment Counts": runs.table().groupby("feedback_type").count(),
        "📋 Feedback Table": runs.table().select([
            "feedback_query", "user_feedback", "feedback_type"
        ])
    })
