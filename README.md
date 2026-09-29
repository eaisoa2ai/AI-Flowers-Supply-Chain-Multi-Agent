# 🌺 Royal FloraHolland AI Flower Recognition System

This repository serves as a sanitized, production-ready reference architecture built to demonstrate enterprise agentic patterns. 
It mirrors the architectural designs, multi-agent state machines, and evaluation frameworks I deploy in enterprise environments, stripped of proprietary data and corporate logic.

A production-grade multimodal AI agent system that identifies flowers from images and provides FloraHolland auction market intelligence using Pydantic AI and LangGraph.

![Project Banner](https://img.shields.io/badge/AI-Multimodal%20RAG-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Python](https://img.shields.io/badge/python-3.10%2B-blue)

---

## 🎯 Project Overview

This system demonstrates a **real-world AI agent** that mimics the workflow of Royal FloraHolland, the world's largest flower auction (€5B annual revenue, 10M flowers/day, 20K+ varieties).

### What It Does

1. **📸 Vision Analysis**: Extracts botanical features from flower images using Gemini 2.0 Flash
2. **🔍 Species Identification**: Matches against 102 flower species using ChromaDB RAG + DeepSeek V3.2 reasoning
3. **💰 Market Intelligence**: Simulates dynamic FloraHolland auction pricing with real-time factors
4. **📊 Professional Reports**: Generates wholesale buyer intelligence reports

---

## 🚀 Quick Start

### 1. Installation
```bash
# Clone the repository
git clone <your-repo>
cd royal-floraholland-ai

# Create virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate
python -m venv floral_agents
        ↑       ↑
      command  name (you choose this)
floral_agents\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Setup

Create `.env` file:
```bash
cp .env.example .env
```

Edit `.env` with your API keys:
```
GEMINI_API_KEY=your_gemini_key_here
OPENROUTER_API_KEY=your_openrouter_key_here
```

**Get API keys:**
- Gemini: https://aistudio.google.com/app/apikey (FREE)
- OpenRouter: https://openrouter.ai/keys (pay-as-you-go)

### 3. Setup Data Pipeline
```bash
# Step 1: Generate botanical database (uses Pydantic AI)
python scripts/01_generate_botanical_data.py

# Step 2: Download Oxford Flowers images
python scripts/03_download_images.py

# Step 3: Index into ChromaDB
python scripts/02_setup_chromadb.py

# Step 4: Test the agent
python scripts/04_test_agent.py
```

### 4. Run Complete Demo

Open the Jupyter notebook:
```bash
jupyter notebook notebooks/demo_complete_workflow.ipynb
```

---

## 📁 Project Structure
```
royal-floraholland-ai/
│
├── README.md                                  # Project documentation
├── requirements.txt                           # Python dependencies
├── .env.example                               # Environment variables template
├── .gitignore                                 # Git ignore rules
│
├── src/                                       # Source code
│   ├── __init__.py
│   ├── config.py                              # Configuration management
│   │
│   ├── models/                                # Data models
│   │   ├── __init__.py
│   │   ├── schemas.py                         # Pydantic models
│   │   └── clients.py                         # API client wrappers
│   │
│   ├── agents/                                # LangGraph agent
│   │   ├── __init__.py
│   │   ├── state.py                           # State definition
│   │   ├── nodes.py                           # Node implementations
│   │   └── graph.py                           # Workflow construction
│   │
│   └── utils/                                 # Utilities
│       ├── __init__.py
│       ├── pricing.py                         # Dynamic pricing simulation
│       └── database.py                        # ChromaDB utilities
│
├── scripts/                                   # Setup and testing scripts
│   ├── 01_generate_botanical_data.py          # Pydantic AI data generation
│   ├── 02_setup_chromadb.py                   # ChromaDB indexing
│   ├── 03_download_images.py                  # Download Oxford Flowers
│   └── 04_test_agent.py                       # Test complete workflow
│
├── examples/                                  # Additional examples
│   └── marketing_image_gen.py                 # Bonus: AI image generation
│
├── notebooks/                                 # Jupyter demonstrations
│   └── demo_complete_workflow.ipynb           # Complete interactive demo
│
├── data/                                      # Generated data (auto-created)
│   ├── raw/
│   ├── processed/                             # Botanical database JSON
│   └── auction/                               # Synthetic auction data
│
├── flora_images/                              # Flower images (auto-created)
└── flora_db/                                  # ChromaDB storage (auto-created)
```

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Data Generation** | Pydantic AI | Type-safe botanical data generation |
| **Agent Framework** | LangGraph | Multi-step workflow orchestration |
| **Vision Model** | Gemini 2.0 Flash | Free image analysis |
| **Reasoning Model** | DeepSeek V3.2 | Cost-effective text generation |
| **Vector Database** | ChromaDB | Botanical taxonomy RAG |
| **Model Router** | OpenRouter | Secure API access |
| **Embeddings** | SentenceTransformers | Local embedding generation |
| **Dataset** | Oxford Flowers 102 | 8,189 flower images, 102 categories |

---

## 📊 Architecture

### Part 1: Data Generation (Pydantic AI)
- Generate structured botanical database for 102 flower species
- Type-safe validation with Pydantic models
- One-time setup (~$0.30 cost)

### Part 2: Agent Workflow (LangGraph)
```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INPUT                                │
│                    (Flower Image Upload)                         │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                   LANGGRAPH ORCHESTRATOR                         │
└──────────────────────┬──────────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
┌──────────────┐ ┌──────────┐ ┌─────────────┐
│ NODE 1       │ │ NODE 2   │ │ NODE 3      │
│ VISION       │ │ SPECIES  │ │ AUCTION     │
│              │ │ ID + RAG │ │ INTEL       │
│ Gemini 2.0   │ │ DeepSeek │ │ Dynamic     │
│ Flash        │ │ +ChromaDB│ │ Pricing     │
└──────────────┘ └──────────┘ └─────────────┘
        │              │              │
        └──────────────┼──────────────┘
                       │
                       ▼
                ┌──────────────┐
                │ NODE 4       │
                │ SYNTHESIS    │
                │ DeepSeek V3.2│
                └──────────────┘
                       │
                       ▼
            ┌──────────────────┐
            │ MARKET REPORT    │
            └──────────────────┘
```

---

## 💰 Cost Analysis

### Per-Request Cost Breakdown

| Component | Provider | Cost | Notes |
|-----------|----------|------|-------|
| **Vision Analysis** | Gemini 2.0 Flash | $0.00 | FREE tier |
| **Species ID (Input)** | DeepSeek via OpenRouter | $0.0003 | 1,500 tokens × $0.20/M |
| **Species ID (Output)** | DeepSeek via OpenRouter | $0.0004 | 500 tokens × $0.88/M |
| **Synthesis (Input)** | DeepSeek via OpenRouter | $0.0003 | 1,500 tokens × $0.20/M |
| **Synthesis (Output)** | DeepSeek via OpenRouter | $0.0007 | 800 tokens × $0.88/M |
| **ChromaDB** | Local | $0.00 | Self-hosted |
| **TOTAL per identification** | | **~$0.0017** | **$1.70 per 1,000 requests** |

## 🎨 Bonus: Marketing Image Generation

After identifying a flower, you can generate professional marketing images:
```python
from examples.marketing_image_gen import generate_marketing_image

# Generate professional marketing image
image_url = generate_marketing_image(
    scientific_name="Rosa hybrid tea",
    common_name="Tea Rose",
    style="professional"  # or "artistic", "minimal"
)

print(f"Marketing image: {image_url}")
```

**Features:**
- Uses OpenAI DALL-E 3 for high-quality images
- Optional GPT-4o prompt enhancement for context-aware generation
- Multiple style options (professional, artistic, minimal)
- Perfect for FloraHolland catalog, social media, e-commerce

**Styles:**
- `professional`: Studio photography, white background, commercial quality
- `artistic`: Oil painting style, elegant composition, museum quality
- `minimal`: Clean aesthetic, simple background, modern photography

### Total Project Costs

- **Data Generation (one-time)**: ~$0.30 (102 species with GPT-4o-mini)
- **Per Agent Run**: ~$0.002
- **With Marketing Image**: ~$0.042 per complete workflow
- **1,000 Identifications**: ~$2.00
- **1,000 Identifications + Images**: ~$42.00

### Comparison

- **This System**: $1.70 per 1,000 runs (identification only)
- **GPT-4 Vision**: ~$50 per 1,000 runs
- **Savings**: 95% cost reduction

### Comparison

- **This System**: $1.70 per 1,000 runs
- **GPT-4 Vision**: ~$50 per 1,000 runs
- **Savings**: 95% cost reduction

---

## 🎬 Features

### Core Features
- ✅ Multimodal RAG (vision + text retrieval + reasoning)
- ✅ Type-safe data generation with Pydantic AI
- ✅ Production-grade agent orchestration with LangGraph
- ✅ Dynamic auction pricing simulation
- ✅ Professional market intelligence reports

### Bonus Features
- ✅ Marketing image generation with AI
- ✅ Interactive Jupyter notebook demo
- ✅ Complete test suite
- ✅ Cost optimization (95% cheaper than GPT-4)

---

## 📖 Usage Examples

### Basic Usage
```python
import asyncio
from src.agents.graph import flora_agent

async def analyze_flower(image_path: str):
    initial_state = {
        "image_path": image_path,
        "visual_description": [],
        "species_candidates": [],
        "auction_data": {},
        "final_response": "",
        "error": ""
    }
    
    result = await flora_agent.ainvoke(initial_state)
    print(result['final_response'])

# Run
asyncio.run(analyze_flower("path/to/flower.jpg"))
```

### Custom Pricing
```python
from src.utils.pricing import get_dynamic_auction_data

# Get current auction data for a species
auction_data = get_dynamic_auction_data(
    scientific_name="Rosa hybrid tea",
    family="Rosaceae"
)

print(f"Current price: €{auction_data['auction_price_eur']}/stem")
print(f"Trend: {auction_data['price_trend']}")
```

### Query ChromaDB
```python
from src.utils.database import query_chromadb

# Search botanical database
results = query_chromadb(
    "red flower with thorny stem",
    n_results=5
)

for metadata in results['metadatas'][0]:
    print(f"{metadata['common_name']} - {metadata['scientific_name']}")
```

---

## 🧪 Testing

Run the complete test suite:
```bash
# Test individual components
python scripts/04_test_agent.py

# Or use the Jupyter notebook for interactive testing
jupyter notebook notebooks/demo_complete_workflow.ipynb
```

---

## 🎓 Educational Value

This project demonstrates:

### AI/ML Concepts
- Multimodal AI (vision + text)
- Retrieval Augmented Generation (RAG)
- Vector databases and semantic search
- Agent orchestration with state management
- Type-safe AI with Pydantic

### Production Best Practices
- Structured project organization
- Configuration management
- Error handling
- Cost optimization
- Modular architecture

### Frameworks Showcased
- **Pydantic AI**: For structured data generation
- **LangGraph**: For production agent workflows
- **ChromaDB**: For vector storage and retrieval
- **Gemini API**: For vision capabilities
- **OpenRouter**: For model routing and access

---

## 🎥 YouTube Video

This project was created as a demonstration for the **AI Agents Mastery** course, showing:
- Real-world use case (FloraHolland auction)
- Production-grade architecture
- Cost optimization strategies
- Framework comparison (Pydantic AI vs LangGraph)

**Key Differentiators:**
- Real production system (not a toy demo)
- 95% cost savings vs GPT-4
- Modular, extensible architecture
- Complete end-to-end workflow

---

## 🚀 Next Steps

### Enhancements
- [ ] Add real FloraHolland API integration
- [ ] Implement caching for repeated queries
- [ ] Add confidence thresholds and fallback logic
- [ ] Create FastAPI REST endpoint
- [ ] Add streaming responses
- [ ] Implement user feedback loop

### Deployment
- [ ] Containerize with Docker
- [ ] Deploy to cloud (AWS/GCP/Azure)
- [ ] Add monitoring and logging
- [ ] Implement rate limiting
- [ ] Add authentication

---

## 📝 License

MIT License - feel free to use for learning and projects!

---

## 🙏 Acknowledgments

- **Oxford Flowers 102 Dataset** - Visual Geometry Group, University of Oxford
- **Royal FloraHolland** - Inspiration for real-world use case
- **Anthropic, Google, DeepSeek** - For excellent AI APIs
- **LangGraph, Pydantic AI** - For production-grade frameworks

---

## 📧 Contact

For questions about this project or the **AI Agents Mastery** course:
- YouTube: [Your Channel]
- LinkedIn: [Your Profile]
- Course: [AI Agents Mastery Link]

---
HEAD
**Built with ❤️ for the AI Agents Mastery community**
=======
**Built with ❤️ for the AI Agents Mastery community**

