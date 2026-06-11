# Proposal: mvp1-knowledge-ingestion

## Why
The continuous-learning RAG pipeline is the core differentiator ("the agent learns within the hour").

## What Changes
Add document upload (PDF/DOCX/Markdown/URL), chunking, embedding, indexing, and re-index on update.

## User-visible impact
A tenant uploads FAQs/how-tos/product docs; the agent reflects them shortly after.

## Rollback
Disable ingestion endpoint; existing indexes remain queryable.
