# LungScreenSDM-AI-Assistant-for-Shared-Decision-Making
LLM-powered assistant for lung cancer screening decisions. Combines FAISS-based semantic search with Zephyr-7B to deliver grounded, SDM-aligned responses. Includes hallucination checks, patient simulation testing, and is deployable via Streamlit + Docker.

Features
Semantic Search: Embeds PubMed-derived texts using all-mpnet-base-v2 and retrieves relevant documents with FAISS.
LLM Integration: Uses Zephyr-7B for answer generation based on top-ranked contextual documents.
SDM-Aligned Prompting: Structured prompts ensure answers follow SDM principles: Eligibility, Benefits, Risks, Patient Questions, and Reassurance.
Grounding & Hallucination Checks: Responses default to "not mentioned" when context is insufficient.
Evaluation Pipeline: Includes a CSV-based system for scoring factuality, clarity, and helpfulness using real-world patient scenarios. 

How It Works
User Input: Patient or provider enters a question.
Embedding & Retrieval: FAISS retrieves top 5 documents from pre-embedded PubMed texts.
Prompt Assembly: Retrieved content is fed into a structured prompt aligned with SDM criteria.
LLM Response: Zephyr-7B generates a grounded answer, avoiding hallucinations.
Output: Answer is returned in plain, patient-friendly language.

Evaluation
CSV-based framework to assess responses along 3 axes: factuality, clarity, and helpfulness.
Includes auto-flags for hallucination risks and unclear phrasing.
Realistic patient scenarios used for robustness testing.

In Progress
GCP deployment via Cloud Run or Compute Engine
Integration with NCI Lung Screening Risk Calculator API
