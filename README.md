# YugiAI

## Purpose 
A specialized AI Judge designed to help determine and resolve complex Yu-Gi-Oh! TCG rulings.

---

## Features

* **RAG-Based Ruling Engine**: Leverages a Retrieval-Augmented Generation (RAG) architecture to answer queries by synthesizing card text, rulebook mechanics, and official rulings.
* **PSCT Logic Parsing**: Implements a custom parser to break down Problem-Solving Card Text (PSCT) into logical components: **Conditions**, **Cost/Actions**, and **Effects**.
* **Automated Rulebook Processing**: Downloads and sections the official Rulebook (Version 10) into searchable chunks using PDF block detection.
* **Live Context Retrieval**: Extracts card names from user queries via regex to fetch specific card text and official rulings on-the-fly.
* **High-Performance Ingestion**: Processes over 12,000 cards using a parallelized pipeline to extract rich metadata including archetypes, attributes, and materials for Extra Deck monsters.

---

## Technical Stack

| Component | Technology |
| :--- | :--- |
| **LLM** | Google Gemini (`gemini-3-pro-preview`) |
| **Vector Database** | ChromaDB (Persistent Client) |
| **PDF Extraction** | PyMuPDF (`fitz`) |
| **Data Processing** | Python, `concurrent.futures`, `re`, `json` |
| **External API** | YGOPRODeck API |

---

## Project Structure

### `parser/`
* `psct_parser.py`: Logic for decomposing raw card text into game-mechanic segments.
* `process_rulebook.py`: Automated tool for downloading and chunking the official rulebook PDF.
* `clean_all_cards.py`: Normalizes card data and extracts specialized sections for Pendulum and Extra Deck cards.
* `parallel_parser.py`: Multi-threaded processing for efficient bulk data cleaning.

### `vector_db/`
* `ingest_cards_to_chroma.py`: Ingests parsed cards with judge-level metadata into ChromaDB.
* `ingest_rules_to_chroma.py`: Stores game engine mechanics and rulebook sections for semantic retrieval.

### Core Logic
* **`judge_query.py`**: The main `YugiJudge` interface that manages entity extraction, context gathering, and LLM prompt generation.

---

## Setup & Usage

1.  **API Configuration**: Set your `GOOGLE_API_KEY` in your environment variables.
2.  **Data Acquisition**: Run `download_all_cards.py` to fetch the raw database from YGOPRODeck.
3.  **Data Preparation**: Execute `parallel_parser.py` and `process_rulebook.py` to prepare the JSON datasets.
4.  **Database Ingestion**: Run the scripts in the `vector_db/` folder to initialize the local ChromaDB vector store.
5.  **Querying the Judge**: Use `judge_query.py` to input a query and receive a ruling supported by citations and reasoning.