# RAG-Enhanced Forensic Linkage Tool for Cybercrime Investigations

An offline, air-gapped GraphRAG platform engineered to correlate digital evidence across encrypted chat logs, network telemetry, and cryptocurrency transaction ledgers.

## Project Structure
- `data/`: Synthetic case evidence (Operation ShadowVault)
- `src/`: Python source code (Dataset generator, Parsers, Neo4j Graph DB, Qdrant Vector DB, Streamlit Dashboard)
- `docs/`: Technical reports, system architecture diagrams, and user manuals

## Quick Start
```bash
pip install -r requirements.txt
python src/generate_dataset.py