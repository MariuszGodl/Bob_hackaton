# Bob Hackathon - Multi-Agent System with IBM WatsonX

Zaawansowany system do tworzenia i zarządzania wieloagentowymi systemami AI z wykorzystaniem IBM WatsonX.

## 🎯 Główne Komponenty

### 1. **MainAgent** - Centralny Router
MainAgent automatycznie routuje zapytania użytkowników do odpowiednich wyspecjalizowanych agentów.

**Lokalizacja:** [`agents/src/main_agent/main_agent.py`](agents/src/main_agent/main_agent.py)

**Funkcje:**
- Automatyczne routowanie zapytań na podstawie capabilities
- Zarządzanie rejestrem agentów
- Agregacja odpowiedzi
- Obsługa błędów i retry logic

### 2. **Custom Agents** - Wyspecjalizowani Agenci
Agenci dedykowani do konkretnych zadań.

**Przykład:** [`WatsonXAgent`](agents/usage/custom_agents/watsons_agent.py) - agent ogólnego przeznaczenia z dostępem do:
- Narzędzi (text stats, date calc, password gen, URL parser, BMI calc)
- Umiejętności (code review, release notes formatting)
- Serwerów MCP (WatsonX Models Server)

### 3. **Modele Danych**
- [`ResponseDataclass`](agents/src/models/response_model.py) - standaryzacja odpowiedzi
- [`AgentDataclass`](agents/src/models/agent_model.py) - metadane agentów
- [`ToolDefinition`](agents/src/models/tool_model.py) - definicje narzędzi
- [`Skill`](agents/src/models/skill_model.py) - umiejętności agentów
- [`MCPConnection`](agents/src/models/mcp_server_model.py) - połączenia MCP

## 🚀 Szybki Start

### Wymagania
```bash
pip install ibm-watsonx-ai mcp fastmcp uvicorn
```

### Konfiguracja Zmiennych Środowiskowych
```bash
export WATSONX_URL="your_watsonx_url"
export WATSONX_API_KEY="your_api_key"
export WATSONX_PROJECT_ID="your_project_id"
```

### Uruchomienie MCP Server (opcjonalnie)
```bash
# Terminal 1: Uruchom WatsonX MCP Server
python agents/usage/mcp_servers/ibm_watsonx_mcp.py
```

### Uruchomienie MainAgent
```bash
# Terminal 2: Uruchom MainAgent Demo
python demo/run_main_agent.py
```

## 📋 Przykłady Użycia

### 1. Podstawowe Użycie MainAgent

```python
import asyncio
from agents.src.main_agent.main_agent import MainAgent

async def main():
    # Inicjalizacja MainAgent
    main_agent = MainAgent()
    
    # Automatyczne routowanie zapytania
    response = await main_agent.process_query(
        "Calculate the word count for: 'Hello world'"
    )
    
    print(f"Status: {response.status}")
    print(f"Result: {response.data['result']}")
    print(f"Agent Chain: {response.agent_chain}")

asyncio.run(main())
```

### 2. Ręczne Wybieranie Agenta

```python
# Użyj konkretnego agenta
response = await main_agent.process_query(
    query="What is IBM WatsonX?",
    agent_name="watsonx_general_agent"
)
```

### 3. Sprawdzanie Dostępnych Agentów

```python
# Lista wszystkich agentów
agents = main_agent.list_agents()
for agent in agents:
    print(agent.get_summary())

# Statystyki systemu
stats = main_agent.get_statistics()
print(f"Active agents: {stats['active_agents']}")
```

## 🏗️ Struktura Projektu

```
Bob_hackaton-1/
├── agents/
│   ├── config/
│   │   └── agent_registry.json          # Rejestr agentów
│   ├── src/
│   │   ├── main_agent/
│   │   │   └── main_agent.py            # MainAgent - router
│   │   ├── custom_agent/
│   │   │   └── custom_agent.py          # Klasa bazowa agentów
│   │   ├── inference/
│   │   │   └── watsonx_inference.py     # Moduł inferencji WatsonX
│   │   └── models/
│   │       ├── response_model.py        # ResponseDataclass
│   │       ├── agent_model.py           # AgentDataclass
│   │       ├── tool_model.py            # ToolDefinition
│   │       ├── skill_model.py           # Skill
│   │       └── mcp_server_model.py      # MCPConnection
│   ├── usage/
│   │   ├── custom_agents/
│   │   │   ├── watsons_agent.py         # WatsonXAgent
│   │   │   └── run_watsonx_agent.py     # Runner dla WatsonXAgent
│   │   ├── tools/
│   │   │   └── math_tools.py            # Narzędzia matematyczne
│   │   ├── skills/
│   │   │   ├── code_review.py           # Skill: code review
│   │   │   ├── format_release_notes.py  # Skill: release notes
│   │   │   └── slim_shady_skill.py      # Skill: przykładowy
│   │   └── mcp_servers/
│   │       └── ibm_watsonx_mcp.py       # WatsonX MCP Server
│   └── development/                      # Skills dla Bob IDE
│       ├── specification.md
│       ├── mcp_creation.md
│       ├── tool_creaton.md
│       └── skill_creation.md
└── demo/
    ├── run_main_agent.py                # Demo MainAgent
    ├── inference_with_tool_and_mcp.py   # Demo z narzędziami
    └── simple_mcp.py                    # Prosty MCP server
```

## 🔧 Tworzenie Własnego Agenta

### 1. Utwórz Klasę Agenta

```python
from agents.src.custom_agent.custom_agent import CustomAgent
from agents.src.inference.watsonx_inference import model

class MyCustomAgent(CustomAgent):
    def __init__(self):
        super().__init__(
            system_prompt="You are a specialized agent for...",
            skills=[my_skill],
            tools=[my_tool],
            mcp_servers=[my_mcp_server]
        )
    
    async def _execute_inference(self, chat_kwargs):
        return model.chat(**chat_kwargs)
```

### 2. Zarejestruj w agent_registry.json

```json
{
  "agent_name": "my_custom_agent",
  "agent_class": "MyCustomAgent",
  "agent_module": "path.to.my_custom_agent",
  "description": "Agent description",
  "capabilities": ["capability1", "capability2"],
  "available_tools": ["tool1", "tool2"],
  "status": "active",
  "priority": 5
}
```

### 3. Użyj przez MainAgent

```python
response = await main_agent.process_query("Your query here")
# MainAgent automatycznie wybierze odpowiedniego agenta
```

## 📊 Agent Registry

Plik [`agents/config/agent_registry.json`](agents/config/agent_registry.json) zawiera metadane wszystkich agentów:

- **agent_name**: Unikalna nazwa agenta
- **agent_class**: Nazwa klasy Python
- **agent_module**: Ścieżka do modułu
- **description**: Opis agenta
- **capabilities**: Lista możliwości (używana do routingu)
- **available_tools**: Lista dostępnych narzędzi
- **available_skills**: Lista dostępnych umiejętności
- **available_mcp_servers**: Lista serwerów MCP
- **status**: active/inactive/maintenance
- **priority**: Priorytet przy routingu (wyższy = preferowany)

## 🎨 Routing Zapytań

MainAgent używa prostego algorytmu scoringowego:

1. **Capability matching** (+10 punktów za każde dopasowanie)
2. **Tool matching** (+5 punktów za każde dopasowanie)
3. **Skill matching** (+5 punktów za każde dopasowanie)
4. **Priority bonus** (dodaje wartość priority)

Agent z najwyższym score obsługuje zapytanie.

## 🔄 Response Format

Wszystkie agenty zwracają `ResponseDataclass`:

```python
{
    "status": "success" | "error" | "partial",
    "data": {"result": "..."},
    "metadata": {
        "selected_agent": "agent_name",
        "agent_version": "1.0.0",
        "routing_method": "automatic"
    },
    "errors": [...],  # jeśli status == "error"
    "agent_chain": ["main_agent", "custom_agent"]
}
```

## 🧪 Testowanie

### Uruchom Demo MainAgent
```bash
python demo/run_main_agent.py
```

Tryby:
1. **Interactive** - wpisuj własne zapytania
2. **Batch** - uruchom predefiniowane testy
3. **Single** - pojedynczy test (domyślny)

### Uruchom Demo WatsonXAgent
```bash
python agents/usage/custom_agents/run_watsonx_agent.py
```

## 📝 TODO

- [ ] Implementacja Main Agent z LLM-based routing (zamiast keyword-based)
- [ ] System hierarchii agentów z sub-agentami
- [ ] Web Interface (plan w [`agents/web_interface_plan.md`](agents/web_interface_plan.md))
- [ ] Testy jednostkowe
- [ ] Monitoring i logging
- [ ] Caching odpowiedzi
- [ ] Rate limiting

## 🤝 Współpraca

Projekt stworzony podczas Bob Hackathon 2026.

## 📄 Licencja

MIT License